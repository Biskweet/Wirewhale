import os
import sys
import webbrowser

import colorama as c


logo = r""" _    _  _                       _             _                   .                 
| |  | |(_)                     | |           | |                 ":"                
| |  | | _  _ __  ___ __      __| |__    __ _ | |  ___          ___:____     |"\/"|  
| |/\| || || '__|/ _ \\ \ /\ / /| '_ \  / _` || | / _ \       ,'        `.    \  /   
\  /\  /| || |  |  __/ \ V  V / | | | || (_| || ||  __/       |  O        \___/  |    
 \/  \/ |_||_|   \___|  \_/\_/  |_| |_| \__,_||_| \___|      ~^~^~^~^~^~^~^~^~^~^~^~^~"""


try:
    char = "▔"
    char.encode(sys.stdout.encoding)
except UnicodeEncodeError as err:
    char = "-"


class TraceAbstract(dict):
    def __init__(self, *args):
        self.update(*args)
        self.__dict__.update(*args)


def pretty_print_mac(mac):
    return ':'.join(mac[n:n+2] for n in range(0, len(mac), 2))


def pretty_print_ip(ip):
    return f"{int(ip[0:2], 16)}.{int(ip[2:4], 16)}.{int(ip[4:6], 16)}.{int(ip[6:8], 16)}"


def to_ascii(hexadecimal):
    return bytearray.fromhex(hexadecimal).decode()


def open_browser(host):
    result = webbrowser.open_new(host)
    if not result:
        print("========================================")
        print(f"COULD NOT OPEN WEB BROWSER. PLEASE OPEN {host} IN YOUR WEB BROWSER.")
        print("========================================")


def colorize(ip, port, mac):
    return (
        c.Fore.BLUE + ip + c.Fore.RESET +
        ':' + c.Fore.CYAN + str(port) + c.Fore.RESET +
        " (MAC: " + c.Fore.GREEN + mac + c.Fore.RESET + ')'
    )


def to_text(frames):
    c.init()  # Initializing Colorama

    dimensions = os.get_terminal_size()

    report = ''
    visited_ips = []

    for f in frames:
        if f.get("http_method") is None:
            infos = f"{f.ethernet_frame_type} communication with protocol {f.protocol}"

        else:
            infos = f"{f.http_method} {f.http_options.get('host', '')}{f.url} ({f.http_version})"

        # report += c.Back.WHITE + c.Fore.BLACK + infos.center(dimensions.columns) + c.Style.RESET_ALL + '\n'
        report += infos.center(dimensions.columns) + '\n'
        report += (char * len(infos)).center(dimensions.columns) + '\n'

        # ==== Making arrow below
        # Calculating size of the bar of the arrow
        arrow = '-' * (dimensions.columns - len(f.ip_src) -
                       len(f.mac_src) - len(f.ip_dest) -
                       len(f.mac_dest) - 30)
        arrow = arrow[:20]  # Max size is 20

        if len(infos) > dimensions.columns or arrow == '':
            return ''  # Not enough size on screen

        if f.ip_dest in visited_ips:
            arrow = f"{f.ip_dest}:{f.port_dest} (MAC: {f.mac_dest}) <{arrow} {f.ip_src}:{f.port_src} (MAC: {f.mac_src})"
        else:
            arrow = f"{f.ip_src}:{f.port_src} (MAC: {f.mac_src}) {arrow}> {f.ip_dest}:{f.port_dest} (MAC: {f.mac_dest})"
            visited_ips.append(f.ip_dest)

        report += arrow.center(dimensions.columns) + '\n\n\n\n\n'

    return report


def print_logo():
    dim = os.get_terminal_size()

    print("\n\n")
    for line in logo.split("\n"):
        print(line.center(dim.columns))
    print("\n\n")

