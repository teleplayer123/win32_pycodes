from windows_wlan import Win32_WlanApi, WLAN_INTF_OPCODE

w = Win32_WlanApi()
res = w.WlanEnumInterfaces()

print(str(res[0].InterfaceInfo[0].InterfaceGuid))

networks = w.WlanGetAvailableNetworkList()

network = networks[0].Network[0].dot11Ssid

print(network.ucSSID.decode())
k = "wlan_intf_opcode_current_connection"

res = w.WlanQueryInterface()