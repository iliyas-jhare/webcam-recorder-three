#!/bin/bash

# Current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PRJ_ROOT_DIR=$SCRIPT_DIR/../../
pushd $PRJ_ROOT_DIR

# Colors
RED='\033[0;31m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Setup python virtual environment
echo -e "${CYAN}Setup Python virtual environment.${RESET}"
source ./bin/linux/setup.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to setup Python virtual environment.${RESET}"
    exit 1
fi

# Run application
echo -e "${CYAN}Running application.${RESET}"
python3 ./src/main.py --config ./dist/config.json

echo -e "${CYAN}Run finished.${RESET}"
popd
