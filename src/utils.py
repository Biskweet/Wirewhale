import os
import sys


logo_img = r"""              ´`.´`                        
                :                          
                :                          
         _______:_______        |""\/""|   
       ,'               `.      |      |   
      /                   \      \    /    
     |    O                \_____/    |    
     |                                |    
 ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~"""


logo_text = r"""
___    __    ___ __   _____    _________    __    ______   __      _      __      ______ 
\  \  /  \  /  /|  | |  _  \  |   ___\  \  /  \  /  /|  | |  |    / \    |  |    |   ___|
 \  \/    \/  / |  | | |_)  | |  |__  \  \/    \/  / |  |_|  |   / ^ \   |  |    |  |__  
  \          /  |  | |     /  |   __|  \          /  |   _   |  / /_\ \  |  |    |   __| 
   \   /\   /   |  | | |\  \__|  |____  \   /\   /   |  | |  | / _____ \ |  `---.|  |___ 
    \_/  \_/    |__| |_| `.___|_______|  \_/  \_/    |__| |__|/_/     \_\|______||______|"""


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


def to_text(frames):
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

        # Making arrow below
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

        report += arrow.center(dimensions.columns) + '\n\n\n\n'

    return report


def print_logo(dim: os.terminal_size):
    print("\n\n")

    for line in logo_img.split('\n'):
        print(line.center(dim.columns))

    print()

    for line in logo_text.split("\n"):
        print(line.center(dim.columns))

    print("\n\n\n")


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")



def filter_frames(frames: list[TraceAbstract]):
    ...
