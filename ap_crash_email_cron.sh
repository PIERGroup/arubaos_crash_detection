#!/bin/bash

# Set this to be the path to the arubaos_crash_detection folder
PATH_TO_ARUBAOS_CRASH_DETECTION="/path/to/arubaos_crash_detection"
EMAIL="test@email.com"

python3 ${PATH_TO_ARUBAOS_CRASH_DETECTION}/ap_crash > ${PATH_TO_ARUBAOS_CRASH_DETECTION}/ap_crash_output


if [ -s "${PATH_TO_ARUBAOS_CRASH_DETECTION}"/ap_crash_output ]; then
        # The file is not-empty.
        mail -s "Aruba AP Crash" ${EMAIL} < ${PATH_TO_ARUBAOS_CRASH_DETECTION}/ap_crash_output
        rm ${PATH_TO_ARUBAOS_CRASH_DETECTION}/ap_crash_output
fi
