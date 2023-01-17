@ECHO off
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::: starter script for scanning SD models for malicious pickling
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::: This script assumes you are running *AUTOMATIC1111's web UI* on Windows
::: you will have to paste the path to your model folder(s) below
::: where it says SET SD_FOLDER="..."
::: Your VENV_PATH should be in the first line of the consolewhen you start up the web UI
::: The DOWNLOAD_FOLDER is an optional second folder that you might like to scan,
::: otherwise leave it as is
:::
:SETUP
SET VENV_PATH="F:\Whatever\Path\stable-diffusion-webui\venv\Scripts\Python.exe"
SET SD_FOLDER="F:\Whatever\Path\stable-diffusion-webui\models\Stable-diffusion"
SET DOWNLOAD_FOLDER="F:\Whatever\Other\Folder"
:::
::: how result details should be displayed ("yes" or "no"):
SET SHOW_RESULT_IN_CONSOLE="yes"
SET OPEN_RESULT_IN_NOTEPAD="yes"
:::
::: End of setup, you can now save this script and run it by double clicking
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

REM create / overwrite the output file .\scan_output.txt and initialize with timestamp
ECHO scan started on %date% %time% > scan_output.txt

:SCANNING
REM check if VENV_PATH was set
if %VENV_PATH% equ "F:\Whatever\Path\stable-diffusion-webui\venv\Scripts\Python.exe" (
ECHO ##### ERROR please set your VENV_PATH #####
goto EXIT
)

ECHO "Scanning...Please wait a moment..."

REM check if SD_FOLDER was set
if %SD_FOLDER% equ "F:\Whatever\Path\stable-diffusion-webui\models\Stable-diffusion" (
ECHO ##### ERROR please set your SD_FOLDER #####
goto EXIT
)

ECHO "step 1: SD models folder"
ECHO ####################################################################### >> scan_output.txt
ECHO ##### scanning SD model folder "~~~webui\models\Stable-diffusion" ##### >> scan_output.txt
ECHO ####################################################################### >> scan_output.txt
%VENV_PATH% pickle_scan.py %SD_FOLDER% >> scan_output.txt

REM check if download folder was set, if not just skip instead of errorlevel
if %DOWNLOAD_FOLDER% equ "F:\Whatever\Other\Folder" (
ECHO "No download folder specified"
goto DISPLAY_RESULT
)
ECHO "step 2: download folder"
ECHO ##################################### >> scan_output.txt
ECHO ##### scanning download folder  ##### >> scan_output.txt
ECHO ##################################### >> scan_output.txt
%VENV_PATH% pickle_scan.py %DOWNLOAD_FOLDER% >> scan_output.txt

:DISPLAY_RESULT
if %SHOW_RESULT_IN_CONSOLE% equ "yes" (type scan_output.txt)
if %OPEN_RESULT_IN_NOTEPAD% equ "yes" (start notepad scan_output.txt)

ECHO "Number of failed scans (potentially malicious files):"
find /c "SCAN FAILED" scan_output.txt

:EXIT
pause

::: based on the original code by *TheEliteGeek* in issue #2:
::: @ECHO off
::: ECHO "Scanning...Please wait a moment..."
::: "F:\Whatever\Path\stable-diffusion-webui\venv\Scripts\Python.exe"  pickle_scan.py models > scan_output.txt
::: type scan_output.txt
::: pause