# generate new wg config after pulling from github repo
import yaml
from requests import get


class Wg_conf(object):

    def __init__(self, path='./config.yml'):
        self.get_ip()
        self.get_private_key()
        self.conf_gen()
        if self.ip == None:
            print('Err: get ip')
        if self.privkey == None:
            print('Err: read privatekey')
        if self.conf == None:
            print('Err: load config')

    def get_ip(self):

        ip_lookup = ['ipv4.icanhazip.com', 'api.ipify.org',
                     'v4.ident.me', 'ipv4bot.whatismyipaddress.com']

        ip_address = None
        for service in ip_lookup:
            try:
                ip_address = get(f'http://{service}',
                                 timeout=5).text.split('\n')[0]
                break
            except:
                pass
        self.ip = ip_address

    def get_private_key(self, wgpath='/etc/wireguard'):
        try:
            f = open(f'{wgpath}/privatekey', 'r')
            self.privkey = f.read()
        except:
            self.privkey = None

    def conf_gen(self, path='./config.yml'):
        try:
            ymlconf = yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)
            wgconf = {}
            wgconf['Peer'] = []
            for peer in ymlconf:
                if peer['WANaddr'] == self.ip:
                    wgconf['interface'] = {'Address': peer['LANaddr'], 'SaveConfig': 'true',
                                           'PrivateKey': self.privkey, 'ListenPort': peer['WGport']}
                else:
                    wgconf['peer'].append({'PublicKey': peer['WGpubkey'], 'AllowedIPs': peer['LANaddr'],
                                           'Endpoint': '{}:{}'.format(peer['WANaddr'], peer['WGport'])})
            self.conf = wgconf
        except:
            self.conf = None

    def write(self, wgconf='/etc/wireguard/wg0.conf'):
        try:
            f = open('/etc/wireguard/wg0.conf', 'w')
            f.write('[Interface]\n')
            for key in self.conf['interface']:
                f.write('{} = {}\n'.format(key, self.conf['Interface'][key]))
            for peer in self.conf['peer']:
                f.write('\n[Peer]\n')
                for key in peer:
                    f.write('{} = {}\n'.format(key, peer[key]))
        except:
            print('Err: write wgconf')


if __name__ == '__main__':
    pass
