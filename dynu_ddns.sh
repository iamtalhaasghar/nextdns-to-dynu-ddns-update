
/data/data/com.termux/files/home/.local/share/virtualenvs/nextdns-to-dynu-ddns-update-H6J607G5/bin/python /data/data/com.termux/files/home/storage/projects/nextdns-to-dynu-ddns-update/main.py
d=$(date)
#termux-notification -c "dynu ddns updated"
curl -d "updated ddns ip on: $d from termux" ntfy.sh/dynu-nextdns-tal
