import os


logo_img = r"""              ´`.´`                        
                :                          
                :                          
         _______:_______        |""\/""|   
       ,'               `.      |      |   
      /                   \      \    /    
     |    O                \_____/    |    
     |                                |    
 ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~"""


logo_text = r"""___    __    ___ __   ______    _________    __    ______   __      _      __     ______ 
\  \  /  \  /  /|  | |   _  \  |   ___\  \  /  \  /  /|  | |  |    / \    |  |   |   ___|
 \  \/    \/  / |  | |  |_)  | |  |__  \  \/    \/  / |  |_|  |   / ^ \   |  |   |  |__  
  \          /  |  | |      /  |   __|  \          /  |   _   |  / /_\ \  |  |   |   __| 
   \   /\   /   |  | |  |\  \__|  |____  \   /\   /   |  | |  | / _____ \ |  `---|  |___ 
    \_/  \_/    |__| |__| `.___|_______|  \_/  \_/    |__| |__|/_/     \_\|______|______|"""



class TraceAbstract(dict):
    def get(self, key: str) -> object:
        return super().get(key, '')


    def __getitem__(self, key: str) -> object:
        return self.get(key)


    def __setitem__(self, key: str, value: object) -> None:
        super().__setitem__(key, value)
        self.__dict__.update({key: value})


    def __init__(self, *args):
        # Declaring attributes for linters

        # Ethernet attributes
        self.mac_dest : str
        self.mac_src : str
        self.ethernet_frame_type : str
        self.raw_data : str

        # IP attributes
        self.ip : bool = False
        self.ipversion : str
        self.ip_header_length : int
        self.dscp_and_ecn : str
        self.total_length : int
        self.ip_identifier : int
        self.flags_and_offset : str
        self.ttl : int
        self.protocol : str
        self.checksum : str
        self.ip_src : str
        self.ip_dest : str
        self.ip_options : str

        # TCP attributes
        self.tcp : bool = False
        self.port_src : int
        self.port_dest : int
        self.sequence_number : int
        self.ack_number : int
        self.tcp_header_length : int
        self.tcp_flags : dict[str, bool]
        self.window_buffer_size : int
        self.tcp_checksum : str
        self.urgent_pointer : int
        self.tcp_options : str

        # HTTP attributes
        self.http : bool = False
        self.http_method : str
        self.url : str
        self.http_version : str
        self.http_options : dict[str, str]
        self.http_body : str

        # On instantiation, update dictionary & attributes
        self.update(*args)
        self.__dict__.update(*args)


def pretty_print_mac(mac: str) -> str:
    return ':'.join(mac[n:n+2].upper() for n in range(0, len(mac), 2))


def pretty_print_ip(ip: str) -> str:
    return f"{int(ip[0:2], 16)}.{int(ip[2:4], 16)}.{int(ip[4:6], 16)}.{int(ip[6:8], 16)}"


def to_ascii(hexadecimal: str) -> str:
    return bytearray.fromhex(hexadecimal).decode()


def analyze_tcp_flags(data: str) -> dict[str, bool]:
    # Convert hexa to bin
    data = bin(int(data, 16))[2:].zfill(6)

    flags = {}
    flags["URG"] = (data[0] == "1")
    flags["ACK"] = (data[1] == "1")
    flags["PSH"] = (data[2] == "1")
    flags["RST"] = (data[3] == "1")
    flags["SYN"] = (data[4] == "1")
    flags["FIN"] = (data[5] == "1")

    return flags


def to_text(frames: list[TraceAbstract], run_safe=False) -> str:
    dimensions = os.get_terminal_size()

    if run_safe: char, arl, arr = '-', '<', '>'
    else: char, arl, arr = '▔', '◀', '▶'


    report = ''
    visited_ips = []

    for f in frames:
        if f.http == True:
            # Frame is HTTP
            infos = f"{f.http_method} {f.http_options.get('host', '')}{f.url} ({f.http_version})"

        else:
            # Frame is NOT HTTP (TCP or other)
            infos = f"{f.ethernet_frame_type} communication with protocol {f.protocol}"

        # Making arrow below
        arrow = '~' * 20

        # Frame is TCP
        if f.tcp == True:
            if f.ip_dest in visited_ips:
                arrow = f"{f.ip_dest}:{f.port_dest} (MAC: {f.mac_dest}) {arl}{arrow} {f.ip_src}:{f.port_src} (MAC: {f.mac_src})"

            else:
                arrow = f"{f.ip_src}:{f.port_src} (MAC: {f.mac_src}) {arrow}{arr} {f.ip_dest}:{f.port_dest} (MAC: {f.mac_dest})"
                visited_ips.append(f.ip_src)

            flags = str([flag for flag, value in f.tcp_flags.items() if value]).replace("'", "")
            infos += f" (SN={f.sequence_number}, ACK={f.ack_number})" + (f' {flags}' if flags != '[]' else '')

        # Frame if NOT TCP
        else:
            if f.ip_dest in visited_ips:
                arrow = f"{f.ip_dest} (MAC: {f.mac_dest}) {arl}{arrow} {f.ip_src} (MAC: {f.mac_src})"

            else:
                arrow = f"{f.ip_src} (MAC: {f.mac_src}) {arrow}{arr} {f.ip_dest} (MAC: {f.mac_dest})"
                visited_ips.append(f.ip_src)


        if len(infos) > (dimensions.columns - 5) or len(arrow) > (dimensions.columns - 5):
            return ''  # Not enough size on screen

        report += infos.center(dimensions.columns) + '\n'
        report += (char * len(infos)).center(dimensions.columns) + '\n'
        report += arrow.center(dimensions.columns) + '\n' * 4

    return report


def print_logo(dim: os.terminal_size) -> None:
    print("\n\n")

    for line in logo_img.split('\n'):
        print(line.center(dim.columns))

    print()

    for line in logo_text.split("\n"):
        print(line.center(dim.columns))

    print("\n" * 3)


def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def filter_frames(frames: list[TraceAbstract], dim: os.terminal_size) -> list[TraceAbstract]:
    print("\n\n" + "Do you want to apply a filter to your frames? (y/N)".center(dim.columns))
    answer = input(' ' * (dim.columns // 2 - 5) + ">>> ")

    # Answer was 'No' or incorrect, return frames
    if answer.lower() not in ('y', 'yes'):
        return frames

    print('\n' + "What filter(s) do you want to apply ?".center(dim.columns))
    print("1: Source IP address, 2: Source port number, 3: Enforce protocol, 4: Multiple filters".center(dim.columns))

    answer = input(' ' * (dim.columns // 2 - 5) + ">>> ")

    # Filter by IP ===============
    if answer in ('1', '4'):
        print('\n' + "Available source IP addresses:".center(dim.columns) + '\n' + list_all_ips(frames, dim))
        print("Please specify an IP address (empty input for any)".center(dim.columns))
        target_ip = input(' ' * (dim.columns // 2 - 7) + ">>> ")

        frames = [frame for frame in frames if not target_ip or frame.ip_src == target_ip]

    # Filter by PORT =============
    if answer in ('2', '4'):
        print("\n" + "Please specify a port number (empty input for any)".center(dim.columns))
        target_port = input(' ' * (dim.columns // 2 - 7) + ">>> ")

        frames = [frame for frame in frames if not target_port or str(frame.get("port_src")) == target_port]

    # Filter by PROTOCOL =========
    if answer in ('3', '4'):
        print("\n" + "Please specify a protocol to enforce (TCP/HTTP) (empty input for any)".center(dim.columns))
        target_protocol = input(' ' * (dim.columns // 2 - 7) + ">>> ")
        target_protocol = target_protocol.lower()

        if target_protocol in ('tcp', 'http'):
            frames = [frame for frame in frames if not target_protocol or frame.get(target_protocol) == True]

    return frames


def list_all_ips(frames: list[TraceAbstract], dim: os.terminal_size) -> str:
    ips = {f.ip_src for f in frames}
    ip_addresses = ''
    line = []
    for i, ip in enumerate(ips):
        if i and i % 5 == 0:
            ip_addresses += ' - '.join(line).center(dim.columns) + '\n'
            line = []

        line.append(ip)

    ip_addresses += ' - '.join(line).center(dim.columns) + '\n'

    return ip_addresses
