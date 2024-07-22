import ctypes as ct
from ctypes.wintypes import DWORD, WORD, BYTE


CHAR = ct.c_char
UCHAR = BYTE

DOT11_MAC_ADDRESSv1 = CHAR * 6
DOT11_MAC_ADDRESSv2 = UCHAR * 6

class GUIDv2(ct.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", BYTE * 2),
        ("Data5", BYTE * 6),
    ]

    def __str__(self):
        return "{:08x}-{:04x}-{:04x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], self.Data5[0],
            self.Data5[1], self.Data5[2], self.Data5[3], self.Data5[4], self.Data5[5]
        )
    
class GUIDv1(ct.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", CHAR * 8),
    ]

    def __str__(self):
        return "{:08x}-{:04x}-{:04x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], self.Data4[2],
            self.Data4[3], self.Data4[4], self.Data4[5], self.Data4[6], self.Data4[7]
        )
    
