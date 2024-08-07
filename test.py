from wlan_client import WlanClient
from pprint import pprint


with WlanClient() as c:
    res = c.get_wlan_connection_attrs()
    pprint(res)
    print("\n\n")
    # res = c.get_realtime_connection_quality()
    # pprint(res)
    # print("\n\n")
    res = c.get_wlan_radio_state()
    pprint(res)
    print("\n\n")
    pprint(c.get_wlan_stats())
    print("\n\n")
    res = c.get_wlan_channel_number()
    pprint(res)