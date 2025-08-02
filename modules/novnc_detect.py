# modules/novnc_detect.py

import requests
import re
from core.log import log_result

def check(ip, port):
    try:
        url = f"http://{ip}:{port}/"
        r = requests.get(url, timeout=3)
        html = r.text.lower()

        # Quick dirty fingerprinting
        if any(keyword in html for keyword in ["novnc", "websockify", "rfb", "html5 vnc", "noVNC".lower()]):
            title = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            if title:
                print(f"      [+] noVNC title: {title.group(1).strip()}")
                log_result(ip, port, "HTTP", "noVNC portal", __name__, "VULNERABLE", title.group(1))
            return True
    except Exception:
        return False
    return False

def exploit(ip, port):
    print(f"      [!] Open noVNC portal — try connecting via browser: http://{ip}:{port}/")
