# generate new wg config by config.yml
from tools.wgconfgen import Wg_conf

#!/usr/bin/python
# daemon service, update config from github repo

from subprocess import run
from os import chdir, getcwd
from yaml import load as ymload
from yaml import SafeLoader, dump
from json import loads as jsload
from requests import get
from datetime import datetime

# rewrite needed
interval = 30  # commits in interval seconds will be ignored

def update_conf():
    try:
        url = f'https://api.github.com/repos/{git_repo}/commits'
        r = get(url=url, headers={
            'Accept': 'application/vnd.github.v3+json'}, params={'pQer_page': 1}, timeout=20)
        r.encoding = 'utf-8'
        content = jsload(r.content)
        commit_time = content[0]['commit']['committer']['date']
        commit_time = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')

        f = open('meshconf.yml', 'r')
        data = ymload(f, Loader=SafeLoader)
        git_repo = data['github repo']
        local_repo = data['local repo']
        if 'last update' in data:
            last_update_time = data['last update']
            delta = (last_update_time-commit_time).total_seconds()
            need_update = (delta > interval)
        else:
            need_update = True
        f.close()
    except:
        print('Err: get commit')
        need_update = False
    if need_update == True:
        cwd = getcwd()
        chdir(local_repo)
        return_code = run(['git', 'pull', '-q'], capture_output=True).returncode
        if return_code != 0:
            print('Err: git pull')
            return False
        else:
            chdir(cwd)
            f = open('meshconf.yml', 'w')
            data = dump({'github repo':git_repo,'local repo':local_repo,'last update':datetime.strftime(commit_time, '%Y-%m-%d %H:%M:%S')})
            print('Config updated')
            return True


if __name__ == '__main__':
    if update_conf() == True:
        wgc = Wg_conf()
        wgc.write()