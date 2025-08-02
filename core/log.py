# core/log.py

import os
import csv
import time
import requests

OUTPUT_DIR = "output"
CSV_FILE = os.path.join(OUTPUT_DIR, "results.csv")

# Prepare on boot
os.makedirs(OUTPUT_DIR, exist_ok=True)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "ip", "port", "country", "service",
            "banner", "module", "status", "details"
        ])

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=3)
        return r.json().get("country", "Unknown")
    except Exception:
        return "Unknown"

def log_result(ip, port, service, banner, module, status, details=""):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    country = get_country(ip)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp, ip, port, country,
            service, banner, module, status, details
        ])
