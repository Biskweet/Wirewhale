class Parser:
    def __init__(self, path):
        try:
            with open(path, "r") as file:
                content = file.read()

        except Exception as err:
            raise SystemExit(f"Could not opoen file (error: {err})")

        # Saving as instance attribute
        self.raw = content


    def clean_data(self):
        """
        Returns the list of frames contained in the trace.
        Each frame is a list of strings (each representing 2 bytes).
        """
        frames = []
        current = []

        for i, line in enumerate(self.raw.splitlines()):
            if int(line[:4], 16) == 0:           # If the line has zero as offset (new frame)
                if i != 0:
                    frames.append(current)       # Only save frame if i != 0 (i.e. not first line)

                current = []

            current.append(line[7:].split(' '))  # Remove offset and split on spaces

        frames.append(sum(current, start=[]))    # Summing all sublists (lines)

        return frames


    @staticmethod
    def scan_ethernet_headers(frame):
        frame = frame[8:]  # Removing the preamble

        mac_dest = frame[:6]
        mac_src  = frame[6:12]

        frame_type = frame[12:14]

        payload_data = self.scan_ip_headers(frame[14:-4])

        crc_field = frame[-4:]

        return {
            "mac_dest": mac_dest,
            "mac_src" : mac_src,
            "frame_type": frame_type,
            "crc_field": crc_field
        }




    @staticmethod
    def scan_ip_headers(frame):
        data = frame[7:21]

        _, hlen = data[0]

        # int(string, 16) converts `string` from hexadecimal str to integer
        header_length = 4 * int(hlen, 16)
        total_length = int(data[2] + data[3], 16)



        return {
            "header_length": header_length,
            "total_length" : total_length,
        }
