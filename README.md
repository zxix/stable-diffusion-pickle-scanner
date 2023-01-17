# Stable Diffusion Pickle Scanner

Scan `.pt`, `.ckpt` and `.bin` files for potentially malicious code.

## How to use

1. Export `pickle_inspector.py` and `pickle_scan.py` to your Stable Diffusion base directory
2. Open bash / CMD
3. Run command `python pickle_scan.py models > scan_output.txt`
4. Open `scan_output.txt`

If you get an error about torch not being installed, start your webui and copy the venv python path and replace `python` with that path. 

> It might look something like this:
>
> `venv "F:\Projects\stable-diffusion-webui\venv\Scripts\Python.exe"`
>
> Final command would look like:
>
> `"F:\Projects\stable-diffusion-webui\venv\Scripts\Python.exe" pickle_scan.py models > scan_output.txt`

## Usage

```shell
python pickle_scan.py [directory] [debugmode]
```

Example

```shell
python pickle_scan.py models
```

## Debug Mode

Add `1` after directory to see which calls / signals triggered the scan failure.

```
python pickle_scan.py models 1 > scan_output.txt
```

## How to set up and use with AUTOMATIC1111 web UI (Windows)

1. Download the three files `pickle_inspector.py`, `pickle_scan.py` and `_start-pickle-scan.cmd` to any directory
2. Open `_start-pickle-scan.cmd` with notepad (or any text editor)
3. Copy your venv path between the quotation marks in the line starting with `SET VENV_PATH=`. When you start the UI this should be displayed in the first line of the console window. Example *venv "**E:\stable-diffusion-webui\venv\Scripts\Python.exe**"*
4. Copy the path to your model folder between the quotation marks in the line starting with `SET SD_FOLDER=`. Example *E:\stable-diffusion-webui\models*
5. (optional) If yo would like to scan an additional folder you can copy the path between the quotation marks in the line starting with `SET DOWNLOAD_FOLDER`. In case you want to scan a checkpoint before moving it into the proper model folder, otherwise leave as is
6. Save the script file
7. Doubleclick `_start-pickle-scan.cmd` and wait for the scan to complete
The last few lines show how many suspicious files were found
```shell
"Number of failed scans (potentially malicious files):"

---------- SCAN_OUTPUT.TXT: 0
```

Example output (with `numpy` considered "non-standard"):

![Code_-_Insiders_Db9qYRswOQ](https://user-images.githubusercontent.com/114846827/200138825-777e4e43-67c0-44cb-b5a7-80ee141ceb7c.png)

## Notes

By default this will scan all subdirectories for files ending with `.pt`, `.ckpt` and `.bin`

## License

https://creativecommons.org/licenses/by-nc-sa/4.0/
