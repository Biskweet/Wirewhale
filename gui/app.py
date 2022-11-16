import os


def to_text(frames):
    dimensions = os.get_terminal_size()

    report = ''
    visited_ips = []

    for f in frames:
        if f.get("HTTP_METHOD") is None:
            infos = f"{f.ethernet_frame_type} communication with protocol {f.protocol}"

        else:
            infos = f"{f.http_method} {f.http_options.get('host')}{f.url} ({f.http_version})"

        report += infos.center(dimensions.columns) + '\n'

        # Making arrow below
        arrow = '-' * (dimensions.columns - len(f.ip_src) -
                       len(f.mac_src) - len(f.ip_dest) -
                       len(f.mac_dest) - 10)

        if len(infos) > dimensions.columns or arrow == '':
            return ''  # Not enough size on screen

        if f.ip_dest in visited_ips:
            arrow = f"{f.ip_dest} (MAC: {f.mac_dest}) <{arrow} {f.ip_src} (MAC: {f.mac_src})"
        else:
            arrow = f"{f.ip_src} (MAC: {f.mac_src}) {arrow}> {f.ip_dest} (MAC: {f.mac_dest})"
            visited_ips.append(f.ip_dest)

        report += arrow.center(dimensions.columns) + '\n\n'

    return report
