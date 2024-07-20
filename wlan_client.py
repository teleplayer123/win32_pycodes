from windows_wlan import Win32_WlanApi, WLAN_INTF_OPCODE_TYPES, WLAN_INTERFACE_STATE_VALUES, WLAN_CONNECTION_MODE_VALUES


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
        t = WLAN_INTF_OPCODE_TYPES[k]
        conn_attrs = self.client.WlanQueryInterface(k, t)
        return conn_attrs
    
    def get_wlan_assoc_attrs(self):
        pass

    def get_wlan_sec_attrs(self):
        pass

    def show_wlan_connection_attrs(self):
        res = {}
        conn_attrs = self.get_wlan_connection_attrs()
        res["isState"] = WLAN_INTERFACE_STATE_VALUES[int(conn_attrs.isState)]
        res["wlanConnectionMode"] = WLAN_CONNECTION_MODE_VALUES[int(conn_attrs.wlanConnectionMode)]
        res["strProfileName"] = str(conn_attrs.strProfileName.decode())


