# Stable Diffusion Pickle Scanner

Scan `.pt`, `.ckpt` and `.bin` files for potentially malicious code.

Example output (with `numpy` considered "non-standard"):

![Code_-_Insiders_Db9qYRswOQ](https://user-images.githubusercontent.com/114846827/200138825-777e4e43-67c0-44cb-b5a7-80ee141ceb7c.png)

## How to use

1. Export `pickle_inspector.py` and `pickle_scan.py` to your Stable Diffusion WebUI base directory
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

## Notes

By default this will scan all subdirectories for files ending with `.pt`, `.ckpt` and `.bin`

## License

https://creativecommons.org/licenses/by-nc-sa/4.0/
