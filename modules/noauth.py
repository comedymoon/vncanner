# modules/noauth.py

import socket
import struct

def check(ip, port):
    try:
        s = socket.create_connection((ip, port), timeout=3)
        banner = s.recv(12)

        if not banner.startswith(b"RFB"):
            return False

        # Send supported version back (minimum)
        s.sendall(b"RFB 003.003\n")

        # Receive security types
        sec_type = s.recv(4)
        s.close()

        # 0x01 = No authentication
        if sec_type == b"\x01\x01\x01\x01" or sec_type.endswith(b"\x01"):
            return True

    except Exception:
        return False

    return False

def exploit(ip, port):
    print(f"      [+] Exploit: connect via `vncviewer {ip}::{port}` or dump screen using `vncdotool`.")
