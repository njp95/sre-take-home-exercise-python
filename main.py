import yaml
import requests
import time
import json
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    sub = url.split("//")[-1].split("/")[1]
    protocol = url.split("//")[0]
    url = protocol + "//" + url.split("//")[-1].split("/")[0].split(":")[0] + "/" + sub
    method = "GET" if endpoint.get('method') is None else endpoint.get('method')
    headers = "" if endpoint.get('headers') is None else endpoint.get('headers')
    body = "" if endpoint.get('body') is None else json.loads(endpoint.get('body'))

    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=.5)
        if 200 <= response.status_code < 300:
            print(f"{url} is available")
            return "UP"
        else:
            print(f"{url} is not available due to request timeout")
            return "DOWN"
    except requests.RequestException:
        print(f"{url} is not available due to a bad request")
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]
            result=check_health(endpoint)
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")