################################################################################
### Script to setup and run the Webcam Recorder app in a Python virtual 
### environment on Windows system.
################################################################################

[CmdletBinding()]
param()

################################################################################
###################################  Setup  ####################################
################################################################################
# Directories
$PRJ_ROOT_DIR = "$PSScriptRoot\..\.."
Push-Location $PRJ_ROOT_DIR

# Setup
Write-Host "Setting up virtual environment for Python" -ForegroundColor Cyan
python -m venv env
if ( -not $?) {
    Write-Host "Failed to setup virtual environment" -ForegroundColor Red
    exit 1
}

# Activation
Write-Host "Activating virtual environment" -ForegroundColor Cyan
& .\env\Scripts\Activate.ps1
if ( -not $?) {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Check
Write-Host "Check virtual environment activated" -ForegroundColor Cyan
pip -V

# Upgrade
Write-Host "Upgrading pip" -ForegroundColor Cyan
python -m pip install --upgrade pip

# Requirements
Write-Host "Installing requirements" -ForegroundColor Cyan
pip install -r .\bin\requirements.txt
if ( -not $?) {
    Write-Host "Failed to installer requirements from .\bin\requirements.txt" -ForegroundColor Red
    exit 1
}

Write-Host "Setup finished" -ForegroundColor Cyan
Pop-Location


################################################################################
##################################  App Run  ###################################
################################################################################

Push-Location $PRJ_ROOT_DIR

# Run
Write-Host "Running app" -ForegroundColor Cyan
python ./src/main.py --config ./dist/config.json

Pop-Location
