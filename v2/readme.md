# Inet Daemon Version 2

## Dependencies

`python3` `wireguard-tools` `bird`

And python packages in `requirements.txt`

## Details

Set up WireGuard tunnel as basis of OSPF, maintaining a dynamic configurable Mesh network.
## Steps

1. Get keypair for this device

    Add the public key and device info (if new) to remote config (refer to exp.yml)

2. Run `python setup.py ${github repo} $(this_device_uuid) $(wireguard_privatekey_in_string)`

    Details:

    1. Config will be fetched to local

    2. Setup WireGuard interface according to the config

    3. Bird runs OSPF and generates routing rules

3. Add daemon to crontab

    Detailss:

    1. Daemon will run periodly to download and renew config

    2. WireGuard tunnel and bird OSPF will update accordingly

The config should be placed in github repo's root directory
## Todos

- Add internet access routing support (edge AS routing)