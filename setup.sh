#!/bin/bash

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Install python virtual environment
echo -e "${CYAN}Installing Python virtual environment.${RESET}"
python -m venv env

# Active the virtual environment
echo -e "${CYAN}Activating virtual environment.${RESET}"
activate_env() { . $PWD/env/Scripts/activate; }
activate_env

# Upgrade pip
echo -e "${CYAN}Upgrading pip.${RESET}"
python -m pip install -U pip

# Install python requirements
echo -e "${CYAN}Installing requirements.${RESET}"
pip install -r ./requirements.txt

echo -e "${GREEN}Done.${RESET}"
