# Inet Daemon Version 2

## Details

Running babeld over established wireguard tunnels.

Wireguard only used as inet-tunnel creator, ip route is handled by babled.

Established tunnels MUST be an strongly connected directed graph

##Steps

1. Add new device to config.yml (refer to config example.yml)

The config should be placed in github repo's root directory

2. Run `init ${github repo}`

    Details:

    1. Config will be fetched to local

    2. Wireguard configuration will be generated according to the config

    3. Wireguard interface set up

    4. Babled runs and generates routing rules

3. Add daemon to crontab

    DetailsL

    1. Daemon will run periodly

    2. Daemon call github REST API to check the config repo's update status

    3. If repo updates, new config will be pulled

    4. Wireguard interface will be updated

    5. Babled will run and update routing rules accordingly

## Todos

- Add internet access routing support

- Add babelWeb (optional)