# [WIP] PyRayhunter 
Automated bulk data extraction and maintenance tool for [EFF's Rayhunter](https://github.com/EFForg/rayhunter) (usb-only)

**Note**: I am in no way affiliated with the EFF or with the Rayhunter project. I just think it's neat.

**Note**: This is a work in progress. Currently this tool only supports bulk PCAP and QMDL file downloads via the HTTP API. The Rayhunter HTTP API should be mapped to localhost using `adb forward tcp:8080 tcp:8000` prior to running file download commands. Still works faster than clicking each download link individually in the HTTP API, and it does its best to keep things organized.

## Usage

1. Create a virtual environment: `python3 venv env.rayhunter`
2. Activate the virtual environment: `source env.rayhunter/bin/activate`
3. Install dependencies: `python3 -m pip install -r requirements.txt`
4. Run the script, providing the `--list` or `--device <device_id>` flags with the actions you'd like to execute

See the output of `--help` below for more information on supported actions (current and planned).

```
usage: python3 rayhunter.py [-h] [-o OUTPUT] [-l] [-c] [-d DEVICE] [-n] [-p] [-q] [-a]

Automated bulk data extraction and maintentance tool for Rayhunter (usb-only)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to write data (default: /home/user/rayhunter)
  -l, --list            List connected USB devices and exit.
  -c, --cleanup         Remove all analysis files using ADB to free up disk space
  -d DEVICE, --device DEVICE
                        Perform actions against this device
  -n, --ndjson          Extract NDJSON files using ADB
  -p, --pcap            Extract PCAP files using the Rayhunter API
  -q, --qmdl            Extract QMDL files using the Rayhunter API
  -a, --all             Execute all extraction and cleanup actions against target device
```

## Caveats

I'm using this tool to help me learn more about Rayhunter and to develop tooling around LTE analysis. It's subject to change at a whim and it very definitely should not be relied upon in high risk situations.