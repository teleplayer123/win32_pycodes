from windows_wlan import Win32_WlanApi, WLAN_INTERFACE_STATE_VALUES, WLAN_CONNECTION_MODE_VALUES, DOT11_BSS_TYPE_VALUES, DOT11_PHY_TYPE_VALUES, DOT11_AUTH_ALGORITHM_VALUES, DOT11_CIPHER_ALGORITHM_VALUES


class WlanClient:

    def __enter__(self):
        self.client = Win32_WlanApi()
        self.ifaces = self.client.WlanEnumInterfaces()
        self.guid = self.ifaces[0].InterfaceInfo[0].InterfaceGuid
        return self

    def __exit__(self, e_type, e_val, e_tb):
        self.client.WlanCloseHandle()

    def _wlan_connection_attrs(self):
        k = "wlan_intf_opcode_current_connection"
        conn_attrs = self.client.WlanQueryInterface(k)
        return conn_attrs
    
    def _wlan_networks(self):
        networks = self.client.WlanGetAvailableNetworkList()
        # network = networks[0].Network[0]
        # print(network.ucSSID.decode())
        return networks
    
    def _wlan_qos_info(self):
        k = "wlan_intf_opcode_qos_info"
        qos_info = self.client.WlanQueryInterface(k)
        return qos_info
    
    def get_wlan_qos_capabilities(self, obj):
        res = {
            "mscs_supported": bool(obj.bMSCSSupported),
            "dscp_to_up_mapping_supported": bool(obj.bDSCPToUPMappingSupported),
            "scss_supported": bool(obj.bSCSSupported),
            "dscp_policy_supported": bool(obj.bDSCPPolicySupported)
        }
        return res
    
    def get_connection_qos_info(self, obj):
        res = {
            "peer_capabilities": self.get_wlan_qos_capabilities(obj.peerCapabilities),
            "mscs_configured": bool(obj.bMSCSConfigured),
            "dscp_to_up_mapping_configured": bool(obj.bDSCPToUPMappingConfigured),
            "number_configured_scss_streams": obj.ulNumConfiguredSCSStreams,
            "number_configured_dscp_policies": obj.ulNumConfiguredDSCPPolicies
        }
        return res
    
    def get_wlan_assoc_attrs(self, obj):
        res = {
            "ssid": obj.dot11Ssid.ucSSID.decode(),
            "bss_type": DOT11_BSS_TYPE_VALUES[obj.dot11BssType],
            "bssid": obj.dot11Bssid,
            "phy_type": DOT11_PHY_TYPE_VALUES[obj.dot11PhyType],
            "phy_index": obj.uDot11PhyIndex,
            "signal_quality": obj.wlanSignalQuality,
            "rx_rate": obj.ulRxRate,
            "tx_rate": obj.ulTxRate
        }
        return res

    def get_wlan_sec_attrs(self, obj):
        res = {
            "security_enabled": bool(obj.bSecurityEnabled),
            "onex_enabled": bool(obj.bOneXEnabled),
            "auth_algorithm": DOT11_AUTH_ALGORITHM_VALUES[obj.dot11AuthAlgorithm],
            "cipher_algorithm": DOT11_CIPHER_ALGORITHM_VALUES[obj.dot11CipherAlgorithm]
        }
        return res

    def get_wlan_connection_attrs(self):
        res = {}
        conn_attrs = self._wlan_connection_attrs().contents
        res["guid"] = str(self.guid)
        res["connection_state"] = WLAN_INTERFACE_STATE_VALUES[conn_attrs.isState]
        res["connection_mode"] = WLAN_CONNECTION_MODE_VALUES[int(conn_attrs.wlanConnectionMode)]
        res["profile_name"] = str(conn_attrs.strProfileName)
        res["association_attrs"] = self.get_wlan_assoc_attrs(conn_attrs.wlanAssociationAttributes)
        res["security_attrs"] = self.get_wlan_sec_attrs(conn_attrs.wlanSecurityAttributes)
        return res
    
    def get_wlan_qos_info(self):
        res = {}
        qos_info = self._wlan_qos_info().contents
        res["guid"] = str(self.guid)
        res["interface_capabilities"] = self.get_wlan_qos_capabilities(qos_info.interfaceCapabilities)
        res["connected"] = bool(qos_info.bConnected)
        res["connection_qos_info"] = self.get_connection_qos_info(qos_info.connectionQoSInfo)
        return res