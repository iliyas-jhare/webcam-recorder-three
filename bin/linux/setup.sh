#!/bin/bash

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PRJ_ROOT_DIR=$SCRIPT_DIR/../../
pushd $PRJ_ROOT_DIR

# Colors
RED='\033[0;31m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Install python virtual environment
echo -e "${CYAN}Installing Python virtual environment.${RESET}"
python3 -m venv env
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install Python virtual environment.${RESET}"
    exit 1
fi

# Active the virtual environment
echo -e "${CYAN}Activating virtual environment.${RESET}"
source ./env/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate Python virtual environment.${RESET}"
    exit 1
fi

# Check virtual environment activated
echo -e "${CYAN}Check virtual environment activated.${RESET}"
pip -V

# Upgrade pip
echo -e "${CYAN}Upgrading pip.${RESET}"
python3 -m pip install --upgrade pip

# Install python requirements
echo -e "${CYAN}Installing requirements.${RESET}"
pip install -r ./bin/requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install the requirements from ./bin/requirements.txt${RESET}"
    exit 1
fi

echo -e "${CYAN}Setup finished.${RESET}"
popd
