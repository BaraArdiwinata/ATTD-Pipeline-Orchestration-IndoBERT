import os
import sys
import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError

# Reconfigure stdout to use UTF-8 to handle unicode symbols/emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Konfigurasi
PIPELINE_NOTEBOOKS = [
    "scripts/cleaner_berita.ipynb",
    "scripts/EDA_FeatExt_NER.ipynb",
    "scripts/Augmentasi_LLM.ipynb",
    "scripts/klasifikasi.ipynb"
]
LOG_PATH = "data/pipeline_execution.log"

def run_notebook(notebook_path, log_file):
    print(f"\n============================================================")
    print(f"⏳ MEMULAI EKSEKUSI: {notebook_path}")
    print(f"============================================================")
    log_file.write(f"\n\n{'='*80}\n")
    log_file.write(f"START EXECUTION: {notebook_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write(f"{'='*80}\n")
    log_file.flush()

    if not os.path.exists(notebook_path):
        err_msg = f"❌ File notebook {notebook_path} tidak ditemukan!"
        print(err_msg)
        log_file.write(err_msg + "\n")
        sys.exit(1)

    # Load notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Buat preprocessor
    # Timeout 1200 detik (20 menit) per notebook untuk mengantisipasi fine-tuning BERT / LLM rate limits
    ep = ExecutePreprocessor(timeout=1200, kernel_name='python3')

    start_time = time.time()
    try:
        # Jalankan notebook secara inplace
        # Resources dict 'path' digunakan agar folder eksekusi sejajar dengan notebook
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
        
        # Simpan hasil eksekusi (inplace) agar output tercatat di notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        elapsed = time.time() - start_time
        success_msg = f"✅ BERHASIL: {notebook_path} selesai dalam {elapsed:.2f} detik."
        print(success_msg)
        log_file.write(success_msg + "\n")
        
        # Tulis output sel ke berkas log
        log_file.write("\n--- DETAILS OF EXECUTED CELLS ---\n")
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                log_file.write(f"\n[Cell {idx}]\nCode:\n{cell.source}\n")
                if 'outputs' in cell:
                    for out in cell.outputs:
                        if out.output_type == 'stream':
                            log_file.write(f"Output ({out.name}):\n{out.text}")
                        elif out.output_type == 'execute_result':
                            log_file.write(f"Result:\n{str(out.data.get('text/plain', ''))}\n")
                        elif out.output_type == 'error':
                            log_file.write(f"Error: {out.ename} - {out.evalue}\n")
                            for line in out.traceback:
                                log_file.write(line + "\n")
        log_file.flush()

    except CellExecutionError as e:
        elapsed = time.time() - start_time
        print(f"\n❌ EROR pada {notebook_path} setelah {elapsed:.2f} detik!")
        print(f"Detail kesalahan:\n{str(e)}")
        
        # Log detail kegagalan
        log_file.write(f"\n{'*'*80}\n")
        log_file.write(f"❌ ERROR DURING EXECUTION: {notebook_path}\n")
        log_file.write(f"{str(e)}\n")
        log_file.write(f"{'*'*80}\n")
        log_file.flush()
        
        # Hentikan orkestrasi jika salah satu fail
        sys.exit(1)

def main():
    # Pastikan folder data ada
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    print("============================================================")
    print("🌿 ORKESTRASI PIPELINE INDOBERT ESG SENTIMENT ANALYSIS 🌿")
    print("============================================================")
    print(f"Log terpusat akan disimpan ke: {LOG_PATH}")
    
    # Buka log file dalam mode append
    with open(LOG_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n\n{'#'*80}\n")
        log_file.write(f"NEW PIPELINE RUN STARTED AT {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"{'#'*80}\n")
        
        for nb_path in PIPELINE_NOTEBOOKS:
            # 1. Smart Skipping (Caching)
            if nb_path == "scripts/cleaner_berita.ipynb":
                if os.path.exists("data/clean_data.csv"):
                    skip_msg = "⏭️ Berkas data/clean_data.csv ditemukan. Melewati Step 1!"
                    print(skip_msg)
                    log_file.write(skip_msg + "\n")
                    log_file.flush()
                    continue
            
            elif nb_path == "scripts/EDA_FeatExt_NER.ipynb":
                if os.path.exists("data/IndoBERT.csv"):
                    skip_msg = "⏭️ Berkas data/IndoBERT.csv ditemukan. Melewati Step 2!"
                    print(skip_msg)
                    log_file.write(skip_msg + "\n")
                    log_file.flush()
                    continue
            
            # 2. Cooldown Sleep
            elif nb_path == "scripts/Augmentasi_LLM.ipynb":
                sleep_msg = "⏳ Memberikan jeda cooldown 10 detik sebelum augmentasi..."
                print(sleep_msg)
                log_file.write(sleep_msg + "\n")
                log_file.flush()
                time.sleep(10)
                
            run_notebook(nb_path, log_file)
            
    print("\n🎉 SELURUH PIPELINE SELESAI DIJALANKAN DENGAN SUKSES! 🎉")

if __name__ == '__main__':
    main()
