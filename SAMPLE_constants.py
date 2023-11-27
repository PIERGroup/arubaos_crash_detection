#!/usr/bin/env python3

"""
File: constants.py
Author: Jeff Hagley - jhagley@piergroup.com
Date: 2023-11-21
Description: Standard variables to use in the scripts in this directory
"""

# username and password to aruba infrastructure, should be network operator permissions at a minimum
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
PATH_TO_AP_CRASH_FILES = "/path/to/ap/crash/files"

# this is the list of aruba conductors, only list the primary conductor(s)
ARUBA_MM = ["192.168.0.5", "192.168.0.15", "192.168.0.25"]

KNOWN_CRASHES_BACKUP = {
    "ar_wal_tx_seq.c:4047": "AOS-246729",
    "ar_wal_tx_halphy_send.c:489": "AOS-246561",
    'dog_hb.c:210 DOG_HB detects starvation of task "WLAN_SCHED0"': "AOS-246929",
    'dog_hb.c:210 DOG_HB detects starvation of task "WLAN RT0"': "AOS-246557",
    "ar_wal_tx_sch_status.c:645": "AOS-246184",
    "ar_wal_tx_send.c:8479": "AOS-243789",
    "whal_sring.c:1815": "AOS-244086",
    "wal_soc_dev_hw.c:708": "AOS-243412",
    "wal_rc_ul.c:218": "AOS-247153",
    "whal_recv.c:1656": "AOS-247193",
    "cmnos_thread.c:3850": "AOS-248231",
    "hca_HwComponentBbQca6018_reset.cpp:169": "AOS-248234",
    "ar_wal_tx_send_selfgen.c:4018": "AOS-245833 (bug fix will be in 8.11.2.1)",
    "anul_aon_flow_ageout+0xa0/0x180": "AOS-245834 (bug fix was in 8.11.2.0)",
    "sched_algo_txbf.c:2734": "AOS-245908 (bug fix will be in 8.11.2.1)",
    "ieee80211_get_he_bsscolor_info+0xfc/0x7a8": "AOS-246203 (bug fix was in 8.11.2.0 and will be in 8.10.0.9)",
    "ar_wal_tx_de.c": "AOS-241083 (bug fix will be in 8.10.0.9)",
}
