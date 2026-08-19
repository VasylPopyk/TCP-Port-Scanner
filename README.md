# Multi-Threaded TCP Port Scanner & Banner Grabber

A lightweight Python security tool for network host discovery, port scanning, and banner grabbing. It is designed with a dual-interface architecture: a flexible command-line engine for automation and an interactive prompt wrapper for ease of use.

## Features

* **Concurrent Performance:** Utilizes `ThreadPoolExecutor` and `as_completed` streaming to scan target ports simultaneously without output delays.
* **Banner Grabbing:** Sends initial payloads upon successful connection to inspect raw service banners (e.g., SSH versions, HTTP headers).
* **Dual Execution Modes:**
  * **Module / CLI Engine (`program.py`):** Accepts argument flags (`argparse`) for headless execution and tool chaining.
  * **Interactive Launcher (`executor.py`):** Prompts the user step-by-step for inputs with safe default values.

## File Architecture

* `program.py` — Core port scanning engine and socket logic.
* `executor.py` — Interactive wrapper that imports `program.py` and passes user inputs directly to the engine.

## Installation & Prerequisites

* Requires Python 3.10+
* No external libraries needed (built entirely with Python standard libraries: `socket`, `argparse`, `concurrent.futures`).

## Usage

### 1. Interactive Mode (Recommended for quick runs)
Launch the interactive prompt to enter target options step-by-step:
```bash
python executor.py
```
### 2. Direct CLI Mode
# Basic scan using defaults (target: 127.0.0.1)
python program.py

# Custom target and scan range
python program.py 192.168.1.1 --start-port 1 --end-port 1024 --threads 100 --timeout 0.5

# Display full help menu
python program.py --help

# Sample output

[*] Starting scan on target: 127.0.0.1
[*] Scanning ports 1 through 254...

[+] Port 22    OPEN | Banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
[+] Port 80    OPEN | Banner: HTTP/1.1 400 Bad Request
[+] Port 443   OPEN | Banner: No banner returned

[*] Scan complete. Found 3 open port(s) on 127.0.0.1.