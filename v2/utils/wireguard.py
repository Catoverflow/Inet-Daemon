class wireguard(object):
    def __init__(self):
        self.interface = []
    def run():
        pass
    def genconf(self,config,privkey,uuid):
        config=config['device']
        wginterface='[Interface]\nListenPort = {}\nPrivateKey = {}\nTable = off\n'\
            .format(config[uuid]['wireguard']['port'],privkey)
        for tunnel in config[uuid]['wireguard']['tunnel']:
            deviceid = tunnel['device']
            peer='[Peer]\nPublicKey = {}\nAllowedIPs = {}\nEndpoint = {}:{}'\
                .format(config[deviceid]['wireguard']['publickey'],config[deviceid]['inetIP'],
                config[deviceid]['destIP'],config[deviceid]['wireguard']['port'])
            netint = tunnel['interface']
            self.interface.append(netint)
            fout = open(f'{netint}.conf','w')
            fout.write(wginterface)
            fout.write(peer)
            fout.close()

if __name__ == '__main__':
    wireguard.genconf()