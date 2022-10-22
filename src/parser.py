import re

# Custom import
from src import utils


class Parser:
    def __init__(self, path):
        try:
            with open(path, "r") as file:
                content = file.read()

        except Exception as err:
            raise SystemExit(f"Could not opoen file ({err})")

        # Saving as instance attribute
        self.raw = content.lower()


    def parse(self, output="wirewhale_output.txt"):
        frames = self.clean_data()

        result = ''

        for i, frame in enumerate(frames):
            if (frame[24:28] != "0800") or (frame[28] != "4"):
                # breakpoint()
                raise SystemExit(f"Frame {i} not IPv4 (or still has preamble). Aborting.")

            result += str(self.analyze_frame(frame)) + '\n\n'

        return result


    def clean_data(self):
        """
        Returns the list of frames contained in the trace, each as a
        single one-line string. Each character of the string is half
        a byte, so 2 characters make an octet.
        """
        data = self.raw.strip(" \n")  # Stripping whitespaces and line returns

        # Removing duplicates line returns (no matter how many of them)
        data = re.sub(r'\n\n+', r'\n', data)

        frames = []
        current_frame = ''
        offset = 0

        for i, line in enumerate(data.splitlines()):
            offset = int(line[:4], 16)

            # In case we find a new frame
            if offset == 0:
                if i != 0:  # If it's the first
                    frames.append(current_frame)
                    current_frame = ''

            # Add (and overwrite) string starting on the offset index, & remove the trailing ASCII translation
            current_frame = current_frame[:offset * 2] + line[4:line.find('   ')].replace(' ', '')

        frames.append(current_frame)

        return frames


    def analyze_frame(self, frame):
        mac_dest = utils.pretty_print_mac(frame[:12])
        mac_src  = utils.pretty_print_mac(frame[12:24])

        # IPv4 has been checked before no need to read from the frame
        ethernet_frame_type = "IPv4 (0x0800)"

        ip_payload = self.scan_ipv4_headers(frame[28:])

        return ip_payload | {
            "mac_dest": mac_dest,
            "mac_src" : mac_src,
            "ethernet_frame_type": ethernet_frame_type
        }


    def scan_ipv4_headers(self, frame):
        ipversion, hlen = frame[0], frame[1]

        # int(string, 16) converts `string` from hexadecimal str to integer
        header_length = 4 * int(hlen, 16)
        dscp_and_ecn = frame[2:4]
        total_length = int(frame[4:8], 16)

        ip_identifier = int(frame[8:12], 16)
        flags_and_offset = frame[12:16]

        ttl = int(frame[16:18], 16)
        protocol = frame[18:20]
        checksum = frame[20:24]

        ip_src = frame[24:32]
        ip_dest = frame[32:40]

        ip_options = frame[40:2 * header_length]

        # Asserting protocol type
        if protocol != "06":
            raise SystemExit("Frame protocol isn't TCP. Aborting.")

        protocol = "TCP (0x06)"

        # Making IP addresses more readable
        ip_src = utils.pretty_print_ip(ip_src)
        ip_dest = utils.pretty_print_ip(ip_dest)


        tcp_payload = self.scan_tcp_headers(frame[2 * header_length:])


        return tcp_payload | {
            "ipversion": ipversion,
            "ip_header_length": header_length,
            "dscp_and_ecn": dscp_and_ecn,
            "total_length" : total_length,
            "ip_identifier": ip_identifier,
            "flags_and_offset": flags_and_offset,
            "ttl": ttl,
            "protocol": protocol,
            "ip_checksum": checksum,
            "ip_src": ip_src,
            "ip_dest": ip_dest,
            "ip_options": ip_options
        }


    def scan_tcp_headers(self, frame):
        port_src = int(frame[0:4], 16)
        port_dest = int(frame[4:8], 16)

        sequence_number = int(frame[8:16], 16)

        ack_number = int(frame[16:24], 16)

        tcp_header_length = 4 * int(frame[24], 16)
        window_buffer_size = int(frame[28:32], 16)

        tcp_checksum = frame[32:36]
        urgent_pointer = int(frame[36:40], 16)

        tcp_options = frame[40:2 * tcp_header_length]

        # Making sure the frame has HTTP data & isn't just TCP
        if frame[2 * tcp_header_length:] == '':
            http_payload = {}

        else:
            http_payload = self.scan_http_headers(frame[2 * tcp_header_length:])

        return http_payload | {
            "port_src": port_src,
            "port_dest": port_dest,
            "sequence_number": sequence_number,
            "ack_number": ack_number,
            "tcp_header_length": tcp_header_length,
            "window_buffer_size": window_buffer_size,
            "tcp_checksum": tcp_checksum,
            "urgent_pointer": urgent_pointer,
            "tcp_options": tcp_options,
        }


    def scan_http_headers(self, frame):
        frame = frame.split("0d0a0d0a")

        # Unpacking frame (should be at max a 2-uple but using starred expr.,
        # just in case there it is a n-uple. `body` is then a list of str)
        headers, *body = frame

        headers = headers.split("0d0a")

        method, url, http_version = headers[0].split("20")

        # Only split on the first occurence of 0x20 for the rest
        headers = [arg.split("20", 1) for arg in headers[1:]]

        http_options = {utils.to_ascii(key)[:-1]: utils.to_ascii(value) for key, value in headers[1:]}

        return {
            "http_method": method,
            "url": url,
            "http_version": http_version,
            "http_options": http_options,
            "http_body": utils.to_ascii(''.join(body))
        }
