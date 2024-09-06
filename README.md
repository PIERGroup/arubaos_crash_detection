# arubaos_crash_detection

This tool is meant to be ran on the machine in which you are sending your Aruba AP Crash logs too.  It will search the directory for new AP firmware crashes or AP process crashes, log into the controllers for more details, and then search the logs for known signatures.  If a known signature is found it will report it, and if it is not found then will notify so more work can be done with Aruba TAC.

This will work on 500 and 600 series APs only and for firmware or process crashes.  Legacy APs don't generate the crash files used by this script.  This works for Mobility Conductor (MCR)-Managed Device (MD) structure only, and has been tested on 8.10.0.8 and above code.

You will need to setup scp offloading of crash files to a SCP server

SAMPLE_AP_CRASH_SIGNATURES was last updated on 02-09-2024

## Setup

Run this first to install the required python modules for your user, note Netmiko requires at least Python 3.7 (RHEL 7/Centos 7 and below have Python 3.6 as native Python by default)

`pip3 install -r requirements.txt --upgrade --user`

Copy SAMPLE_constants.py to constants.py
Setup constants.py with the appropriate user credentials, crash file location, and primary aruba conductor APs

Set PATH_TO_AP_CRASH_FILES in constants.py to be the folder on the server where the AP crash files are SCP'd from the controller infrastructure

Please place SAMPLE_AP_CRASH_SIGNATURES in a folder called AP-crash-signature in the same directory as the PATH_TO_AP_CRASH_FILES variable in constants.py.  Rename it to AP-crash-signature-list.txt  For updated versions of this information please reach out to Aruba TAC

ie /path/to/scp/location/AP-crash-signature/AP-crash-signature-list.txt

## Tools
### ap_crash
This tool will search through the crash files for crashes that happened today or yesterday and report on them

### controller_crash
This tool will look for controller crashes and report on them

### crash_email_cron.sh
This is a sample cron job that can be used to email out the results of the tool

### controller_commands.py
This will run the commands listed in controller_command_list 
Format for the controller_command_list is 

column delimeter is ;
1st field: MM, MD, or MM/MD - run on the MM, MD, or Both
2nd field: command to run
3rd field: Can be blank or only display if "col:column (space delimeted) number,math compare:number to compare to"
math compares for 3rd field: gt, lt, gte, lte, equal, notequal

Examples:
MM/MD;show process monitor statistics | include mswitch | exclude PROCESS_RUNNING;""
MD;show datapath utilization | include SPGW,SP,FPGW,DPI,FP | exclude Path;"col:9,gte:70"
MD;show cpuload | include idle;"col:6,lte:25"
MD;show datapath bwm type 0 | include "0     ";"col:5,gte:9000"



Contributor from Aruba ERT - David Nie, david.nie@hpe.com
Please submit a GitHub issue with any feedback