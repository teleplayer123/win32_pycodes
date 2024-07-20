from wlan_client import WlanClient


c = WlanClient()
res = c.get_connection_attrs_dict()
print(res)