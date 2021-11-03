from utils.config import Config
from argparse import ArgumentParser
from subprocess import run
parser = ArgumentParser()
parser.add_argument('addr', metavar='URL', type=str, help='Config address in url')
parser.add_argument('id', metavar='UUID',type=str, help='Unique ID for this device')
parser.add_argument('privkey', metavar='wgkey',type=str, help=\
    'WireGuard private key for this device, must corresponding to publickey in config')

if __name__ == '__main__':
    args=parser.parse_args()
    caddr, uuid, privkey = args.addr, args.id, args.privkey
    try:
        fin = open('.cache', 'r')
        cache = fin.read().split(' ')
        oldhash = cache[0]
        fin.close()
    except:
        oldhash = ''
    config = Config(caddr)
    newhash = config.hash
    if newhash == oldhash:
        exit(0)
    else: #config updated
        from utils.wireguard import Wireguard
        from utils.bird import Bird

        interfaces = cache[1:]
        print('Shutting down previous wireguard interface(s)...')
        for interface in interfaces:
            run(['wg-quick', 'down', f'{interface}'])
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
        print('Renew completed.')