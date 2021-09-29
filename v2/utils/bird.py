
interfacetmplt = "\
        interface %interface {\n\
            cost 5;\n\
            type pointopoint;\n\
            hello 15; retransmit 2;\n\
            authentication simple;\n\
            password \"%pass\";\n\
        };\n"
class Bird(object):

    def __init__(self, ip, tunnel, passwd = 'pass'):
        self.ip = ip
        self.passwd = passwd
        self.interfaces = []
        for tun in tunnel:
            self.interfaces.append(tun[0][2])
    
    def write(self,path = '/etc/bird/bird.conf'):
        fin = open('./utils/bird_template.conf', 'r')
        conf = fin.read()
        fin.close()
        conf = conf.replace('%ip',self.ip,1)
        intconf = ""
        for interface in self.interfaces:
            intconf += interfacetmplt.replace('%interface',interface)\
                .replace('%pass',self.passwd)
        conf = conf.replace('%interface', intconf)
        fout = open(path, 'w')
        fout.write(conf)