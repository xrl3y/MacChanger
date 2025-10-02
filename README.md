# Change MAC (Python)

Python tool to **change the MAC address** of a network interface from the terminal. It validates parameters, brings the interface down, applies the new MAC, and brings it back up. Ideal for network testing, privacy, and lab experiments.

---

## ✨ Features
- Clear CLI with `argparse`
- Interface and MAC validation using **regular expressions**
- Colored messages (using `termcolor`)
- Simple use of `ifconfig` (with a note for `ip` on modern systems)
- Easy-to-understand success/error output

---

## 📦 Requirements
- Linux (tested on common distributions)
- Python 3.7+
- System packages:
  - `net-tools` (for `ifconfig`) **or** `iproute2` utilities (if you prefer `ip`) (optional)
- Python packages:
  - `termcolor`
  - `subprocess`
  - `argparse`
  - `re`

---

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/xrl3y/MacChanger
cd MacChanger
python3 macchanger.py
```

---

## ▶️ Usage

```bash
usage: change_mac.py [-h] -i INTERFACE -m MAC

Tool to change the MAC address of a network interface

options:
  -h, --help            show this help message and exit
  -i, --interface       Network interface name (e.g., eth0, wlan0, enp3s0)
  -m, --mac             New MAC address (format: XX:XX:XX:XX:XX:XX)
```

---

## Examples

```bash
# Show help
python3 change_mac.py -h
```

# Change the MAC (requires privileges)

```bash
sudo python3 change_mac.py -i ens33 -m 12:34:56:78:9A:BC
```

---

## 🧠 How does it work?
Argument parsing with argparse (-i/--interface and -m/--mac).

Validation:

- Interface: basic pattern to avoid invalid names.
- MAC: exact format XX:XX:XX:XX:XX:XX in hex.

Applying the change (via subprocess.run):

```bash
ifconfig <iface> down

ifconfig <iface> hw ether <mac>

ifconfig <iface> up
```

- Colored success/error messages (termcolor.colored).

---

## ⚠️ Disclaimer

This tool is for educational and testing purposes only. Use it only on networks and devices where you have explicit authorization. The authors are not responsible for misuse.

---

## Author

This project was developed by **xrl3y**.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
