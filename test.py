from wlan_client import WlanClient


c = WlanClient()
res = c.get_wlan_connection_attrs()
print(res)