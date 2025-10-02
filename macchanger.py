#!/usr/bin/env python3
"""
Small command-line tool to change the MAC address of a network interface.

Original behavior:
- Takes an interface name (-i/--interface) and a MAC address (-m/--mac).
- Validates both with regular expressions.
- Brings the interface down, changes the MAC with ifconfig, and brings it up again.
- Prints colored success/error messages.
"""

import argparse         # For parsing command-line options and arguments
import subprocess       # To run system commands (ifconfig here)
from termcolor import colored  # To print colored messages in the terminal
import re               # For regular-expression validation


def get_arguments():
    """
    Build and parse the command-line interface.

    Returns:
        argparse.Namespace: An object with attributes 'interface' and 'mac_address'
                            corresponding to the provided arguments.
    """
    parser = argparse.ArgumentParser(
        description="Tool to change the MAC address of a network interface"
    )

    # Name of the network interface (e.g., eth0, wlan0, enp3s0). Required.
    parser.add_argument(
        "-i", "--interface",
        required=True,
        dest="interface",
        help="Network interface name (e.g., eth0, wlan0, enp3s0)"
    )

    # New MAC address to assign. Required.
    parser.add_argument(
        "-m", "--mac",
        required=True,
        dest="mac_address",
        help="New MAC address for the network interface (format: XX:XX:XX:XX:XX:XX)"
    )

    # Parse and return the arguments provided by the user
    return parser.parse_args()


def is_valid_input(interface, mac_address):
    """
    Validate the interface name and MAC address using regular expressions.

    Args:
        interface (str): Interface name supplied by the user.
        mac_address (str): MAC address supplied by the user.

    Returns:
        bool: True if both interface and MAC match the expected patterns; False otherwise.

    Notes:
        - The MAC regex is strict: six octets of hex separated by colons.
        - The interface regex is intentionally simple and may reject valid names on some distros
          (e.g., 'enp0s3', 'wlp2s0'); adjust as needed for your environment.
    """

    # --- Interface name validation ---
    # The original pattern attempts to cover common names like 'eth0', 'ens33', etc.
    # If this is too restrictive in your system, consider a looser alternative like: r'^[a-zA-Z0-9._:-]+$'
    is_valid_interface = re.match(
        r'^[e|n][t|n|l][s|h|p]\d{1,2}$',  # simplistic example based on the original code in the screenshot
        interface
    )

    # --- MAC address validation ---
    # Matches exactly 6 pairs of hexadecimal digits separated by colons.
    # Example of a valid MAC: "00:11:22:AA:BB:CC"
    is_valid_mac_address = re.match(
        r'^([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2}$',
        mac_address
    )

    # Return True only if both validations succeed
    return bool(is_valid_interface) and bool(is_valid_mac_address)


def change_mac_address(interface, mac_address):
    """
    Change the MAC address of the given network interface.

    Steps:
        1) Validate inputs (interface name and MAC format).
        2) Bring the interface DOWN.
        3) Change the hardware (ether) address with ifconfig.
        4) Bring the interface UP.
        5) Print a colored status message.

    Args:
        interface (str): The network interface to modify.
        mac_address (str): The new MAC address to set.
    """
    if is_valid_input(interface, mac_address):
        # Bring the interface down so we can modify its MAC safely
        subprocess.run(["ifconfig", interface, "down"], check=False)

        # Apply the new MAC address via ifconfig (legacy but still present on many systems)
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address], check=False)

        # Bring the interface back up so it’s usable again
        subprocess.run(["ifconfig", interface, "up"], check=False)

        print(colored("\n[+] MAC address changed successfully\n", "green"))
    else:
        print(colored("\n[!] The provided interface or MAC address is invalid\n", "red"))


def main():
    """
    Entry point:
      - Parse user arguments.
      - Attempt to change the MAC with those arguments.
    """
    args = get_arguments()
    change_mac_address(args.interface, args.mac_address)


if __name__ == "__main__":
    # Only execute main() when the script is run directly, not when imported as a module.
    main()

