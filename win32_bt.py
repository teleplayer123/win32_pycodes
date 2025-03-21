import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, BOOL, CHAR, BYTE, WCHAR, ULONG, USHORT, WORD


# windows library for bluetooth
btapi = ct.windll.LoadLibrary("BluetoothApis.dll")

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

##### Windows Bluetooth API #####

BTH_ADDR = ct.c_ulonglong
BTADDR_BYTE = ct.c_ubyte * 6

BLUETOOTH_MAX_NAME_SIZE = 248

ERROR_SUCCESS = 0

BLUETOOTH_AUTHENTICATION_METHOD = {
    0x00: "bluetooth_authentication_method_legacy",
    0x01: "bluetooth_authentication_method_oob",
    0x02: "bluetooth_authentication_method_numeric_comparison",
    0x03: "bluetooth_authentication_method_passkey_notification",
    0x04: "bluetooth_authentication_method_passkey"
}

class SYSTEMTIME(ct.Structure):
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

class BLUETOOTH_ADDRESS(ct.Union):
    _fields_ = [
        ("ullLong", BTH_ADDR),
        ("rgBytes", BTADDR_BYTE)
    ]

class BLUETOOTH_DEVICE_INFO(ct.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("address", BLUETOOTH_ADDRESS),
        ("ulClassofDevice", ULONG),
        ("fConnected", BOOL),
        ("fRemembered", BOOL),
        ("fAuthenticated", BOOL),

    ]

class BLUETOOTH_FIND_RADIO_PARAMS(ct.Structure):
    _fields_ = [
        ("dwSize", DWORD)
    ]

class BLUETOOTH_DEVICE_SEARCH_PARAMS(ct.Structure):
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

class BLUETOOTH_RADIO_INFO(ct.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("address", BLUETOOTH_ADDRESS),
        ("szName", WCHAR * BLUETOOTH_MAX_NAME_SIZE),
        ("ulClassofDevice", ULONG),
        ("lmpSubversion", USHORT),
        ("manufacturer", USHORT)
    ]

class Win32_BT:

    def BluetoothGetRadioInfo(self, h_find):
        func_ref = btapi.BluetoothGetRadioInfo
        func_ref.argtypes = [HANDLE, ct.POINTER(BLUETOOTH_RADIO_INFO)]
        func_ref.restype = DWORD
        btri = BLUETOOTH_RADIO_INFO()
        dres = func_ref(h_find, ct.byref(btri))
        print(f"BluetoothGetRadioInfo Result: {dres}")
        return btri


    def BluetoothGetDeviceInfo(self, h_dev):
        func_ref = btapi.BluetoothGetDeviceInfo
        func_ref.argtypes = [HANDLE, ct.POINTER(BLUETOOTH_DEVICE_INFO)]
        func_ref.restype = DWORD
        btdi = BLUETOOTH_DEVICE_INFO()
        dres = func_ref(h_dev, ct.byref(btdi))
        return btdi


    def BluetoothFindFirstRadio(self):
        """
            HBLUETOOTH_RADIO_FIND BluetoothFindFirstRadio(
                const BLUETOOTH_FIND_RADIO_PARAMS *pbtfrp,
                [out] HANDLE                      *phRadio
            );
        """
        func_ref = btapi.BluetoothFindFirstRadio
        func_ref.argtypes = [ct.POINTER(BLUETOOTH_FIND_RADIO_PARAMS), ct.POINTER(HANDLE)]
        func_ref.restype = DWORD
        ph_radio = HANDLE()
        btfrp = BLUETOOTH_FIND_RADIO_PARAMS()
        h_find = func_ref(ct.byref(btfrp), ct.byref(ph_radio))
        return h_find, ph_radio


    def BluetoothFindNextRadio(self, h_find):
        """
            BOOL BluetoothFindNextRadio(
                [in]  HBLUETOOTH_RADIO_FIND hFind,
                [out] HANDLE                *phRadio
            );
        """
        func_ref = btapi.BluetoothFindNextRadio
        func_ref.argtypes = [HANDLE, ct.POINTER(HANDLE)]
        func_ref.restype = BOOL
        ph_radio = HANDLE()
        bres = func_ref(h_find, ct.byref(ph_radio))
        print(f"Bool: {bres}")
        return ph_radio


    def BluetoothFindFirstDevice(self, h_find):
        func_ref = btapi.BluetoothFindFirstDevice
        func_ref.argtypes = [ct.POINTER(BLUETOOTH_DEVICE_SEARCH_PARAMS), ct.POINTER(BLUETOOTH_DEVICE_INFO)]
        func_ref.restype = HANDLE
        btdsp = BLUETOOTH_DEVICE_SEARCH_PARAMS()
        btdsp.dwSize = ct.sizeof(btdsp)
        btdi = BLUETOOTH_DEVICE_INFO()
        h_dev = func_ref(ct.byref(btdsp), ct.byref(btdi))
        return h_dev



def main():
    bt = Win32_BT()
    h_find, ph_radio = bt.BluetoothFindFirstRadio()
    print(f"hFind Handle: {h_find}")
    print(f"phRadio Handle: {ph_radio}")
    r_info = bt.BluetoothGetRadioInfo(h_find)
    print(f"RadioInfo Address: {r_info.address.rgBytes[:]}")


if __name__ == "__main__":
    main()