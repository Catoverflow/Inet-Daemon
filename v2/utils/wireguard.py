from subprocess import run


class wireguard(object):
    def __init__(self):
        self.interface = []

    def genconf(self, config, privkey, uuid, path='/etc/wireguard'):
        if not uuid in config['device']:
            print('No config found, config generation passed')
            return
        for tunnel in config['tunnel']:
            if uuid == tunnel[0][0]:
                end1, end2 = tunnel
            elif uuid == tunnel[1][0]:
                end2, end1 = tunnel
            else:
                continue
            device = config['device']
            oppid = end2[0]
            wginterface = '[Interface]\nAddress = {}\nListenPort = {}\nPrivateKey = {}\nTable = off\n'\
                .format(device[uuid]['inetIP'], end1[1], privkey)
            hook = "PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o {} -j MASQUERADE\n\
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o {} -j MASQUERADE\n"\
                .format(end1[2], end1[2])
            peer = '[Peer]\nPublicKey = {}\nAllowedIPs = {}\nEndpoint = {}:{}\n'\
                .format(device[oppid]['publickey'], device[oppid]['inetIP'],
                        device[oppid]['destIP'], end2[1])
            netint = end1[2]
            self.interface.append(netint)
            fout = open(f'{path}/{netint}.conf', 'w')
            fout.write(wginterface+hook+peer)
            fout.close()

    def up(self):
        for netint in self.interface:
            run(['wg-quick', 'up', f'{netint}'])
        if len(self.interface) == 0:
            print("No interface configured, interface set up passed")

    def down(self):
        for netint in self.interface:
            run(['wg-quick', 'down', f'{netint}'])
        if len(self.interface) == 0:
            print("No interface configured, interface set down passed")
