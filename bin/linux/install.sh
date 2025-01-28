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

# Create application executable
echo -e "${CYAN}Creating application executable.${RESET}"
pyinstaller ./webcam_recorder.spec --clean --noconfirm

# Copy to the internal config directory
echo -e "${CYAN}Copying dist to the internal config directory.${RESET}"
DEST_DIR=../../internal/webcam_recorder/
mkdir $DEST_DIR
cp -fv ./webcam_recorder.spec ./dist/config.json ./dist/webcam_recorder.exe $DEST_DIR
cp -rfv ./bin/ ./src/ $DEST_DIR

echo -e "${CYAN}Install finished.${RESET}"
popd
