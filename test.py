from windows_wlan import Win32_WlanApi, WLAN_INTF_OPCODE_TYPES, WLAN_INTERFACE_STATE_VALUES

w = Win32_WlanApi()
res = w.WlanEnumInterfaces()
