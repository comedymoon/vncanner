# core/loader.py

import os
import importlib.util

MODULES_DIR = "modules"

def load_modules():
    loaded = []
    for fname in os.listdir(MODULES_DIR):
        if not fname.endswith(".py") or fname.startswith("_"):
            continue

        path = os.path.join(MODULES_DIR, fname)
        spec = importlib.util.spec_from_file_location(fname, path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "check"):
                loaded.append(mod)
        except Exception as e:
            print(f"[!] Error loading module {fname}: {e}")
    return loaded
