#!/usr/bin/python
# cli for mesh network
# todo: connectivity query

from yaml import load
import argparse

parser = argparse.ArgumentParser(description='Mesh subnet controller')
parser.add_argument('command',type=str,default='status')

def status(path='./config.yml'):
    try:
        f = open(path, encoding='UTF-8')
    except:
        print(f'config {path} not found')
        exit(1)
    conf = load(f)
    pass

if __name__ == '__main__':
    args = parser.parse_args()
    pass