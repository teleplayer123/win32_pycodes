from wlan_client import WlanClient


with WlanClient() as c:
    res = c.get_wlan_connection_attrs()
    print(res)
    # res = c.get_wlan_qos_info()
    # print(res)
    # print("\n\n")
    # res = c.get_realtime_connection_quality()
    # print(res)