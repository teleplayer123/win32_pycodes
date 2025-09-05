import ctypes
import struct
import socket
import time

# Load the icmp.dll library
icmp = ctypes.windll.LoadLibrary("icmp.dll")
# icmp = ctypes.windll.LoadLibrary("iphlpapi.dll")

class InAddr(ctypes.Union):
    _fields_ = [("S_addr", ctypes.c_ulong),
                ("S_un_b", ctypes.c_ubyte * 4),
                ("S_un_w", ctypes.c_ushort * 2)]
    

def send_ping_windows(host):
    ip_address = socket.gethostbyname(host)

    # Allocate a buffer for the ICMP request and reply
    # The size of the ICMP header is 8 bytes, followed by the data
    request_data = b"abcdefghijklmnopqrstuvwabcdefghi"  # 32 bytes of data
    request_data_size = len(request_data)
    reply_buffer_size = struct.calcsize("L" * 6 + f"s") + request_data_size + 8
    reply_buffer = ctypes.create_string_buffer(reply_buffer_size)

    # Convert the IP address string to an integer
    dest_ip = int.from_bytes(socket.inet_aton(ip_address), 'big')
    dest_ip = ctypes.c_ulong(dest_ip)
    dest_ip = InAddr(dest_ip)

    # Open a handle to the ICMP service
    handle = icmp.IcmpCreateFile()
    if handle == 0:
        return None, "IcmpCreateFile failed."

    # Send the ping and get the reply
    start_time = time.time()
    ret = icmp.IcmpSendEcho(
        handle,
        dest_ip,
        request_data,
        request_data_size,
        None,  # No options
        ctypes.byref(reply_buffer),
        reply_buffer_size,
        1000  # Timeout in milliseconds
    )
    end_time = time.time()

    icmp.IcmpCloseHandle(handle)

    if ret == 0:
        return None, "Request timed out."

    # Simple check for a valid reply
    reply_header_size = struct.calcsize("L") # Assuming a 4-byte status field is at the start
    if ctypes.cast(ctypes.byref(reply_buffer), ctypes.POINTER(ctypes.c_long))[0] != 0:
        # Success, calculate the round-trip time
        rtt = int((end_time - start_time) * 1000)
        return rtt, "Success"
    else:
        return None, "Request timed out."

if __name__ == "__main__":
    host_to_ping = "8.8.8.8" 

    print(f"Pinging {host_to_ping}...")
    rtt, status = send_ping_windows(host_to_ping)

    if status == "Success":
        print(f"Reply from {host_to_ping}: time={rtt}ms")
    else:
        print(f"Ping failed: {status}")

