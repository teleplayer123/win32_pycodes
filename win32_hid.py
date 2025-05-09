import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, BOOL, CHAR, BYTE, WCHAR, ULONG, USHORT, WORD, LPCWSTR
from win32_utils import GUID


PVOID = ct.c_void_p

# dll references
hidapi = ct.windll.hid
setupapi = ct.windll.setupapi
kernel32 = ct.windll.kernel32

#kernel32 function references
read_file = kernel32.ReadFile


###### setup api ######

DIGCF_VALUES = {
    "default": 0x00000001,
    "present": 0x00000002,
    "all_classes": 0x00000004,
    "profile": 0x00000008,
    "device_interface": 0x00000010
}
DIGCF_TYPE = DWORD

# Call SetupDiGetClassDevsW to get handle by device guid
"""
WINSETUPAPI HDEVINFO SetupDiGetClassDevsW(
  [in, optional] const GUID *ClassGuid,
  [in, optional] PCWSTR     Enumerator,
  [in, optional] HWND       hwndParent,
  [in]           DWORD      Flags
);
"""
get_dev_handle = setupapi.SetupDiGetClassDevsW
get_dev_handle.restype = HANDLE
get_dev_handle.argtypes = [
    ct.POINTER(GUID),
    LPCWSTR,
    HANDLE,
    DIGCF_TYPE
]


###### hid api ######

HID_USAGE_PAGE = {
    "generic": 0x01,
    "game": 0x05,
    "leds": 0x08,
    "button": 0x09
}

HID_USAGE_ID = {
    "pointer": 0x01,
    "mouse": 0x02,
    "joystick": 0x04,
    "game_pad": 0x05,
    "keyboard": 0x06,
    "keypad": 0x07,
    "multi_axis_controller": 0x08
}

USAGE_TYPE = ct.c_uint16

class HIDP_CAPS(ct.Structure):
    _fields_ = [
        ("usage", USAGE_TYPE),
        ("usage_page", USAGE_TYPE),
        ("input_report_byte_length", USHORT),
        ("output_report_byte_length", USHORT),
        ("feature_report_byte_length", USHORT),
        ("reserved", USHORT * 17),
        ("number_link_collection_nodes", USHORT),
        ("number_input_button_caps", USHORT),
        ("number_input_value_caps", USHORT),
        ("number_input_data_indices", USHORT),
        ("number_output_button_caps", USHORT),
        ("number_output_value_caps", USHORT),
        ("number_output_data_indices", USHORT),
        ("number_feature_button_caps", USHORT),
        ("number_feature_value_caps", USHORT),
        ("number_feature_data_indices", USHORT)
    ]

class HIDP_LINK_COLLECTION_NODE(ct.Structure):
    _fields_ = [
        ("link_usage", USAGE_TYPE),
        ("link_usage_page", USAGE_TYPE),
        ("parent", USHORT),
        ("number_of_children", USHORT),
        ("next_sibling", USHORT),
        ("first_child", USHORT),
        ("collection_type", ULONG),
        ("is_alias", ULONG),
        ("reserved", ULONG),
        ("user_context", PVOID)
    ]

class HIDD_ATTRIBUTES(ct.Structure):
    _fields_ = [
        ("size", ULONG),
        ("vendor_id", USHORT),
        ("product_id", USHORT),
        ("version_number", USHORT)
    ]

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