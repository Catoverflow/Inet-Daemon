Wireguard mesh network auto-configurator

## Requirement

ALL machine in mesh should have WAN ip currently (ipv6 not supported yet, nat-to-server/nat-to-nat is in to-do list)

## Usage

Create a github repository to store config.yml, and change the value of `git_repo` in `tools/confupdate.py` accordingly

This repo's scripts can be put anywhere you want, while wireguard files should be in /etc/wireguard, and thus daemon and setup script must run as root

### Add new peer

#### Use setup tool

> setup script under construction

#### Manual configuration

0. Before you start

    You should have:

    - a github repository contain config.yml (see `config.yml.example` for format)

1. Configure envirement

    - Install python dependencies

        `pip install -r requirements.txt`

    - Install wireguard (varies on distros)

2. Create basic config

    - Generate wg keypair in `/etc/wireguard`

        ~~~~bash
        # cd /etc/wireguard
        # wg genkey | tee privatekey | wg pubkey > publickey
        ~~~~

    - Create necessary updating config

        Pull the config from remote

        `git clone $YOUR_REPO_OF_CONFIG $LOCAL_POS`

        Create `meshconf.yml` in the same folder with `daemon.py`, this basically contains:

        ~~~~yaml
        github repo: $YOUR_USERNAME/$YOUR_REPO_OF_CONFIG
        local repo: ./$LOCAL_POS
        ~~~~

        `daemon.py` will update local wireguard config according to this

3. Update github repository

    Add the new peer's `wg publickey`/`LAN address`/`WAN address` to `config.yml` in `$LOCAL_POS`

    Push to remote

4. Set crontab in new peer

    Use crontab to start `daemon.py` periodly, which will query github for update and update local wireguard configuration & interface

    Recommand interval: 30 mins

    > `daemon.py` under construction

5. Enable IP forwarding and set firewall rules

    Set `net.ipv4.ip_forward=1` in /etc/sysctl.conf

    To aviod restarting server,

    ~~~~bash
    # sysctl -p
    # echo 1 > /proc/sys/net/ipv4/ip_forward
    ~~~~

    Allow VPN traffic

    ~~~~bash
    # iptables -A INPUT -p udp -m udp --dport $YOUR_WG_LISTEN_PORT -m conntrack --ctstate NEW -j ACCEPT
    ~~~~

    To save iptables after rebooting, use `netfilter-persistent`

    ~~~~bash
    # apt install iptables-persistent
    # systemctl enable netfilter-persistent
    # netfilter-persistent save
    ~~~~

### Check mesh status

`mesh.py` is the cli for this

> `mesh.py` under construction

> ref: [Wireguard VPN: Typical Setup](https://www.ckn.io/blog/2017/11/14/wireguard-vpn-typical-setup/)