from windows_wlan import Win32_WlanApi, WLAN_INTERFACE_STATE_VALUES, WLAN_CONNECTION_MODE_VALUES, DOT11_BSS_TYPE_VALUES, DOT11_PHY_TYPE_VALUES, DOT11_AUTH_ALGORITHM_VALUES, DOT11_CIPHER_ALGORITHM_VALUES


class WlanClient:

    def __init__(self):
        self.client = Win32_WlanApi()

    def get_wlan_connection_attrs(self):
        res = self.client.WlanEnumInterfaces()
        print(str(res[0].InterfaceInfo[0].InterfaceGuid))
        networks = self.client.WlanGetAvailableNetworkList()
        network = networks[0].Network[0].dot11Ssid
        print(network.ucSSID.decode())
        k = "wlan_intf_opcode_current_connection"
        conn_attrs = self.client.WlanQueryInterface(k)
        return conn_attrs
    
    def get_wlan_assoc_attrs(self, obj):
        res = f"""
        SSID: {obj.dot11Ssid.ucSSID.decode()}
        BSS Type: {DOT11_BSS_TYPE_VALUES[obj.dot11BssType]}
        BSSID: {obj.dot11Bssid.decode()}
        PHY Type: {DOT11_PHY_TYPE_VALUES[obj.dot11PhyType]}
        PHY Index: {obj.uDot11PhyIndex}
        Signal Quality: {obj.wlanSignalQuality}
        RX Rate: {obj.ulRxRate}
        TX Rate: {obj.ulTxRate}
        """
        return res

    def get_wlan_sec_attrs(self, obj):
        res = f"""
        Security Enabled: {bool(obj.bSecurityEnabled)}
        OneX Enabled: {bool(obj.bOneXEnabled)}
        Auth Algorithm: {DOT11_AUTH_ALGORITHM_VALUES[obj.dot11AuthAlgorithm]}
        Cipher Algorithm: {DOT11_CIPHER_ALGORITHM_VALUES[obj.dot11CipherAlgorithm]}
        """

    def get_connection_attrs_dict(self):
        res = {}
        conn_attrs = self.get_wlan_connection_attrs()
        res["connection_state"] = WLAN_INTERFACE_STATE_VALUES[conn_attrs.isState]
        res["connection_mode"] = WLAN_CONNECTION_MODE_VALUES[int(conn_attrs.wlanConnectionMode)]
        res["profile_name"] = str(conn_attrs.strProfileName.decode())
        res["association_attrs"] = self.get_wlan_assoc_attrs(conn_attrs.wlanAssociationAttributes)
        res["security_attrs"] = self.get_wlan_sec_attrs(conn_attrs.wlanSecurityAttributes)
        return res
