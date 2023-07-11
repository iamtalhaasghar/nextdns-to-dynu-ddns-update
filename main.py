
import os, requests
from dotenv import load_dotenv

if not load_dotenv():
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

print(f'Setting ddns ip to: {client_ip}')

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

print(f'Finished Request with:', response.status_code)
print(response.json())

