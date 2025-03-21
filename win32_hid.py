import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, BOOL, CHAR, BYTE, WCHAR, ULONG, USHORT, WORD


# windows library for HID devices
hidapi = ct.windll.hid
# setup library for device handle and destruct
setupapi = ct.windll.setupapi



# Call SetupDiGetClassDevsW to get handle and SetupDiDestroyDeviceInfoList to close handle

# Windows HID API

DEVICE_GUIDS = {
    "keyboard": "{884b96c3-56ef-11d1-bc8c-00a0c91405dd}",
    "mouse": "{378DE44C-56EF-11D1-BC8C-00A0C91405DD}",
    "net": "{CAC88484-7515-4C03-82E6-71A87ABAC361}",
    
}

class GUID(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", BYTE * 8),
    ]

    def __str__(self):
        return "{:08x}-{:04x}-{:04x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], self.Data4[2],
            self.Data4[3], self.Data4[4], self.Data4[5], self.Data4[6], self.Data4[7]
        )

# Structs

class HIDD_ATTRIBUTES(ct.Structure):
    _fields_ = [
        ("size", ULONG),
        ("vendor_id", USHORT),
        ("product_id", USHORT),
        ("version_number", USHORT)
    ]

# Functions

def get_hid_guid():
    """ 
    void HidD_GetHidGuid(
        [out] LPGUID HidGuid);
    """
    hid_guid = GUID()
    hidapi.HidD_GetHidGuid(ct.byref(hid_guid))
    return hid_guid

def hid_get_attrs(handle):
    """
    BOOLEAN HidD_GetAttributes(
        [in]  HANDLE            HidDeviceObject,
        [out] PHIDD_ATTRIBUTES  Attributes);
    """
    func_ref = hidapi.HidD_GetAttributes
    func_ref.argtypes = [HANDLE, HIDD_ATTRIBUTES]
    func_ref.restype = BOOL
    hid_attrs = ct.pointer(HIDD_ATTRIBUTES())
    res = func_ref(handle, ct.byref(hid_attrs))
    return hid_attrs