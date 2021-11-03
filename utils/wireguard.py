from subprocess import run


class Wireguard(object):
    def __init__(self):
        self.interface = []

    def write(self, device, tunnel, privkey, uuid, path='/etc/wireguard'):
        if not uuid in device:
            print('No config found, config generation passed')
            return
        for tun in tunnel:
            #tun[1] = [opposite device id, opp port, opp interface], check exp.yml for details
            wginterface = '[Interface]\nAddress = {}\nListenPort = {}\nPrivateKey = {}\nTable = off\n'\
                .format(device[uuid]['inetIP'], tun[0][1], privkey)
            hook = "\
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o %i -j MASQUERADE\n\
PostUp = ip addr add {} peer {} dev %i\n\
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o %i -j MASQUERADE\n"\
                .format(device[uuid]['inetIP'],device[tun[1][0]]['inetIP'])
            peer = '[Peer]\nPublicKey = {}\nAllowedIPs = {}\nEndpoint = {}:{}\n'\
                .format(device[tun[1][0]]['publickey'], '0.0.0.0/0',
                        device[tun[1][0]]['destIP'], tun[1][1])
            # wireguard will drop packages with destination ip not match allowip, and also use allowip to route
            # we need wireguard accept relay packages, in this case we can set allowip to full subnet or 0.0.0.0
            # and add iptable manually
            netint = tun[0][2]
            self.interface.append(netint)
            fout = open(f'{path}/{netint}.conf', 'w')
            fout.write(wginterface+hook+peer)
            fout.close()

    def up(self):
        for netint in self.interface:
            run(['wg-quick', 'up', f'{netint}'])
        if len(self.interface) == 0:
            print("No interface configured, interface set up passed")
