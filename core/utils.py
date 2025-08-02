# core/utils.py

import ipaddress

DEFAULT_PORTS = [5900, 5901, 5902]

def load_targets(path="data/targets.txt"):
    targets = []

    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                if "/" in line:
                    # CIDR block
                    net = ipaddress.ip_network(line, strict=False)
                    for ip in net.hosts():
                        for port in DEFAULT_PORTS:
                            targets.append((str(ip), port))

                elif "-" in line:
                    # IP range
                    start, end = line.split("-")
                    start_ip = ipaddress.IPv4Address(start.strip())
                    end_ip = ipaddress.IPv4Address(end.strip())
                    for ip_int in range(int(start_ip), int(end_ip) + 1):
                        ip = str(ipaddress.IPv4Address(ip_int))
                        for port in DEFAULT_PORTS:
                            targets.append((ip, port))

                elif ":" in line:
                    # IP with custom port
                    ip, port = line.split(":")
                    targets.append((ip.strip(), int(port.strip())))

                else:
                    # Single IP
                    for port in DEFAULT_PORTS:
                        targets.append((line.strip(), port))

            except Exception as e:
                print(f"[!] Failed to parse line '{line}': {e}")

    return targets
