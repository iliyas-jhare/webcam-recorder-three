#!/bin/bash

# Directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR=$SCRIPT_DIR/../../
pushd $ROOT_DIR

# Colors
CYAN='\033[0;36m'
RESET='\033[0m'

# Install python virtual environment
echo -e "${CYAN}Installing Python virtual environment.${RESET}"
python3 -m venv env

# Active the virtual environment
echo -e "${CYAN}Activating virtual environment.${RESET}"
activate_env() { source ./env/bin/activate; }
activate_env

# Check virtual environment activated
echo -e "${CYAN}Check virtual environment activated.${RESET}"
pip -V

# Upgrade pip
echo -e "${CYAN}Upgrading pip.${RESET}"
python3 -m pip install -U pip

# Install python requirements
echo -e "${CYAN}Installing requirements.${RESET}"
pip install -r ./bin/requirements.txt

echo -e "${CYAN}Setup finished.${RESET}"
popd