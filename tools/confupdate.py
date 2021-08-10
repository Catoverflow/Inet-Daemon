#!/usr/bin/python
# daemon service, update config from github repo

from os import popen
from yaml import load as ymload
from yaml import SafeLoader
from json import loads as jsload
from requests import get
from datetime import datetime

# rewrite needed
interval = 30  # commits in interval seconds will be ignored


def query_latest_commit():
    try:
        f = open('meshconf.yml')
        f = ymload(f, Loader=SafeLoader)
        git_repo = f['github repo']
        last_update_time = f['last update time']
        url = f'https://api.github.com/repos/{git_repo}/commits'
        r = get(url=url, headers={
            'Accept': 'application/vnd.github.v3+json'}, params={'per_page': 1}, timeout=20)
        r.encoding = 'utf-8'
        content = jsload(r.content)
        commit_time = content[0]['commit']['committer']['date']
    except:
        print('Err: get commit')
        return None
    # both is set to UTC +0
    commit_time = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')
    last_update_time = datetime.strptime(last_update_time, '%Y-%m-%d %H:%M:%S')
    delta = (last_update_time-commit_time).total_seconds()
    if delta > interval:
        return True
    else:
        return False


def update_config():
    return_code = popen('git pull -q')
    if return_code != 0:
        return False
    else:
        print('Err: git pull')
        return True


if __name__ == '__main__':
    pass
