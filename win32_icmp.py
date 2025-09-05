import ctypes
import struct
import socket

# Load the ICMP.DLL
try:
    icmp = ctypes.windll.icmp
except AttributeError:
    print("ICMP.DLL not found. This script is for Windows only.")
    exit()

# Define the necessary ICMP functions
# IcmpCreateFile
IcmpCreateFile = icmp.IcmpCreateFile
IcmpCreateFile.restype = ctypes.c_void_p

# IcmpCloseHandle
IcmpCloseHandle = icmp.IcmpCloseHandle
IcmpCloseHandle.argtypes = [ctypes.c_void_p]
IcmpCloseHandle.restype = ctypes.c_bool

# IcmpSendEcho
IcmpSendEcho = icmp.IcmpSendEcho
IcmpSendEcho.argtypes = [
    ctypes.c_void_p,        # IcmpHandle
    ctypes.c_ulong,         # DestinationAddress
    ctypes.c_void_p,        # RequestData
    ctypes.c_ushort,        # RequestSize
    ctypes.c_void_p,        # RequestOptions
    ctypes.c_void_p,        # ReplyBuffer
    ctypes.c_ulong,         # ReplySize
    ctypes.c_ulong          # Timeout
]
IcmpSendEcho.restype = ctypes.c_ulong

# Define structures for ICMP_ECHO_REPLY and IP_OPTION_INFORMATION
class IP_OPTION_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("Ttl", ctypes.c_ubyte),
        ("Tos", ctypes.c_ubyte),
        ("Flags", ctypes.c_ubyte),
        ("OptionsSize", ctypes.c_ubyte),
        ("OptionsData", ctypes.c_char_p),
    ]

class ICMP_ECHO_REPLY(ctypes.Structure):
    _fields_ = [
        ("Address", ctypes.c_ulong),
        ("Status", ctypes.c_ulong),
        ("RoundTripTime", ctypes.c_ulong),
        ("DataSize", ctypes.c_ushort),
        ("Reserved", ctypes.c_ushort),
        ("Data", ctypes.c_void_p),
        ("Options", IP_OPTION_INFORMATION),
    ]

def ping_windows_icmp_dll(host, timeout=1000):
    """
    Pings a host using IcmpSendEcho from ICMP.DLL on Windows.

    Args:
        host (str): The hostname or IP address to ping.
        timeout (int): The timeout in milliseconds.

    Returns:
        tuple: A tuple containing (success, round_trip_time_ms) or (False, None) on failure.
    """
    icmp_handle = IcmpCreateFile()
    if icmp_handle == 0:
        print("Error creating ICMP handle.")
        return False, None

    try:
        # Convert host to IP address
        try:
            dest_addr = socket.gethostbyname(host)
            dest_addr_long = struct.unpack("L", socket.inet_aton(dest_addr))[0]
        except socket.gaierror:
            print(f"Could not resolve host: {host}")
            return False, None

        request_data = b"abcdefghijklmnopqrstuvwabcdefghi" # 32 bytes of data
        request_size = len(request_data)

        # Prepare reply buffer
        reply_buffer_size = ctypes.sizeof(ICMP_ECHO_REPLY) + request_size
        reply_buffer = ctypes.create_string_buffer(reply_buffer_size)

        # Send the echo request
        num_replies = IcmpSendEcho(
            icmp_handle,
            dest_addr_long,
            request_data,
            request_size,
            None, # RequestOptions
            reply_buffer,
            reply_buffer_size,
            timeout
        )

        if num_replies > 0:
            echo_reply = ICMP_ECHO_REPLY.from_buffer(reply_buffer)
            if echo_reply.Status == 0: # 0 indicates success
                return True, echo_reply.RoundTripTime
            else:
                print(f"Ping failed with status: {echo_reply.Status}")
                return False, None
        else:
            print("No reply received.")
            return False, None

    finally:
        IcmpCloseHandle(icmp_handle)

if __name__ == "__main__":
    target_host = "google.com"
    success, rtt = ping_windows_icmp_dll(target_host)

    if success:
        print(f"Ping to {target_host} successful. Round trip time: {rtt}ms")
    else:
        print(f"Ping to {target_host} failed.")

    target_host_local = "127.0.0.1"
    success, rtt = ping_windows_icmp_dll(target_host_local)

    if success:
        print(f"Ping to {target_host_local} successful. Round trip time: {rtt}ms")
    else:
        print(f"Ping to {target_host_local} failed.")