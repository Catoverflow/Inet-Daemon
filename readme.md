Wireguard mesh network auto-configurator

## Requirement

ALL machine in mesh should have WAN ip currently(ipv6 not supported yet, nat-to-server/nat-to-nat is in to-do list)

## Usage

Create a github repository to store config.yml, and change the value of `git_repo` in tools/confupdate.py accordingly

### Add new peer

#### Use setup tool

> setup script under construction

#### Manual configure

0. Configure envirement

    Install python dependencies

    `pip install -r requirements.txt`

    Install wireguard (vary on distros)

1. Generate wg keypair in /etc/wireguard

    ~~~~bash
    # cd /etc/wireguard
    # wg genkey | tee server_private_key | wg pubkey > server_public_key
    ~~~~

2. Update github repository

    Add the new peer's `wg publickey`/`LAN address`/`WAN address` to `config.yml` in github repository (which `git_repo` specifies)

    Push to remote

3. Set crontab in new peer

    Use crontab to start `daemon.py` periodly, which will query github for update and generate new wireguard config

    Recommand interval: 30 mins

    > `daemon.py` under construction

### Check mesh status

`mesh.py` is the cli for this

> `mesh.py` under construction