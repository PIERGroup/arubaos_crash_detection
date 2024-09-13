#!/usr/bin/env python3

import urllib3
import concurrent.futures
from aruba_query import *
from constants import *
import time
import requests

requests.packages.urllib3.disable_warnings()


def main():
    inventory = ArubaInventory()
    query = ArubaQuery()
    aruba_md = {}
    aruba_mm = {}
    aruba_mm_commands = []
    aruba_md_commands = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for mm in ARUBA_MM:
            executor.submit(query.get_aruba_api_token, mm, PASSWORD, inventory)

    # get the list of infrastructure from the primary conductor, and then get API tokens for the gear
    for mm in ARUBA_MM:
        response = query.aruba_show_command(mm, "show+switches+debug", inventory)
        for switch in response["All Switches"]:
            if switch["Type"] == "MD":
                aruba_md.update({switch["IP Address"]: switch["Name"]})
            elif switch["Type"] == "standby":
                aruba_mm.update({switch["IP Address"]: switch["Name"]})
            elif switch["Type"] == "conductor":
                aruba_mm.update({switch["IP Address"]: switch["Name"]})

    with concurrent.futures.ThreadPoolExecutor() as executor:    
        for md in aruba_md:
            executor.submit(query.get_aruba_api_token, md, PASSWORD, inventory)

    # get the list of commands from controller_command_list
    with open("controller_command_list", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                pass
            else:
                line_split = line.strip().split(";")
                if line_split[2] != "" and line_split[2] != "\n":
                    column = line_split[2].split(",")[0].split(":")[1]
                    math_compare = line_split[2].split(",")[1].split(":")[0]
                    integer = line_split[2].split(",")[1].split(":")[1]
                else:
                    column = ""
                    math_compare = ""
                    integer = ""
                if line_split[0].upper() == "MM":
                    aruba_mm_commands.append({"command_name": line_split[1], "column": column, "math_compare": math_compare, "integer": integer})
                elif line_split[0].upper() == "MD":
                    aruba_md_commands.append({"command_name": line_split[1], "column": column, "math_compare": math_compare, "integer": integer})
                elif "MM" and "MD" in line_split[0].upper():
                    aruba_md_commands.append({"command_name": line_split[1], "column": column, "math_compare": math_compare, "integer": integer})
                    aruba_mm_commands.append({"command_name": line_split[1], "column": column, "math_compare": math_compare, "integer": integer})

    results = ""
    for mm in aruba_mm:
        temp_results = query.aruba_ssh_command(mm, aruba_mm_commands)
        results += aruba_mm[mm] + " " + mm + "\n"
        results += temp_results
        results += "\n"
    
    for md in aruba_md:
        temp_results = query.aruba_ssh_command(md, aruba_md_commands)
        results += aruba_md[md] + " " + md + "\n"
        results += temp_results
        results += "\n"
        
    print(results)

    
    
if __name__ == "__main__":
    main()
