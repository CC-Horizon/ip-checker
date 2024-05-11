import requests
import csv
import concurrent.futures
import re
from urllib.parse import quote

# Define a list of proxies
proxies = [
    {"username": "INSER_USERNAME", "password": "INSER_PASSWORD", "host": "192.248.189.128", "port": "9876", "output_file": "tufan_test2_loaod.csv"}
    # Add more proxies as needed
]


url = "https://ipinfo.io/ip"

# Number of requests to make per proxy
num_requests_per_proxy = 100000

# Function to validate an IP address
def is_valid_ip(ip):
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return re.match(ip_pattern, ip)

# Function to fetch IP and write to CSV
def fetch_ip_and_write(proxy, output_file):
    proxy_url = f"http://{quote(proxy['username'])}:{quote(proxy['password'])}@{proxy['host']}:{proxy['port']}"
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        try:
            response = requests.get(url, proxies={"http": proxy_url, "https": proxy_url})
            if response.status_code == 200:
                ip = response.text.strip()
                if is_valid_ip(ip):
                    writer.writerow([ip])
                    # Modified print statement to include the output file name
                    print(f"IP Fetched: {ip} - {output_file}")
                else:
                    print(f"Invalid IP received: {ip}")
            else:
                print(f"Failed to get IP information. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to make requests using a specific proxy
def make_requests(proxy):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(fetch_ip_and_write, proxy, proxy['output_file']) for _ in range(num_requests_per_proxy)]
        for future in concurrent.futures.as_completed(futures):
            pass
    print(f"Requests completed for proxy {proxy['host']}")

# Launch requests for each proxy in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies)) as executor:
    executor.map(make_requests, proxies)
