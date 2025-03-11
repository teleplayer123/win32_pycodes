from ctypes import *
from ctypes.wintypes import DWORD, HANDLE, BOOL, CHAR, BYTE, WCHAR, ULONG, USHORT, WORD
from win32_utils import GUID


btapi = windll.LoadLibrary("BluetoothApis.dll")
hidapi = windll.hid

def get_hid_guid():
    hid_guid = GUID()
    hidapi.HidD_GetHidGuid(byref(hid_guid))
    return hid_guid

BTH_ADDR = c_ulonglong
BTADDR_BYTE = c_ubyte * 6

BLUETOOTH_MAX_NAME_SIZE = 248

ERROR_SUCCESS = 0

BLUETOOTH_AUTHENTICATION_METHOD = {
    0x00: "bluetooth_authentication_method_legacy",
    0x01: "bluetooth_authentication_method_oob",
    0x02: "bluetooth_authentication_method_numeric_comparison",
    0x03: "bluetooth_authentication_method_passkey_notification",
    0x04: "bluetooth_authentication_method_passkey"
}

class SYSTEMTIME(Structure):
    _fields_ = [
        ("wYear", WORD),
        ("wMonth", WORD),
        ("wDayOfWeek", WORD),
        ("wDay", WORD),
        ("wHour", WORD),
        ("wMinute", WORD),
        ("wSecond", WORD),
        ("wMilliseconds", WORD)
    ]

class BLUETOOTH_ADDRESS(Union):
    _fields_ = [
        ("ullLong", BTH_ADDR),
        ("rgBytes", BTADDR_BYTE)
    ]

class BLUETOOTH_DEVICE_INFO(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("address", BLUETOOTH_ADDRESS),
        ("ulClassofDevice", ULONG),
        ("fConnected", BOOL),
        ("fRemembered", BOOL),
        ("fAuthenticated", BOOL),

    ]

class BLUETOOTH_FIND_RADIO_PARAMS(Structure):
    _fields_ = [
        ("dwSize", DWORD)
    ]

class BLUETOOTH_DEVICE_SEARCH_PARAMS(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("fReturnAuthenticated", BOOL),
        ("fReturnRemembered", BOOL),
        ("fReturnUnknown", BOOL),
        ("fReturnConnected", BOOL),
        ("fIssueInquiry", BOOL),
        ("cTimeoutMultiplier", CHAR),
        ("hRadio", HANDLE)
    ]

class BLUETOOTH_RADIO_INFO(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("address", BLUETOOTH_ADDRESS),
        ("szName", WCHAR * BLUETOOTH_MAX_NAME_SIZE),
        ("ulClassofDevice", ULONG),
        ("lmpSubversion", USHORT),
        ("manufacturer", USHORT)
    ]

def BluetoothGetRadioInfo(h_find):
    func_ref = btapi.BluetoothGetRadioInfo
    func_ref.argtypes = [HANDLE, POINTER(BLUETOOTH_RADIO_INFO)]
    func_ref.restype = DWORD
    btri = BLUETOOTH_RADIO_INFO()
    dres = func_ref(h_find, byref(btri))
    print(f"BluetoothGetRadioInfo Result: {dres}")
    return btri


def BluetoothGetDeviceInfo(h_dev):
    func_ref = btapi.BluetoothGetDeviceInfo
    func_ref.argtypes = [HANDLE, POINTER(BLUETOOTH_DEVICE_INFO)]
    func_ref.restype = DWORD
    btdi = BLUETOOTH_DEVICE_INFO()
    dres = func_ref(h_dev, byref(btdi))
    return btdi


def BluetoothFindFirstRadio():
    """
        HBLUETOOTH_RADIO_FIND BluetoothFindFirstRadio(
            const BLUETOOTH_FIND_RADIO_PARAMS *pbtfrp,
            [out] HANDLE                      *phRadio
        );
    """
    func_ref = btapi.BluetoothFindFirstRadio
    func_ref.argtypes = [POINTER(BLUETOOTH_FIND_RADIO_PARAMS), POINTER(HANDLE)]
    func_ref.restype = DWORD
    ph_radio = HANDLE()
    btfrp = BLUETOOTH_FIND_RADIO_PARAMS()
    h_find = func_ref(byref(btfrp), byref(ph_radio))
    return h_find, ph_radio


def BluetoothFindNextRadio(h_find):
    """
        BOOL BluetoothFindNextRadio(
            [in]  HBLUETOOTH_RADIO_FIND hFind,
            [out] HANDLE                *phRadio
        );
    """
    func_ref = btapi.BluetoothFindNextRadio
    func_ref.argtypes = [HANDLE, POINTER(HANDLE)]
    func_ref.restype = BOOL
    ph_radio = HANDLE()
    bres = func_ref(h_find, byref(ph_radio))
    print(f"Bool: {bres}")
    return ph_radio


def BluetoothFindFirstDevice(h_find):
    func_ref = btapi.BluetoothFindFirstDevice
    func_ref.argtypes = [POINTER(BLUETOOTH_DEVICE_SEARCH_PARAMS), POINTER(BLUETOOTH_DEVICE_INFO)]
    func_ref.restype = HANDLE
    btdsp = BLUETOOTH_DEVICE_SEARCH_PARAMS()
    btdsp.dwSize = sizeof(btdsp)
    btdi = BLUETOOTH_DEVICE_INFO()
    h_dev = func_ref(byref(btdsp), byref(btdi))
    return h_dev



def main():
    h_find, ph_radio = BluetoothFindFirstRadio()
    print(f"hFind Handle: {h_find}")
    print(f"phRadio Handle: {ph_radio}")
    r_info = BluetoothGetRadioInfo(h_find)
    print(f"RadioInfo Address: {r_info.address.rgBytes[:]}")
    



if __name__ == "__main__":
    main()