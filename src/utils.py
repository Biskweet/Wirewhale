def pretty_print_mac(mac):
    return ':'.join(mac[n:n+2] for n in range(0, len(mac), 2))


def pretty_print_ip(ip):
    return f"{int(ip[0:2], 16)}.{int(ip[2:4], 16)}.{int(ip[4:6], 16)}.{int(ip[6:8], 16)}"


def to_ascii(hexadecimal):
    return bytearray.fromhex(hexadecimal).decode()
