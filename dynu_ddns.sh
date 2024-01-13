out=$(/data/data/com.termux/files/home/storage/projects/nextdns-to-dynu-ddns-update/main.py)
echo "$out"
#termux-notification -c "dynu ddns updated"
curl -d "termux: $out" ntfy.sh/dynu-nextdns-tal
