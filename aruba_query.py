#!/usr/bin/env python3

"""
File: aruba_query.py
Author: Jeff Hagley - jhagley@piergroup.com
Date: 2023-11-21
Description: This is a class for handling ArubaOS8 RestAPI queries
"""

import requests
from dataclasses import dataclass, field
from constants import *


# This is a class to store the ap data from the controllers.  This makes it easier to add more data later as we are asked for more data
@dataclass
class ArubaAP:
    name: str
    mac: str = field(default="")
    serial: str = field(default="")
    model: str = field(default="")
    primary: str = field(default="")
    secondary: str = field(default="")
    status: str = field(default="")
    ip: str = field(default="")
    flags: str = field(default="")
    group: str = field(default="")


# Class to store the API token per controller or conductor
@dataclass
class ArubaToken:
    wc: str
    uid: str
    csrf: str


# Class to store the inventory of class instantiations for APs and API credentials
@dataclass
class ArubaInventory:
    aps: dict = field(default_factory=dict)
    api: dict = field(default_factory=dict)


# This class does the queries and the work on the controllers.  You need to make sure that ArubaInventory is called and passed into any functions
class ArubaQuery:
    def __init__(self) -> None:
        pass

    def get_aruba_api_token(self, wc, password, inventory):
        r = requests.get(
            url="https://"
            + wc
            + ":4343/v1/api/login?username="
            + USERNAME
            + "&password="
            + password,
            verify=False,
        )
        logindata = r.json()
        # store the api token in a dict to reference later
        tmp_token = ArubaToken(
            wc,
            logindata["_global_result"]["UIDARUBA"],
            logindata["_global_result"]["X-CSRF-Token"],
        )
        inventory.api[wc] = tmp_token

    def aruba_show_command(self, wc, command, inventory):
        # generic show commands api query
        uid = inventory.api[wc].uid
        cookie = dict(SESSION=uid)
        response = requests.get(
            url="https://"
            + wc
            + ":4343/v1/configuration/showcommand?command="
            + command
            + "&UIDARUBA="
            + uid,
            data="",
            headers={},
            cookies=cookie,
            verify=False,
        )
        return response.json()

    def get_aruba_db(self, wc, inventory):
        command = "show+ap+database+long"
        response = self.aruba_show_command(wc, command, inventory)
        # parse json response and update the class
        for ap in response["AP Database"]:
            if ap["Switch IP"] == wc:
                if ap["Status"].startswith("Up"):
                    inventory.aps[ap["Name"]] = ArubaAP(
                        name=ap["Name"],
                        mac=ap["Wired MAC Address"],
                        ip=ap["IP Address"],
                        flags=ap["Flags"],
                        model=ap["AP Type"],
                        serial=ap["Serial #"],
                        primary=ap["Switch IP"],
                        secondary=ap["Standby IP"],
                        status=ap["Status"],
                        group=ap["Group"],
                    )
