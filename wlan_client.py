from win32_wlan import Win32_WlanApi, WLAN_INTERFACE_STATE_VALUES, WLAN_CONNECTION_MODE_VALUES, DOT11_BSS_TYPE_VALUES, DOT11_PHY_TYPE_VALUES, DOT11_AUTH_ALGORITHM_VALUES, DOT11_CIPHER_ALGORITHM_VALUES


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
    
    def _wlan_realtime_connection_quality(self):
        k = "wlan_intf_opcode_realtime_connection_quality"
        quality_info = self.client.WlanQueryInterface(k)
        return quality_info
    
    def _format_rate(self, num):
        d = str(num)[-3:]
        i = str(num)[:-3]
        rate = "{}.{}".format(i, d)
        return float(rate)

    def _format_bssid(self, raw_bytes):
        return ":".join(map(lambda x: "{:02x}".format(x), raw_bytes))
    
    def _get_wlan_qos_capabilities(self, obj):
        res = {
            "mscs_supported": bool(obj.bMSCSSupported),
            "dscp_to_up_mapping_supported": bool(obj.bDSCPToUPMappingSupported),
            "scss_supported": bool(obj.bSCSSupported),
            "dscp_policy_supported": bool(obj.bDSCPPolicySupported)
        }
        return res
    
    def _get_connection_qos_info(self, obj):
        res = {
            "peer_capabilities": self._get_wlan_qos_capabilities(obj.peerCapabilities),
            "mscs_configured": bool(obj.bMSCSConfigured),
            "dscp_to_up_mapping_configured": bool(obj.bDSCPToUPMappingConfigured),
            "number_configured_scss_streams": obj.ulNumConfiguredSCSStreams,
            "number_configured_dscp_policies": obj.ulNumConfiguredDSCPPolicies
        }
        return res
    
    def _get_wlan_assoc_attrs(self, obj):
        res = {
            "ssid": obj.dot11Ssid.ucSSID.decode(),
            "bss_type": DOT11_BSS_TYPE_VALUES[obj.dot11BssType],
            "bssid": self._format_bssid(obj.dot11Bssid),
            "phy_type": DOT11_PHY_TYPE_VALUES[obj.dot11PhyType],
            "phy_index": obj.uDot11PhyIndex,
            "signal_quality": obj.wlanSignalQuality,
            "rx_rate": self._format_rate(obj.ulRxRate),
            "tx_rate": self._format_rate(obj.ulTxRate)
        }
        return res

    def _get_wlan_sec_attrs(self, obj):
        res = {
            "security_enabled": bool(obj.bSecurityEnabled),
            "onex_enabled": bool(obj.bOneXEnabled),
            "auth_algorithm": DOT11_AUTH_ALGORITHM_VALUES[obj.dot11AuthAlgorithm],
            "cipher_algorithm": DOT11_CIPHER_ALGORITHM_VALUES[obj.dot11CipherAlgorithm]
        }
        return res
    
    def _get_realtime_connection_link_info(self, objs):
        res = []
        for obj in objs:
            link_info = {
                "link_id": obj.ucLinkID,
                "channel_center_freq": obj.ulChannelCenterFrequencyMhz,
                "bandwidth": obj.ulBandwidth,
                "rssi": obj.lRssi,
                "rate_set": obj.wlanRateSet.usRateSet
            }
            res.append(link_info)
        return res

    def get_wlan_connection_attrs(self):
        res = {}
        conn_attrs = self._wlan_connection_attrs().contents
        res["guid"] = str(self.guid)
        res["connection_state"] = WLAN_INTERFACE_STATE_VALUES[conn_attrs.isState]
        res["connection_mode"] = WLAN_CONNECTION_MODE_VALUES[int(conn_attrs.wlanConnectionMode)]
        res["profile_name"] = str(conn_attrs.strProfileName)
        res["association_attrs"] = self._get_wlan_assoc_attrs(conn_attrs.wlanAssociationAttributes)
        res["security_attrs"] = self._get_wlan_sec_attrs(conn_attrs.wlanSecurityAttributes)
        return res
    
    def get_wlan_qos_info(self):
        res = {}
        qos_info = self._wlan_qos_info().contents
        res["guid"] = str(self.guid)
        res["interface_capabilities"] = self._get_wlan_qos_capabilities(qos_info.interfaceCapabilities)
        res["connected"] = bool(qos_info.bConnected)
        res["connection_qos_info"] = self._get_connection_qos_info(qos_info.connectionQoSInfo)
        return res
    
    def get_realtime_connection_quality(self):
        res = {}
        info = self._wlan_realtime_connection_quality().contents
        res["phy_type"] = DOT11_PHY_TYPE_VALUES[info.dot11PhyType]
        res["link_quality"] = info.ulLinkQuality
        res["rx_rate"] = self._format_rate(info.ulRxRate)
        res["tx_rate"] = self._format_rate(info.ulTxRate)
        res["mlo_connection"] = bool(info.bIsMLOConnection)
        res["number_of_links"] = info.ulNumLinks
        res["link_info"] = self._get_realtime_connection_link_info(info.linksInfo)
        return res