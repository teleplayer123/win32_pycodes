from win32_wlan import (
    Win32_WlanApi,
    WLAN_INTERFACE_STATE_VALUES,
    WLAN_CONNECTION_MODE_VALUES,
    DOT11_BSS_TYPE_VALUES,
    DOT11_PHY_TYPE_VALUES,
    DOT11_AUTH_ALGORITHM_VALUES,
    DOT11_CIPHER_ALGORITHM_VALUES,
    DOT11_RADIO_STATE_VALUES
)

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
    
    def _wlan_radio_state(self):
        k = "wlan_intf_opcode_radio_state"
        radio_state = self.client.WlanQueryInterface(k)
        return radio_state
    
    def _wlan_stats(self):
        k = "wlan_intf_opcode_statistics"
        stats = self.client.WlanQueryInterface(k)
        return stats
    
    def _wlan_channel_number(self):
        k = "wlan_intf_opcode_channel_number"
        chan = self.client.WlanQueryInterface(k)
        return chan
    
    def _wlan_rssi(self):
        k = "wlan_intf_opcode_rssi"
        rssi = self.client.WlanQueryInterface(k)
        return rssi
    
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
    
    def _get_realtime_connection_link_info(self, objs, num_objs):
        res = []
        for obj in objs[:num_objs]:
            link_info = {
                "link_id": obj.ucLinkID,
                "channel_center_freq": obj.ulChannelCenterFrequencyMhz,
                "bandwidth": obj.ulBandwidth,
                "rssi": obj.lRssi,
                "rate_set": obj.wlanRateSet.usRateSet
            }
            res.append(link_info)
        return res
    
    def _get_wlan_phy_radio_state(self, objs, num_objs):
        res = []
        for obj in objs[:num_objs]:
            info = {
                "phy_index": obj.dwPhyIndex,
                "software_radio_state": DOT11_RADIO_STATE_VALUES[obj.dot11SoftwareRadioState],
                "hardware_radio_state": DOT11_RADIO_STATE_VALUES[obj.dot11HardwareRadioState]
            }
            res.append(info)
        return res
    
    def _get_mac_frame_stats(self, obj):
        res = {
            "transmitted_frame_count": obj.ullTransmittedFrameCount,
            "received_frame_count": obj.ullReceivedFrameCount,
            "wep_excluded_count": obj.ullWEPExcludedCount,
            "tkip_local_mic_fails": obj.ullTKIPLocalMICFailures,
            "tkip_relays": obj.ullTKIPReplays,
            "tkip_icv_error_count": obj.ullTKIPICVErrorCount,
            "ccmp_relays": obj.ullCCMPReplays,
            "ccmp_decrypt_errors": obj.ullCCMPDecryptErrors,
            "wep_undecryptable_count": obj.ullWEPUndecryptableCount,
            "wep_icv_error_count": obj.ullWEPICVErrorCount,
            "decrypt_success_count": obj.ullDecryptSuccessCount,
            "decrypt_failure_count": obj.ullDecryptFailureCount
        }
        return res
    
    def _get_phy_frame_stats(self, objs, num_objs):
        res = []
        for obj in objs[:num_objs]:
            stats = {
                "transmitted_frame_count": obj.ullTransmittedFrameCount,
                "multicast_transmitted_frame_count": obj.ullMulticastTransmittedFrameCount,
                "failed_count": obj.ullFailedCount,
                "retry_count": obj.ullRetryCount,
                "multiple_retry_count": obj.ullMultipleRetryCount,
                "max_tx_lifetime_exceeded_count": obj.ullMaxTXLifetimeExceededCount,
                "transmitted_fragment_count": obj.ullTransmittedFragmentCount,
                "rts_success_count": obj.ullRTSSuccessCount,
                "rts_failure_count": obj.ullRTSFailureCount,
                "ack_failure_count": obj.ullACKFailureCount,
                "received_frame_count": obj.ullReceivedFrameCount,
                "multicast_received_frame_count": obj.ullMulticastReceivedFrameCount,
                "promiscuous_received_frame_count": obj.ullPromiscuousReceivedFrameCount,
                "max_rx_lifetime_exceeded_count": obj.ullMaxRXLifetimeExceededCount,
                "frame_duplicate_count": obj.ullFrameDuplicateCount,
                "received_fragment_count": obj.ullReceivedFragmentCount,
                "promiscuous_receieved_fragment_count": obj.ullPromiscuousReceivedFragmentCount,
                "fcs_error_count": obj.ullFCSErrorCount
            }
            res.append(stats)
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
        res["link_info"] = self._get_realtime_connection_link_info(info.linksInfo, res["number_of_links"])
        return res
    
    def get_wlan_radio_state(self):
        res = {}
        info = self._wlan_radio_state().contents
        res["number_of_phys"] = info.dwNumberOfPhys
        res["phy_radio_state"] = self._get_wlan_phy_radio_state(info.PhyRadioState, res["number_of_phys"])
        return res
    
    def  get_wlan_stats(self):
        res = {}
        info = self._wlan_stats().contents
        res["four_way_handshake_fails"] = info.ullFourWayHandshakeFailures
        res["tkip_counter_measures_invoked"] = info.ullTKIPCounterMeasuresInvoked
        res["reserved"] = info.ullReserved
        res["mac_ucast_counters"] = self._get_mac_frame_stats(info.MacUcastCounters)
        res["mac_mcast_counters"] = self._get_mac_frame_stats(info.MacMcastCounters)
        res["number_of_phys"] = info.dwNumberOfPhys
        res["phy_counters"] = self._get_phy_frame_stats(info.PhyCounters, res["number_of_phys"])
        return res
    
    def get_wlan_channel_number(self):
        res = {}
        chan = self._wlan_channel_number().contents
        rssi = self._wlan_rssi().contents
        res["channel_number"] = chan.value
        res["rssi"] = rssi.value
        return res
