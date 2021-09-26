from requests import get
from yaml import load, SafeLoader
class conf(object):
    def __init__(self, url):
        self.conf = get(url).text
        self.data = load(self.conf, Loader=SafeLoader)

    #TODO: compare time stamp to prevent unnecessary updates