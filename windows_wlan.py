import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, WORD, BYTE, WCHAR, UINT, ULONG, BOOL
from enum import Enum

wlanapi = ct.windll.LoadLibrary("wlanapi.dll")
ERROR_SUCCESS = 0
WLAN_MAX_NAME_LENGTH = 256
DOT11_SSID_MAX_LENGTH = 32
WLAN_MAX_PHY_TYPE_NUMBER = 8
PVOID = ct.c_void_p
WIN32_CHECK_ERROR = lambda e: e != ERROR_SUCCESS

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

WLAN_REASON_CODE_T = UINT
WLAN_REASON_CODE = {
    "success": 0,
    "unknown": 0x10000+1
}

DOT11_AUTH_ALGORITHM_T = UINT
DOT11_AUTH_ALGORITHM = {
    "DOT11_AUTH_ALGO_80211_OPEN": 1,
    "DOT11_AUTH_ALGO_80211_SHARED_KEY": 2,
    "DOT11_AUTH_ALGO_WPA": 3,
    "DOT11_AUTH_ALGO_WPA_PSK": 4,
    "DOT11_AUTH_ALGO_WPA_NONE": 5,
    "DOT11_AUTH_ALGO_RSNA": 6,
    "DOT11_AUTH_ALGO_RSNA_PSK": 7,
    "DOT11_AUTH_ALGO_WPA3": 8,
    "DOT11_AUTH_ALGO_WPA3_ENT_192": 8,
    "DOT11_AUTH_ALGO_WPA3_SAE": 9,
    "DOT11_AUTH_ALGO_OWE": 10,
    "DOT11_AUTH_ALGO_WPA3_ENT": 11,
    "DOT11_AUTH_ALGO_IHV_START": 0x80000000,
    "DOT11_AUTH_ALGO_IHV_END": 0xffffffff
}

DOT11_CIPHER_ALGORITHM_T = UINT
DOT11_CIPHER_ALGORITHM = {
    "DOT11_CIPHER_ALGO_NONE": 0x00,
    "DOT11_CIPHER_ALGO_WEP40": 0x01,
    "DOT11_CIPHER_ALGO_TKIP": 0x02,
    "DOT11_CIPHER_ALGO_CCMP": 0x04,
    "DOT11_CIPHER_ALGO_WEP104": 0x05,
    "DOT11_CIPHER_ALGO_WPA_USE_GROUP": 0x100,
    "DOT11_CIPHER_ALGO_RSN_USE_GROUP": 0x100,
    "DOT11_CIPHER_ALGO_WEP": 0x101,
    "DOT11_CIPHER_ALGO_IHV_START": 0x80000000,
    "DOT11_CIPHER_ALGO_IHV_END": 0xffffffff
}

DOT11_PHY_TYPE_T = UINT
DOT11_PHY_TYPE = {
    "dot11_phy_type_unknown": 0,
    "dot11_phy_type_any": 0,
    "dot11_phy_type_fhss": 1,
    "dot11_phy_type_dsss": 2,
    "dot11_phy_type_irbaseband": 3,
    "dot11_phy_type_ofdm": 4,
    "dot11_phy_type_hrdsss": 5,
    "dot11_phy_type_erp": 6,
    "dot11_phy_type_ht": 7,
    "dot11_phy_type_vht": 8,
    "dot11_phy_type_IHV_start": 0x80000000,
    "dot11_phy_type_IHV_end": 0xffffffff
}

DOT11_BSS_TYPE_T = UINT
DOT11_BSS_TYPE = {
    "dot11_BSS_type_infrastructure": 1,
    "dot11_BSS_type_independent": 2,
    "dot11_BSS_type_any": 3
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

class DOT11_SSID(ct.Structure):
    _fields_ = [
        ("uSSIDLength", ULONG),
        ("ucSSID", ct.c_char * DOT11_SSID_MAX_LENGTH)
    ]

class WLAN_AVAILABLE_NETWORK(ct.Structure):
    _fields_ = [
        ("strProfileName", WCHAR * WLAN_MAX_NAME_LENGTH),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE_T),
        ("uNumberOfBssids", ULONG),
        ("bNetworkConnectable", BOOL),
        ("wlanNotConnectableReason", WLAN_REASON_CODE_T),
        ("uNumberOfPhyTypes", ULONG),
        ("dot11PhyTypes", DOT11_PHY_TYPE_T),
        ("bMorePhyTypes", BOOL),
        ("wlanSignalQuality", ULONG),
        ("bSecurityEnabled", BOOL),
        ("dot11DefaultAuthAlgorithm", DOT11_AUTH_ALGORITHM_T),
        ("dot11DefaultCipherAlgorithm", DOT11_CIPHER_ALGORITHM_T),
        ("dwFlags", DWORD),
        ("dwReserved", DWORD)
    ]

    def dwFlags(self):
        return {
            "WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES": 0x00000001,
            "WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES": 0x00000002
        }

class WLAN_AVAILABLE_NETWORK_LIST(ct.Structure):
    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("dwIndex", DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1)
    ]


class Win32_WlanApi:

    def __init__(self):
        self._handle = self.WlanOpenHandle()
        self._guid = None
        
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
        func_ref.argtypes = [DWORD, PVOID, ct.POINTER(DWORD), ct.POINTER(HANDLE)]  #func argument types 
        func_ref.restype = DWORD  #func return type
        negotiated_ver = DWORD()  #dword holder for pdwNegotiatedVersion reference
        client_handle = HANDLE()  #handle holder for client handle reference
        client_ver = 2  #predefined value client version for newer windows versions
        p_reserved = None  #void variable for reserved param
        res = func_ref(client_ver, p_reserved, ct.byref(negotiated_ver), ct.byref(client_handle))  #byref() used for [Out] params that will be assigned value
        if WIN32_CHECK_ERROR(res):
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
        func_ref.argtypes = [HANDLE, PVOID]
        func_ref.restype = DWORD
        res = func_ref(self._handle, None)
        if WIN32_CHECK_ERROR(res):
            raise Exception("Error closing wlan handle")
        return res

    def WlanEnumInterfaces(self):
        func_ref = wlanapi.WlanEnumInterfaces
        func_ref.argtypes = [HANDLE, PVOID, ct.POINTER(ct.POINTER(WLAN_INTERFACE_INFO_LIST))]
        func_ref.restype = DWORD
        intf_list = ct.pointer(WLAN_INTERFACE_INFO_LIST())
        res = func_ref(self._handle, None, ct.byref(intf_list))
        if WIN32_CHECK_ERROR(res):
            raise Exception("Error enumerating interfaces")
        self._guid = intf_list[0].InterfaceInfo[0].InterfaceGuid
        return intf_list

    def WlanGetAvailableNetworkList(self):
        func_ref = wlanapi.WlanGetAvailableNetworkList
        func_ref.argtypes = [HANDLE, GUID, DWORD, PVOID, ct.POINTER(ct.POINTER(WLAN_AVAILABLE_NETWORK_LIST))]
        func_ref.restype = DWORD
        networks = ct.pointer(WLAN_AVAILABLE_NETWORK_LIST())
        res = func_ref(self._handle, self.guid, None, ct.byref(networks))
        if WIN32_CHECK_ERROR(res):
            raise Exception("Error getting available networks")
        return networks
