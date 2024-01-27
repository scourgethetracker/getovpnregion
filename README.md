# Get OpenVPN Regions

This Python script automates the process of fetching OpenVPN server IP addresses based on a specified geographical region. It parses `.ovpn` configuration files within a given directory, resolves domain names to their respective IP addresses, queries these IPs for geographical information using the `ipinfo.io` API, and generates configuration snippets suitable for OpenVPN clients.

## Features

- Parses `.ovpn` files to extract server information.
- Resolves server domain names to IP addresses.
- Filters servers based on the specified geographical region.
- Generates OpenVPN configuration snippets with servers from the desired region.
- Debug mode for detailed operation insight.

## Installation

To use this script, ensure you have Python 3 installed on your system. You will also need the `requests` library, which can be installed using pip:

```bash
pip install requests
```

Clone the repository or download the script to your local machine:

```bash
git clone https://github.com/scourgethetracker/getovpnregion.git
cd getvpnregion
```

## Usage

To run the script, you need to provide the path to the directory containing your `.ovpn` configuration files using the `--configdir` option. Optionally, you can specify the region with `--region` and enable debug mode with `--debug`.

Basic usage:

```bash
./getregion.py --configdir /path/to/your/ovpn/configs
```

Specifying a region:

```bash
./getregion.py --configdir /path/to/your/ovpn/configs --region "Europe/London"
```

Enabling debug mode:

```bash
./getregion.py --configdir /path/to/your/ovpn/configs --debug
```

## Output Files

The script generates two files in the user's `Downloads` directory:

- `regionips.txt`: Contains a list of IP addresses matching the specified region.
- `ovpnremotes.txt`: Contains OpenVPN remote entries for the matching IP addresses, ready to be included in your OpenVPN configuration.

## Note
- Replaace `YourIpInfoTokenHere` in `getregion.conf` with your own ipinfo.io API token.
- If you decide to relocate the conf file update the `load_config` in the `getregion.py` script.
- Ensure your `ipinfo.io` API token is valid and has not exceeded its rate limits.
- The script's performance and accuracy depend on the correctness of the `.ovpn` files and the availability of the `ipinfo.io` service.

