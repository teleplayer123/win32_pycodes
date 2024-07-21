import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, WORD, BYTE, WCHAR, UINT, ULONG, BOOL, LONG, USHORT, BOOLEAN


wlanapi = ct.windll.LoadLibrary("wlanapi.dll")
ERROR_SUCCESS = 0
WLAN_MAX_NAME_LENGTH = 256
DOT11_SSID_MAX_LENGTH = 32
WLAN_MAX_PHY_TYPE_NUMBER = 8
WLAN_MAX_PHY_INDEX = 64
DOT11_RATE_SET_MAX_LENGTH = 126
PVOID = ct.c_void_p
ULONGLONG = ct.c_ulonglong
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

DOT11_MAC_ADDRESS = ct.c_char * 6

WLAN_CONNECTION_MODE_T = UINT
WLAN_CONNECTION_MODE = {
    "wlan_connection_mode_profile": 0,
    "wlan_connection_mode_temporary_profile": 1,
    "wlan_connection_mode_discovery_secure": 2,
    "wlan_connection_mode_discovery_unsecure": 3,
    "wlan_connection_mode_auto": 4,
    "wlan_connection_mode_invalid": 5
}
WLAN_CONNECTION_MODE_VALUES = {v: k for k, v in WLAN_CONNECTION_MODE.items()}

WLAN_OPCODE_VALUE_TYPE_T = UINT
WLAN_OPCODE_VALUE_TYPE = {
    "wlan_opcode_value_type_query_only": 0,
    "wlan_opcode_value_type_set_by_group_policy": 1,
    "wlan_opcode_value_type_set_by_user": 2,
    "wlan_opcode_value_type_invalid": 3
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
WLAN_INTERFACE_STATE_VALUES = {v: k for k, v in WLAN_INTERFACE_STATE.items()}

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
DOT11_AUTH_ALGORITHM_VALUES = {v: k for k, v in DOT11_AUTH_ALGORITHM.items()}

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
DOT11_CIPHER_ALGORITHM_VALUES = {v: k for k, v in DOT11_CIPHER_ALGORITHM.items()}

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
    "dot11_phy_type_dmg": 9,
    "dot11_phy_type_he": 10,
    "dot11_phy_type_eht": 11,
    "dot11_phy_type_IHV_start": 0x80000000,
    "dot11_phy_type_IHV_end": 0xffffffff
}
DOT11_PHY_TYPE_VALUES = {v: k for k, v in DOT11_PHY_TYPE.items()}

DOT11_BSS_TYPE_T = UINT
DOT11_BSS_TYPE = {
    "dot11_BSS_type_infrastructure": 1,
    "dot11_BSS_type_independent": 2,
    "dot11_BSS_type_any": 3
}
DOT11_BSS_TYPE_VALUES = {v: k for k, v in DOT11_BSS_TYPE.items()}

DOT11_RADIO_STATE_T = UINT
DOT11_RADIO_STATE = {
    "dot11_radio_state_unknown": 0,
    "dot11_radio_state_on": 1,
    "dot11_radio_state_off": 2
}

WLAN_IHV_CONTROL_TYPE_T = UINT
WLAN_IHV_CONTROL_TYPE = {
    "wlan_ihv_control_type_service": 0,
    "wlan_ihv_control_type_driver": 1
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

class WLAN_INTERFACE_CAPABILITY(ct.Structure):
    _fields_ = [
        ("bDot11DSupported", BOOL),
        ("dwMaxDesiredSsidListSize", DWORD),
        ("dwMaxDesiredBssidListSize", DWORD),
        ("dwNumberOfSupportedPhys", DWORD),
        ("dot11PhyTypes", DOT11_PHY_TYPE_T * WLAN_MAX_PHY_INDEX)
    ]

class WLAN_ASSOCIATION_ATTRIBUTES(ct.Structure):
    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE_T),
        ("dot11Bssid", DOT11_MAC_ADDRESS),
        ("dot11PhyType", DOT11_PHY_TYPE_T),
        ("uDot11PhyIndex", ULONG),
        ("wlanSignalQuality", ULONG),
        ("ulRxRate", ULONG),
        ("ulTxRate", ULONG)
    ]

class WLAN_QOS_CAPABILITIES(ct.Structure):
    _fields_ = [
        ("bMSCSSupported", BOOL),
        ("bDSCPToUPMappingSupported", BOOL),
        ("bSCSSupported", BOOL),
        ("bDSCPPolicySupported", BOOL)
    ]

class WLAN_CONNECTION_QOS_INFO(ct.Structure):
    _fields_ = [
        ("peerCapabilities", WLAN_QOS_CAPABILITIES),
        ("bMSCSConfigured", BOOL),
        ("bDSCPToUPMappingConfigured", BOOL),
        ("ulNumConfiguredSCSStreams", ULONG),
        ("ulNumConfiguredDSCPPolicies", ULONG)
    ]

class WLAN_QOS_INFO(ct.Structure):
    _fields_ = [
        ("interfaceCapabilities", WLAN_QOS_CAPABILITIES),
        ("bConnected", BOOL),
        ("connectionQoSInfo", WLAN_CONNECTION_QOS_INFO)
    ]

class WLAN_SECURITY_ATTRIBUTES(ct.Structure):
    _fields_ = [
        ("bSecurityEnabled", BOOL),
        ("bOneXEnabled", BOOL),
        ("dot11AuthAlgorithm", DOT11_AUTH_ALGORITHM_T),
        ("dot11CipherAlgorithm", DOT11_CIPHER_ALGORITHM_T)
    ]

class WLAN_CONNECTION_ATTRIBUTES(ct.Structure):
    _fields_ = [
        ("isState", WLAN_INTERFACE_STATE_T),
        ("wlanConnectionMode", WLAN_CONNECTION_MODE_T),
        ("strProfileName", WCHAR * WLAN_MAX_NAME_LENGTH),
        ("wlanAssociationAttributes", WLAN_ASSOCIATION_ATTRIBUTES),
        ("wlanSecurityAttributes", WLAN_SECURITY_ATTRIBUTES)
    ]

class WLAN_PHY_RADIO_STATE(ct.Structure):
    _fields_ = [
        ("dwPhyIndex", DWORD),
        ("dot11SoftwareRadioState", DOT11_RADIO_STATE_T),
        ("dot11HardwareRadioState", DOT11_RADIO_STATE_T)
    ]

class WLAN_RADIO_STATE(ct.Structure):
    _fields_ = [
        ("dwNumberOfPhys", DWORD),
        ("PhyRadioState", WLAN_PHY_RADIO_STATE * WLAN_MAX_PHY_INDEX)
    ]

class WLAN_RATE_SET(ct.Structure):
    _fields_ = [
        ("uRateSetLength", ULONG),
        ("usRateSet", USHORT * DOT11_RATE_SET_MAX_LENGTH)
    ]

class WLAN_REALTIME_CONNECTION_QUALITY_LINK_INFO(ct.Structure):
    _fields_ = [
        ("ucLinkID", ct.c_char),
        ("ulChannelCenterFrequencyMhz", ULONG),
        ("ulBandwidth", ULONG),
        ("lRssi", LONG),
        ("wlanRateSet", WLAN_RATE_SET)
    ]

class WLAN_REALTIME_CONNECTION_QUALITY(ct.Structure):
    _fields_ = [
        ("dot11PhyType", DOT11_PHY_TYPE_T),
        ("ulLinkQuality", ULONG),
        ("ulRxRate", ULONG),
        ("ulTxRate", ULONG),
        ("bIsMLOConnection", BOOL),
        ("ulNumLinks", ULONG),
        ("linksInfo", WLAN_REALTIME_CONNECTION_QUALITY_LINK_INFO * 1)
    ]

class WLAN_MAC_FRAME_STATISTICS(ct.Structure):
    _fields_ = [
        ("ullTransmittedFrameCount", ULONGLONG),
        ("ullReceivedFrameCount", ULONGLONG),
        ("ullWEPExcludedCount", ULONGLONG),
        ("ullTKIPLocalMICFailures", ULONGLONG),
        ("ullTKIPReplays", ULONGLONG),
        ("ullTKIPICVErrorCount", ULONGLONG),
        ("ullCCMPReplays", ULONGLONG),
        ("ullCCMPDecryptErrors", ULONGLONG),
        ("ullWEPUndecryptableCount", ULONGLONG),
        ("ullWEPICVErrorCount", ULONGLONG),
        ("ullDecryptSuccessCount", ULONGLONG),
        ("ullDecryptFailureCount", ULONGLONG)
    ]

class WLAN_PHY_FRAME_STATISTICS(ct.Structure):
    _fields_ = [
        ("ullTransmittedFrameCount", ULONGLONG),
        ("ullMulticastTransmittedFrameCount", ULONGLONG),
        ("ullFailedCount", ULONGLONG),
        ("ullRetryCount", ULONGLONG),
        ("ullMultipleRetryCount", ULONGLONG),
        ("ullMaxTXLifetimeExceededCount", ULONGLONG),
        ("ullTransmittedFragmentCount", ULONGLONG),
        ("ullRTSSuccessCount", ULONGLONG),
        ("ullRTSFailureCount", ULONGLONG),
        ("ullACKFailureCount", ULONGLONG),
        ("ullReceivedFrameCount", ULONGLONG),
        ("ullMulticastReceivedFrameCount", ULONGLONG),
        ("ullPromiscuousReceivedFrameCount", ULONGLONG),
        ("ullMaxRXLifetimeExceededCount", ULONGLONG),
        ("ullFrameDuplicateCount", ULONGLONG),
        ("ullReceivedFragmentCount", ULONGLONG),
        ("ullPromiscuousReceivedFragmentCount", ULONGLONG),
        ("ullFCSErrorCount", ULONGLONG)
    ]

class WLAN_STATISTICS(ct.Structure):
    _fields_ = [
        ("ullFourWayHandshakeFailures", ULONGLONG),
        ("ullTKIPCounterMeasuresInvoked", ULONGLONG),
        ("ullReserved", ULONGLONG),
        ("MacUcastCounters", WLAN_MAC_FRAME_STATISTICS),
        ("MacMcastCounters", WLAN_MAC_FRAME_STATISTICS),
        ("dwNumberOfPhys", DWORD),
        ("PhyCounters", WLAN_PHY_FRAME_STATISTICS * 1)
    ]

class DOT11_AUTH_CIPHER_PAIR(ct.Structure):
    _fields_ = [
        ("AuthAlgoId", DOT11_AUTH_ALGORITHM_T),
        ("CipherAlgoId", DOT11_CIPHER_ALGORITHM_T)
    ]

class WLAN_AUTH_CIPHER_PAIR_LIST(ct.Structure):
    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("pAuthCipherPairLis", DOT11_AUTH_CIPHER_PAIR * 1)
    ]

DOT11_COUNTRY_OR_REGION_STRING = ct.c_char * 3
class WLAN_COUNTRY_OR_REGION_STRING_LIST(ct.Structure):
    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("pCountryOrRegionStringList", DOT11_COUNTRY_OR_REGION_STRING * 1)
    ]

class WLAN_BSS_ENTRY(ct.Structure):
    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("uPhyId", ULONG),
        ("dot11Bssid", DOT11_MAC_ADDRESS),
        ("dot11BssType", DOT11_BSS_TYPE_T),
        ("dot11BssPhyType", DOT11_PHY_TYPE_T),
        ("lRssi", LONG),
        ("uLinkQuality", ULONG),
        ("bInRegDomain", BOOLEAN),
        ("usBeaconPeriod", USHORT),
        ("ullTimestamp", ULONGLONG),
        ("ullHostTimestamp", ULONGLONG),
        ("usCapabilityInformation", USHORT),
        ("ulChCenterFrequency", ULONG),
        ("wlanRateSet", WLAN_RATE_SET),
        ("ulIeOffset", ULONG),
        ("ulIeSize", ULONG)
    ]

class WLAN_BSS_LIST(ct.Structure):
    _fields_ = [
        ("dwTotalSize", DWORD),
        ("dwNumberOfItems", DWORD),
        ("wlanBssEntries", WLAN_BSS_ENTRY * 1)
    ]

class WLAN_CONNECTION_QOS_INFO(ct.Structure):
    _fields_ = [
        ("peerCapabilities", WLAN_QOS_CAPABILITIES),
        ("bMSCSConfigured", BOOL),
        ("bDSCPToUPMappingConfigured", BOOL),
        ("ulNumConfiguredSCSStreams", ULONG),
        ("ulNumConfiguredDSCPPolicies", ULONG)
    ]

WLAN_INTF_OPCODE_TYPES = {
    "wlan_intf_opcode_autoconf_enabled": BOOL,
    "wlan_intf_opcode_background_scan_enabled": BOOL,
    "wlan_intf_opcode_bss_type": DOT11_BSS_TYPE,
    "wlan_intf_opcode_certified_safe_mode": BOOL,
    "wlan_intf_opcode_channel_number": ULONG,
    "wlan_intf_opcode_current_connection": WLAN_CONNECTION_ATTRIBUTES,
    "wlan_intf_opcode_current_operation_mode": ULONG,
    "wlan_intf_opcode_hosted_network_capable": BOOL,
    "wlan_intf_opcode_interface_state": WLAN_INTERFACE_STATE,
    "wlan_intf_opcode_management_frame_protection_capable": BOOL,
    "wlan_intf_opcode_media_streaming_mode": BOOL,
    "wlan_intf_opcode_qos_info": WLAN_QOS_INFO,
    "wlan_intf_opcode_radio_state": WLAN_RADIO_STATE,
    "wlan_intf_opcode_realtime_connection_quality": WLAN_REALTIME_CONNECTION_QUALITY,
    "wlan_intf_opcode_rssi": LONG,
    "wlan_intf_opcode_secondary_sta_interfaces": WLAN_INTERFACE_INFO_LIST,
    "wlan_intf_opcode_secondary_sta_synchronized_connections": BOOL,
    "wlan_intf_opcode_statistics": WLAN_STATISTICS,
    "wlan_intf_opcode_supported_adhoc_auth_cipher_pairs": WLAN_AUTH_CIPHER_PAIR_LIST,
    "wlan_intf_opcode_supported_country_or_region_string_list": WLAN_COUNTRY_OR_REGION_STRING_LIST,
    "wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs": WLAN_AUTH_CIPHER_PAIR_LIST,
    "wlan_intf_opcode_supported_safe_mode": BOOL
}

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
    
    def WlanFreeMemory(self, p_mem):
        func_ref = wlanapi.WlanFreeMemory
        func_ref.argtypes = [PVOID]
        func_ref.restype = None
        func_ref(p_mem)
            
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
        dwflag = DWORD()
        res = func_ref(self._handle, self._guid, dwflag, None, ct.byref(networks))
        if WIN32_CHECK_ERROR(res):
            raise Exception("Error getting available networks")
        return networks
    
    def WlanQueryInterface(self, opcode_key):
        """
        DWORD WlanQueryInterface(
            [in]            HANDLE                  hClientHandle,
            [in]            const GUID              *pInterfaceGuid,
            [in]            WLAN_INTF_OPCODE        OpCode,
                            PVOID                   pReserved,
            [out]           PDWORD                  pdwDataSize,
            [out]           PVOID                   *ppData,
            [out, optional] PWLAN_OPCODE_VALUE_TYPE pWlanOpcodeValueType
            );
        """
        opcode = WLAN_INTF_OPCODE[opcode_key]
        opcode_type = WLAN_INTF_OPCODE_TYPES[opcode_key]
        func_ref = wlanapi.WlanQueryInterface
        func_ref.argtypes = [HANDLE, GUID, WLAN_INTF_OPCODE_T, PVOID, ct.POINTER(DWORD), ct.POINTER(ct.POINTER(opcode_type)), ct.POINTER(WLAN_OPCODE_VALUE_TYPE_T)]
        func_ref.restype = DWORD
        data_size = DWORD()
        data = ct.pointer(opcode_type())
        opcode_value_type = WLAN_OPCODE_VALUE_TYPE_T()
        res = func_ref(self._handle, self._guid, opcode, None, ct.byref(data_size), ct.byref(data), ct.byref(opcode_value_type))
        if WIN32_CHECK_ERROR(res):
            raise Exception("Error querying wlan interface")
        return data

    def WlanIhvControl(self):
        """
        DWORD WlanIhvControl(
            [in]                HANDLE                hClientHandle,
            [in]                const GUID            *pInterfaceGuid,
            [in]                WLAN_IHV_CONTROL_TYPE Type,
            [in]                DWORD                 dwInBufferSize,
            [in]                PVOID                 pInBuffer,
            [in]                DWORD                 dwOutBufferSize,
            [in, out, optional] PVOID                 pOutBuffer,
            [out]               PDWORD                pdwBytesReturned
            );
        """
        func_ref = wlanapi.WlanIhvControl
        func_ref.argtypes = [HANDLE, GUID, WLAN_IHV_CONTROL_TYPE_T, DWORD, PVOID, DWORD, PVOID, ct.POINTER(DWORD)]
        func_ref.restype = DWORD
        #TODO finish this function