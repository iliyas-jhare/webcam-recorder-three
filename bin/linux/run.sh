#!/bin/bash

# Current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR=$SCRIPT_DIR/../../
pushd $ROOT_DIR

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Setup python virtual environment
echo -e "${CYAN}Setup Python virtual environment.${RESET}"
source ./bin/linux/setup.sh

# Run application
echo -e "${CYAN}Running application.${RESET}"
python3 ./src/main.py --config ./bin/config.json

echo -e "${CYAN}Run finished.${RESET}"
popd