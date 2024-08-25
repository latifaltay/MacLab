# Network Security Tool

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

Network Security Tool is a powerful and versatile Python script designed to help network administrators and cybersecurity enthusiasts perform various tasks such as MAC address manipulation, network interface management, IP address scanning, and TCP packet crafting for penetration testing purposes. This tool is particularly useful for ethical hackers who want to test network vulnerabilities and strengthen security measures.

## Features

- **MAC Address Manipulation:** Change the MAC address of network interfaces to anonymize your presence on a network.
- **TCP Packet Generation:** Craft and send custom TCP packets to test network defenses.
- **Network Interface Management:** List and reset network interfaces with ease.
- **IP Scanning:** Identify live IP addresses within a specified network range.
- **Interactive Command-Line Interface:** User-friendly CLI for easy navigation and operation.

## Prerequisites

Before running this script, ensure you have the following dependencies installed:

- Python 3.x
- Scapy
- ipaddress module (usually included with Python 3.x)

To install the required Python packages, run:

```bash 
- pip install -r requirements.txt 
```

## Usage

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/network-security-tool.git
cd network-security-tool

Main Menu Options
List interfaces and change MAC address: Select a network interface and assign a random MAC address.
Perform Attack: Generate and send custom TCP packets to a target IP address.
List and select target IP addresses: Scan a specified network range to find live IP addresses.
Reset network interfaces: Restart a selected network interface.
Exit: Close the tool.
Example Use Cases
MAC Address Change:

Select the "List interfaces and change MAC address" option.
Choose a network interface from the list.
The tool will automatically generate and assign a new MAC address to the selected interface.
Performing a TCP Flood Attack:

Choose the "Perform Attack" option.
Enter the target IP address.
Specify the number of packets to send.
Select the network interface to use.
The tool will generate and send the packets to the target IP.
Network Scanning:

Select the "List and select target IP addresses" option.
Enter the network range (e.g., 192.168.1.0/24).
The tool will scan and display live IP addresses within the range.
Note
This tool is intended for educational and ethical hacking purposes only. Use responsibly and always obtain proper authorization before testing any network.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Authors
Dr. Gokhan Akin - Initial Work
Latif Altay - Contributor
Disclaimer
The author(s) of this tool are not responsible for any misuse or damage caused by the improper use of this tool. It is solely intended for educational purposes and should only be used in a lawful manner.
