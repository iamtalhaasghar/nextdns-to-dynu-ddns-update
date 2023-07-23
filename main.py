#!/data/data/com.termux/files/home/.local/share/virtualenvs/nextdns-to-dynu-ddns-update-H6J607G5/bin/python

import os, requests
from datetime import datetime
from dotenv import load_dotenv

env_path = '/data/data/com.termux/files/home/storage/projects/nextdns-to-dynu-ddns-update/.env'
if not load_dotenv(env_path):
    print("ERR: Couldn't load .env file!")
    exit()

# Fetch latest log entry from NextDNS analytics
nextdns_api_key = os.getenv("NEXT_DNS_API_KEY")

next_dns_profile = os.getenv("NEXT_DNS_PROFILE")
analytics_url = f"https://api.nextdns.io/profiles/{next_dns_profile}/logs"
headers = {"X-Api-Key": nextdns_api_key}
params = {"limit":10, "sort": "desc"}
response = requests.get(analytics_url, headers=headers, params=params)
data = response.json()
# Extract client IP from the log entry
client_ip = data["data"][0]["clientIp"]

cache_path = os.path.join(os.path.expanduser('~'), 'dynu.txt')
if os.path.isfile(cache_path):
    old_ip = open(cache_path).read()
    if old_ip == client_ip:
        print("no change")
        exit()

#print(f'Setting ddns ip to: {client_ip}')
open(cache_path, 'w').write(client_ip)

dynu_api_key = os.getenv("DYNU_API_KEY")
dynu_dns_id = os.getenv("DYNU_DNS_ID")
dynu_dns_url = os.getenv("DYNU_DNS_URL")

url = f"https://api.dynu.com/v2/dns/{dynu_dns_id}"
headers = {
    "accept": "application/json",
    "API-Key": dynu_api_key,
    "Content-Type": "application/json"
}

data = {
    "name": dynu_dns_url,
    "group": "home",
    "ipv4Address": client_ip,
    "ipv6Address": None,
    "ttl": 120,
    "ipv4": True,
    "ipv6": True,
    "ipv4WildcardAlias": True,
    "ipv6WildcardAlias": True
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print(f"ip changed to *.{client_ip.split('.')[-1]}")
else:
    print(response.status_code, response.json())

