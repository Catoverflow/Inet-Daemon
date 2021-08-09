# generate new wg config after pulling from github repo
import yaml
from requests import get

ip_lookup = ['ipv4.icanhazip.com', 'api.ipify.org',
             'v4.ident.me', 'ipv4bot.whatismyipaddress.com']


def get_wan_ip():
    ip_address = None
    for service in ip_lookup:
        try:
            ip_address = get(f'http://{service}',
                             timeout=5).text.split('\n')[0]
            break
        except:
            pass
    return ip_address


def load_config(path='./config.yml'):
    try:
        conf = yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)
        return conf
    except:
        return None


def wgconf_gen(conf, selfip, selfprivkey):
    wgconf = {}
    wgconf['Peer'] = []
    try:
        for peer in conf:
            if peer['WANaddr'] == selfip:
                wgconf['Interface'] = {'Address': peer['LANaddr'], 'SaveConfig': 'true',
                                    'PrivateKey': selfprivkey, 'ListenPort': peer['WGport']}
            else:
                wgconf['peer'].append({'PublicKey': peer['WGpubkey'], 'AllowedIPs': peer['LANaddr'],
                                    'Endpoint': '{}:{}'.format(peer['WANaddr'], peer['WGport'])})
        return wgconf
    except:
        return None


def get_privatekey():
    pass

if __name__ == '__main__':
    pass
