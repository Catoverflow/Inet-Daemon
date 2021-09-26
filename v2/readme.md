# Inet Daemon Version 2

## Dependencies

python3 wireguard-tools bird
## Details

Set up WireGuard tunnel as basis of OSPF overlay.
## Steps

1. Get keypair for this device

    Add the public key to remote config

2. Run `python setup.py ${github repo} $(this_device_uuid) $(wireguard_privatekey_in_string)`

    Details:

    1. Config will be fetched to local

    2. Setup WireGuard interface according to the config

    3. Bird runs OSPF and generates routing rules

3. Add daemon to crontab

    Detailss:

    1. Daemon will run periodly to download and renew config

    2. WireGuard tunnel and bird OSPF will update accordingly

4. Add new device to config (refer to config example.yml)

The config should be placed in github repo's root directory
## Todos

- Add internet access routing support (edge AS routing)