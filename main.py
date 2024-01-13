import os, requests
from datetime import datetime
from dotenv import load_dotenv
import sys, time
from redis import Redis

def main():
    if not load_dotenv():
        print("ERR: Couldn't load .env file!")
        exit()

    rdb = Redis(decode_responses=True)

    ntfy_url = os.getenv('NTFY_URL')
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

    rkey = '/nextdns/ip'
    old_ip = rdb.get(rkey)
    print('old ip is:', old_ip, 'new ip is:', client_ip)
    if old_ip == client_ip:
        msg = f'{os.getlogin()}: no changes'
        print(msg)
        return

    print(f'Setting ddns ip to: {client_ip}')
    rdb.set(rkey, client_ip)
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
        msg = f"{os.getlogin()}: new ip is *.{client_ip.split('.')[-1]}"
        requests.post(ntfy_url, headers={'Priority': 'high'}, json=msg)
        print(msg)
    else:
        print(response.status_code, response.json())

if __name__=='__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        time.sleep(5)
