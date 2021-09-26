from utils.config import conf
from utils.wireguard import wireguard
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('addr', metavar='URL', type=str, help='Config address in url')
parser.add_argument('id', metavar='UUID',type=str, help='Unique ID for this device')
parser.add_argument('privkey', metavar='wgkey',type=str, help=\
    'WireGuard private key for this device, must corresponding to publickey in config')

if __name__ == '__main__':
    args=parser.parse_args()
    caddr = args.addr
    uuid = args.id
    privkey = args.privkey
    print('Getting config...')
    config = conf(caddr)
    data = config.data
    print('Generating wireguard configuration...')
    wg = wireguard()
    wg.genconf(data,privkey,uuid)
    print('Setting up wireguard interface...')
    wg.up()
    print('Wireguard tunnel established.')