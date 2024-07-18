import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, WORD, BOOLEAN, BYTE, WCHAR, UINT
from enum import Enum

wlanapi = ct.windll.LoadLibrary("wlanapi.dll")
ERROR_SUCCESS = 0

class GUID(ct.Structure):
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

WLAN_CONNECTION_MODE_T = UINT
WLAN_CONNECTION_MODE = {
    "wlan_connection_mode_profile": 0,
    "wlan_connection_mode_temporary_profile": 1,
    "wlan_connection_mode_discovery_secure": 2,
    "wlan_connection_mode_discovery_unsecure": 3,
    "wlan_connection_mode_auto": 4,
    "wlan_connection_mode_invalid": 5
}

WLAN_INTF_OPCODE_T = UINT
WLAN_INTF_OPCODE = {
    "wlan_intf_opcode_autoconf_start": 0,
    "wlan_intf_opcode_autoconf_enabled": 1,
    "wlan_intf_opcode_background_scan_enabled": 2,
    "wlan_intf_opcode_media_streaming_mode": 3,
    "wlan_intf_opcode_radio_state": 4,
    "wlan_intf_opcode_bss_type": 5,
    "wlan_intf_opcode_interface_state": 6,
    "wlan_intf_opcode_current_connection": 7,
    "wlan_intf_opcode_channel_number": 8,
    "wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs": 9,
    "wlan_intf_opcode_supported_adhoc_auth_cipher_pairs": 10,
    "wlan_intf_opcode_supported_country_or_region_string_list": 11,
    "wlan_intf_opcode_current_operation_mode": 12,
    "wlan_intf_opcode_supported_safe_mode": 13,
    "wlan_intf_opcode_certified_safe_mode": 14,
    "wlan_intf_opcode_hosted_network_capable": 15,
    "wlan_intf_opcode_management_frame_protection_capable": 16,
    "wlan_intf_opcode_secondary_sta_interfaces": 17,
    "wlan_intf_opcode_secondary_sta_synchronized_connections": 18,
    "wlan_intf_opcode_autoconf_end": 0x0fffffff,
    "wlan_intf_opcode_msm_start": 0x10000100,
    "wlan_intf_opcode_statistics": 0x10000101,
    "wlan_intf_opcode_rssi": 0x10000102,
    "wlan_intf_opcode_msm_end": 0x1fffffff,
    "wlan_intf_opcode_security_start": 0x20010000,
    "wlan_intf_opcode_security_end": 0x2fffffff,
    "wlan_intf_opcode_ihv_start": 0x30000000,
    "wlan_intf_opcode_ihv_end": 0x3fffffff
}

WLAN_INTERFACE_STATE_T = UINT
WLAN_INTERFACE_STATE = {
    "wlan_interface_state_not_ready": 0,
    "wlan_interface_state_connected": 1,
    "wlan_interface_state_ad_hoc_network_formed": 2,
    "wlan_interface_state_disconnecting": 3,
    "wlan_interface_state_disconnected": 4,
    "wlan_interface_state_associating": 5,
    "wlan_interface_state_discovering": 6,
    "wlan_interface_state_authenticating": 7
}

class WLAN_INTERFACE_INFO(ct.Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", WCHAR),
        ("isState", WLAN_INTERFACE_STATE_T)
    ]

class WLAN_INTERFACE_INFO_LIST(ct.Structure):
    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("dwIndex", DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
    ]


class Win32_WlanApi:

    def __init__(self):
        self._handle = self.WlanOpenHandle()

    def WlanOpenHandle(self):
        """
        DWORD WlanOpenHandle(
        [In] DWORD dwClientVersion,
        [Reserved] PVOID pReserved,
        [Out] PWORD pdwNegotiatedVersion
        [Out] PHANDLE phClientHandle
        )
        """
        func_ref = wlanapi.WlanOpenHandle
        func_ref.argtypes = [DWORD, ct.c_void_p, ct.POINTER(DWORD), ct.POINTER(HANDLE)]  #func argument types 
        func_ref.restype = DWORD  #func return type
        negotiated_ver = DWORD()  #dword holder for pdwNegotiatedVersion reference
        client_handle = HANDLE()  #handle holder for client handle reference
        client_ver = 2  #predefined value client version for newer windows versions
        p_reserved = None  #void variable for reserved param
        res = func_ref(client_ver, p_reserved, ct.byref(negotiated_ver), ct.byref(client_handle))  #byref() used for [Out] params that will be assigned value
        if res != ERROR_SUCCESS:
            raise Exception("Error trying to open wlan handle")
        return client_handle

    def WlanCloseHandle(self):
        """
        DWORD WlanCloseHandle(
        [In] HANDLE pClientHandle,
        [Reserved] PVOID pReserved
        )
        """
        func_ref = wlanapi.WlanCloseHandle
        func_ref.argtypes = [HANDLE, ct.c_void_p]
        func_ref.restype = DWORD
        res = func_ref(self._handle, None)
        if res != ERROR_SUCCESS:
            raise Exception("Error closing wlan handle")
        return res

    def WlanEnumInterfaces(self):
        func_ref = wlanapi.WlanEnumInterfaces
        func_ref.argtypes = [HANDLE, ct.c_void_p, ct.POINTER(ct.POINTER(WLAN_INTERFACE_INFO_LIST))]
        func_ref.restype = DWORD
        intf_list = ct.pointer(WLAN_INTERFACE_INFO_LIST())
        res = func_ref(self._handle, None, ct.byref(intf_list))
        if res != ERROR_SUCCESS:
            raise Exception("Error enumerating interfaces")
        return intf_list
