# core/scanner.py

import socket

def is_vnc(ip, port):
    try:
        s = socket.create_connection((ip, port), timeout=3)
        banner = s.recv(12)
        s.close()
        if banner.startswith(b"RFB"):
            return banner.decode(errors="ignore").strip()
    except Exception:
        return None
    return None

def scan_target(ip, port, modules):
    rfb = is_vnc(ip, port)
    if not rfb:
        return

    print(f"[+] {ip}:{port} - VNC detected ({rfb})")

    for mod in modules:
        try:
            vuln = mod.check(ip, port)
            if vuln:
                print(f"    [!] VULNERABLE to {mod.__name__}")
                if hasattr(mod, "exploit"):
                    mod.exploit(ip, port)
        except Exception as e:
            print(f"    [x] Module {mod.__name__} failed: {e}")
