from utils.config import Config
from utils.wireguard import Wireguard
from utils.bird import Bird
from argparse import ArgumentParser
from os import getcwd
from subprocess import run

parser = ArgumentParser()
parser.add_argument('addr', metavar='URL', type=str, help='Config address in url')
parser.add_argument('id', metavar='UUID',type=str, help='Unique ID for this device')
parser.add_argument('privkey', metavar='wgkey',type=str, help=\
    'WireGuard private key for this device, must corresponding to publickey in config')

if __name__ == '__main__':
    args=parser.parse_args()
    caddr, uuid, privkey = args.addr, args.id, args.privkey
    print('Getting config...')
    config = Config(caddr)
    config.write_cache()
    print('Generating wireguard configuration...')
    wg = Wireguard()
    wg.write(config.device,config.tunnel,privkey,uuid)
    print('Setting up wireguard interface...')
    wg.up()
    print('Wireguard tunnel established.')
    print('Setting up bird OSPF daemon...')
    bd = Bird(config.device[uuid]['inetIP'],config.tunnel)
    print('Bird daemon set.')
    print('Adding daemon script to systemd...')
    fin = open('utils/meshinet.services','r')
    service = fin.read().replace('%a', f'{getcwd()}/daemon.py {caddr} {uuid} {privkey}')
    fin.close()
    fout = open('/etc/systemd/system/inetdaemon.service', 'w')
    fout.write(service)
    fout.close()
    print('Daemon script added as inetdaemon.service.')
    print('Adding systemd timer...')
    run(['cp','utils/meshinet.timer','/etc/systemd/system/'])
    run(['systemctl', 'enable', 'meshinet.timer'])
    print('Set up completed.')