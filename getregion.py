#!/usr/bin/env python3

import os
import argparse
import requests
import time
import socket
import ipaddress

def is_ip_address(host):
    """Check if the given host is a valid IP address."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False

def resolve_host(host):
    """Resolve a hostname to its IP addresses (both IPv4 and IPv6)."""
    try:
        ips = socket.getaddrinfo(host, None)
        return [ip[4][0] for ip in ips]
    except socket.gaierror:
        return []

def get_unique_hosts(configs_path, debug):
    hosts = set()
    for root, dirs, files in os.walk(configs_path):
        for file in files:
            if file.endswith('.ovpn'):
                if debug:
                    print(f"Reading file: {file}")
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        if "remote" in line and not ("random" in line or "server" in line):
                            host = line.split()[1]
                            if debug:
                                print(f"Found host: {host}")
                            if is_ip_address(host):
                                hosts.add(host)  # Directly add if it's an IP
                            else:
                                resolved_ips = resolve_host(host)
                                if debug and resolved_ips:
                                    print(f"Resolved {host} to: {', '.join(resolved_ips)}")
                                hosts.update(resolved_ips)  # Add resolved IPs
    return hosts

def fetch_region_ips(hosts, myregion, token, debug):
    match_count = 0
    matching_ips = []
    for host in hosts:
        if debug:
            print(f"Fetching IP info for host: {host}")
        try:
            response = requests.get(f"https://ipinfo.io/{host}?token={token}")
            if response.status_code == 200:
                data = response.json()
                if myregion.lower() in (data.get("region", "").lower(), data.get("timezone", "").lower()):
                    matching_ips.append(data['ip'])
                    match_count += 1
                    if debug:
                        print(f"Matched IP: {data['ip']}")
            else:
                if debug:
                    print(f"Failed to fetch IP info for {host}, status code: {response.status_code}")
            time.sleep(1)  # Respectful pause to avoid hitting rate limits
        except Exception as e:
            print(f"Error fetching IP info for {host}: {e}")

    if match_count == 0:
        print(f"No IPs matched the requested region: {myregion}")
    return matching_ips

def write_files(matching_ips, region_ips_path, ovpn_remotes_path, debug):
    if matching_ips:
        with open(region_ips_path, 'w') as region_file, open(ovpn_remotes_path, 'w') as remotes_file:
            for ip in matching_ips:
                region_file.write(ip + '\n')
                remotes_file.write(f"remote {ip.strip()};\n")
                if debug:
                    print(f"Added remote entry for IP: {ip.strip()}")
    else:
        if debug:
            print("No matching IPs found; not writing files.")

def main():
    parser = argparse.ArgumentParser(description='Fetch OpenVPN server IPs based on region from multiple configs and for use in single config.')
    parser.add_argument('--configdir', required=True, help='Directory containing OpenVPN .ovpn configuration files')
    parser.add_argument('--region', default='America/Los_Angeles', help='Region to filter the IPs (default: America/Los_Angeles)')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled")

    home = os.path.expanduser('~')
    region_ips_path = os.path.join(home, "Downloads/regionips.txt")
    ovpn_remotes_path = os.path.join(home, "Downloads/ovpnremotes.txt")

    # Get unique hosts and resolve non-IP hostnames
    hosts = get_unique_hosts(args.configdir, args.debug)

    # Fetch region IPs
    token = ""  # Replace with your actual token
    matching_ips = fetch_region_ips(hosts, args.region, token, args.debug)

    # Write to files if there are matching IPs
    write_files(matching_ips, region_ips_path, ovpn_remotes_path, args.debug)

if __name__ == "__main__":
    main()
