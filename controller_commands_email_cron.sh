#!/bin/bash

# Set this to be the path to the arubaos_crash_detection folder
PATH_TO_ARUBAOS_CRASH_DETECTION="/path/to/arubaos_crash_detection"
EMAIL="test@email.com"

python3 ${PATH_TO_ARUBAOS_CRASH_DETECTION}/controller_commands.py > ${PATH_TO_ARUBAOS_CRASH_DETECTION}/controller_commands_output


if [ -s ${PATH_TO_ARUBAOS_CRASH_DETECTION}/controller_commands_output ]; then
        # The file is not-empty.
        mail -s "Aruba Controller Commands" ${EMAIL} < ${PATH_TO_ARUBAOS_CRASH_DETECTION}/controller_commands_output
        rm ${PATH_TO_ARUBAOS_CRASH_DETECTION}/controller_commands_output
fi
