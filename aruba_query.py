#!/usr/bin/env python3

"""
File: aruba_query.py
Author: Jeff Hagley - jhagley@piergroup.com
Date: 2023-11-21
Description: This is a class for handling ArubaOS8 RestAPI queries
"""

import requests
from dataclasses import dataclass, field
from netmiko import ConnectHandler
from constants import *
import re
import time


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

    def aruba_show_ap_crash_info_reboot_reason(self, mc, password, ap):
        conn = {
            "device_type": "aruba_os_ssh",
            "host": mc,
            "username": USERNAME,
            "password": password,
            "banner_timeout": 10,
        }

        ch = ConnectHandler(**conn)
        command = f"show ap debug system-status ap-name {ap}"
        crash_info = ch.send_command_timing(
            command, strip_command=False, strip_prompt=False
        )
        reboot_information = False
        for line in crash_info.splitlines():
            if line.startswith(("Reboot Information")):
                reboot_information = True
            elif not line.startswith("-") and reboot_information:
                ch.disconnect()
                return line
        ch.disconnect()
        return None
    

    def remove_non_numeric(self, string):
        return string.replace(",", "").replace("%","")
        # return re.sub(r'\D', '', string)
    
    def aruba_ssh_command(self, mc, commands):
        conn = {
            "device_type": "aruba_os_ssh",
            "host": mc,
            "username": USERNAME,
            "password": PASSWORD,
            "banner_timeout": 10,
        }

        # Run each command in the list and return the results
        ch = ConnectHandler(**conn)
        results = ""
        for command in commands:
            temp_output = ch.send_command_timing(command["command_name"], strip_prompt=True, strip_command=True)
            if command["column"] != "":
                try:
                    temp_result = temp_output.splitlines()
                    column = int(command["column"])-1
                    results += command["command_name"]
                    results += "\n"
                    for line in temp_result:
                        if line.startswith("#"):
                            pass
                        elif command["math_compare"] == "gt":
                            if float(self.remove_non_numeric(line.split()[column])) > float(command["integer"]):
                                results += line
                                results += "\n"
                        elif command["math_compare"] == "lt":
                            if float(self.remove_non_numeric(line.split()[column])) < float(command["integer"]):
                                results += line
                                results += "\n"
                        elif command["math_compare"] == "eq":
                            if float(self.remove_non_numeric(line.split()[column])) == float(command["integer"]):
                                results += line
                                results += "\n"
                        elif command["math_compare"] == "neq":
                            if float(self.remove_non_numeric(line.split()[column])) != float(command["integer"]):
                                results += line
                                results += "\n"
                        elif command["math_compare"] == "gte":
                            if float(self.remove_non_numeric(line.split()[column])) >= float(command["integer"]):
                                results += line
                                results += "\n"
                        elif command["math_compare"] == "lte":
                            if float(self.remove_non_numeric(line.split()[column])) <= float(command["integer"]):
                                results += line
                                results += "\n"
                except Exception as e:
                    results += "\n" + f"Error processing command {command['command_name']}"
                    results += "\n" + f"Error: Column {str(int(column)+1)} - {e}"
                    results += "\n"
            else:
                results += "\n"
                results += command["command_name"]
                results += "\n"
                for line in temp_output.splitlines():
                    if line.startswith("#"):
                        pass
                    elif line.startswith("("):
                        pass
                    else:
                        results += line
                        results += "\n"
            results += "\n"
            time.sleep(1)

        ch.disconnect()
        return results