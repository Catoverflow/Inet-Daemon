from requests import get
from yaml import load, SafeLoader, dump
class Config(object):
    class Tunnel(object):
        def __init__(self, tunnel):
            self.tunnels = tunnel

        # get tunnel connected to specific device
        def filter(self, uuid):
            tunnel = []
            for tun in self.tunnels:
                if tun[0][0] == uuid:
                    tunnel.append(tun)
                elif tun[1][0] == uuid:
                    tunnel.append([tun[1],tun[0]])
            return tunnel

    class Device(object):
        def __init__(self, device):
            self.devices = device

    def __init__(self, url, uuid):
        conf = get(url).text
        conf = load(conf, Loader=SafeLoader)
        self.tunnel = self.Tunnel(conf['tunnel']).filter(uuid)
        self.device = self.Device(conf['device']).devices
        self.hash = hash(dump(conf))
        self.uuid = uuid
    
    def write_cache(self):
        fout = open('.cache', 'w')
        cache = ''
        interface = ''
        cache += str(self.hash)
        for tun in self.tunnel:
            interface += (' '+tun[0][2])
        cache += interface
        fout.write(cache)
        fout.close()

