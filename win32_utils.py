import ctypes as ct
from ctypes.wintypes import DWORD, WORD, BYTE


CHAR = ct.c_char
UCHAR = BYTE

DOT11_MAC_ADDRESSv1 = CHAR * 6
DOT11_MAC_ADDRESSv2 = UCHAR * 6

class GUIDv2(ct.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", BYTE * 2),
        ("Data5", BYTE * 6),
    ]

    def __str__(self):
        return "{:08x}-{:04x}-{:04x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], self.Data5[0],
            self.Data5[1], self.Data5[2], self.Data5[3], self.Data5[4], self.Data5[5]
        )
    
class GUIDv1(ct.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", CHAR * 8),
    ]

    def __str__(self):
        return "{:08x}-{:04x}-{:04x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], self.Data4[2],
            self.Data4[3], self.Data4[4], self.Data4[5], self.Data4[6], self.Data4[7]
        )
    
AKM_FROM_TYPE = lambda p, a: p + (a << 24)
CIPHER_FROM_TYPE = lambda p, c: p + (c << 24)
RSNA_OUI_PREFIX = 0xac0f00
WPA_OUI_PREFIX = 0xf25000

RSNA_AKM_SUITE = {
    "rsna_akm_none": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 0),
    "rsna_akm_1x": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 1),        # 1X + PRF-128
    "rsna_akm_psk": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 2),        # PSK + PRF-128
    "rsna_akm_ft_1x_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 3),        # FT_1X + SHA-256
    "rsna_akm_ft_psk_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 4),        # FT_PSK + SHA-256
    "rsna_akm_1x_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 5),        # 1X + SHA-256
    "rsna_akm_psk_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 6),        # PSK + SHA-256
    "rsna_akm_tdls_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 7),        # TPK + SHA-256
    "rsna_akm_sae_pmk256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 8),        # SAE + [PMK = 256]
    "rsna_akm_ft_sae_pmk256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 9),        # FT_SAE + [PMK = 256]
    "rsna_akm_peerkey_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 10),
    "rsna_akm_1x_suite_b_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 11),       # 1X_Suite_B + SHA-256
    "rsna_akm_1x_suite_b_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 12),       # 1X_Suite_B/CSNA + SHA-384
    "rsna_akm_ft_1x_sha384_cmp_256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 13),       # FT_1X + SHA-384 + CCMP-256/GCMP-256
    "rsna_akm_fils_1x_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 14),
    "rsna_akm_fils_1x_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 15),
    "rsna_akm_ft_fils_1x_sha256": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 16),
    "rsna_akm_ft_fils_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 17),
    "rsna_akm_owe": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 18),       # Reserved
    "rsna_akm_ft_psk_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 19),       # FT_PSK + SHA-384
    "rsna_akm_psk_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 20),       # PSK + SHA-384
                                                                                    # 21 is not defined
    "rsna_akm_ft_1x_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 22),       # FT_1X + SHA-384
    "rsna_akm_1x_sha384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 23),       # 1X + SHA-384
    "rsna_akm_sae_pmk384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 24),       # SAE + [PMK = 384]
    "rsna_akm_ft_sae_pmk384": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 25),       # FT_SAE + [PMK = 384]
    "rsna_akm_max": AKM_FROM_TYPE(RSNA_OUI_PREFIX, 25)
}

WPA_AKM_SUITE = {
    "wpa_akm_none": AKM_FROM_TYPE(WPA_OUI_PREFIX, 0),
    "wpa_akm_1x": AKM_FROM_TYPE(WPA_OUI_PREFIX, 1),         # 1X + PRF-128
    "wpa_akm_psk": AKM_FROM_TYPE(WPA_OUI_PREFIX, 2),         # PSK + PRF-128
    "wpa_akm_max": AKM_FROM_TYPE(WPA_OUI_PREFIX, 2)
}

RSNA_CIPHER_SUITE = {
    "rsna_cipher_group": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 0),
    "rsna_cipher_wep40": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 1),
    "rsna_cipher_tkip": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 2),
    "rsna_cipher_reserved": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 3),
    "rsna_cipher_ccmp_128": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 4),
    "rsna_cipher_wep104": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 5),
    "rsna_cipher_bip_cmac_128": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 6),
    "rsna_cipher_no_group_traffic": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 7),
    "rsna_cipher_gcmp_128": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 8),
    "rsna_cipher_gcmp_256": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 9),
    "rsna_cipher_ccmp_256": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 10),
    "rsna_cipher_bip_gmac_128": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 11),
    "rsna_cipher_bip_gmac_256": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 12),
    "rsna_cipher_bip_cmac_256": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 13),
    "rsna_cipher_max": CIPHER_FROM_TYPE(RSNA_OUI_PREFIX, 13)
}

