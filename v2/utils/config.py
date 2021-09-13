from subprocess import run
class conf(object):
    def update():
        run(['cd','conf'],shell=True)
        run(['git', 'pull', '-q'])
    def init(repo):
        run(['git','clone',repo,'confrepo'])