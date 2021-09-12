# setup script for new instance
# under construction
if [ "$EUID" -ne 0 ]
  then echo "This script need to run as root"
  exit
fi
pip install -r requirements.txt
cwd = $(pwd)
cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey
echo "
-
  WGpubkey: $(cat publickey)
  WANaddr: $(curl -4 icanhazip.com)
  LANaddr: $1
  WGport: $2
" >> "$cwd/config.yml"
#cd "$cwd"
#git config set user.name ustclug
#git config set user.email noreply@ustclug.org
#git add config.yml
#git commit -m 'new peer added'
#git push