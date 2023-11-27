# arubaos_crash_detection

This tool is meant to be ran on the machine in which you are sending your Aruba AP Crash logs too.  It will search the directory for new AP crashes, log into the controllers for more details, and then search the logs for known signatures.  If a known signature is found it will report it, and if it is not found then will notify so more work can be done with Aruba TAC.

This will work on 500 and 600 series APs only and for firmware only crashes.  Legacy APs don't generate the crash files used by this script

You will need to setup scp offloading of crash files to a SCP server

## Setup

Run this first to install the required python modules for your user

`pip3 install -r requirements.txt --upgrade --user`

Copy SAMPLE_constants.py to constants.py
setup constants.py with the appropriate user credentials, crash file location, and aruba infrastructure

Please place SAMPLE_AP_CRASH_SIGNATURES in a folder called AP-crash-signature in the same directory as the PATH_TO_AP_CRASH_FILES variable in constants.py.  Rename it to AP-crash-signature-list.txt  For updated versions of this information please reach out to Aruba TAC

## Tools
### ap_crash
This tool will search through the crash files for crashes that happened today or yesterday and report on them

### controller_crash
This tool will look for controller crashes and report on them

### crash_email_cron.sh
This is a sample cron job that can be used to email out the results of the tool