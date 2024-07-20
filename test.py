from wlan_client import WlanClient


c = WlanClient()
res = c.show_wlan_connection_attrs()

print(res)
