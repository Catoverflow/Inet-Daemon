from utils.config import conf
from utils.wireguard import wireguard
from subprocess import run
from argparse import ArgumentParser
from yaml import load, SafeLoader

parser = ArgumentParser()
parser.add_argument('addr', metavar='URL', type=str, help='Remote git repository address in url')
parser.add_argument('id', metavar='UUID',type=str,help='Unique ID for this device')

if __name__ == '__main__':
    args=parser.parse_args()
    repo = args.addr
    uuid = args.id
    print('Cloning remote repository...')
    conf.init(repo)
    print('Loading config...')
    fin=open('confrepo/config.yml','r')
    data=load(fin,Loader=SafeLoader)
    fin.close()
    print('Generating wireguard keypairs...')
    fout=open('wgprivkey','w')
    privkey = run(['wg','genkey'],capture_output=True).stdout.decode('utf-8').strip()
    fout.write(privkey)
    fout.close()
    fout=open('wgpubkey','w')
    fin=open('wgprivkey','r')
    pubkey = run(['wg','pubkey'],stdin=fin,capture_output=True).stdout.decode('utf-8').strip()
    fout.write(pubkey)
    fout.close()
    fin.close()
    print('Wireguard keys saved at wgprivkey, wgpubkey.')
    print('Generating wireguard configuration...')
    wg = wireguard()
    wg.genconf(data,privkey,uuid)
    print('Setting up wireguard interface...')
    #for interface in wg.interface:
    #    run([f'wg-quick','up','./{interface}.conf'])
    print('Wireguard tunnel established.')