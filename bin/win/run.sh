#!/bin/bash

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RESET='\033[0m'

# # Setup python virtual environment
# echo -e "${CYAN}Setup Python virtual environment.${RESET}"
# sh ./setup.sh

# Setup python virtual environment
echo -e "${CYAN}Running application.${RESET}"
python ./src/main.py --config ./bin/config.json

echo -e "${GREEN}Done.${RESET}"
