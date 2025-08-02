# vncgram.py
from core.utils import load_targets
from core.loader import load_modules
from core.scanner import scan_target
import concurrent.futures

THREADS = 50

def main():
    targets = load_targets("data/targets.txt")
    modules = load_modules()

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        for ip, port in targets:
            executor.submit(scan_target, ip, port, modules)

if __name__ == "__main__":
    main()
