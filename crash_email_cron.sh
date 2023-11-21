#!/bin/bash

python3 ~/arubaos_crash_detection/controller_crash > ~/arubaos_crash_detection/controller_crash_output
python3 ~/arubaos_/crash_detection/ap_crash > ~/arubaos_crash_detection/ap_crash_output

EMAIL="test@email.com"

if [ -s ~/arubaos_crash_detection/controller_crash_output ]; then
        # The file is not-empty.
        cat ~/arubaos_crash_detection/controller_crash_output | mail -s "Aruba Controller Crash" ${EMAIL}
fi

if [ -s ~/arubaos_crash_detection/ap_crash_output ]; then
        # The file is not-empty.
        cat ~/arubaos_crash_detection/ap_crash_output | mail -s "Aruba AP Crash" ${EMAIL}
fi
