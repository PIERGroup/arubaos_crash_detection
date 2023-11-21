# arubaos_crash_detection

This tool is meant to be ran on the machine in which you are sending your Aruba AP Crash logs too.  It will search the directory for new AP crashes, log into the controllers for more details, and then search the logs for known signatures.  If a known signature is found it will report it, and if it is not found then will notify so more work can be done with Aruba TAC

## Setup

Run this first to install the required python modules for your user

`pip3 install -r requirements.txt --upgrade --user`

setup constants.py with the appropriate user credentials, crash file location, and aruba infrastructure


## Tools
### ap_crash
This tool will search through the crash files for crashes that happened today or yesterday and report on them

### controller_crash
This tool will look for controller crashes and report on them

### crash_email_cron.sh
This is a sample cron job that can be used to email out the results of the tool