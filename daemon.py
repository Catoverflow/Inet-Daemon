#!/usr/bin/python
# daemon service, update config from github repo

import os
import json
import requests
import datetime

git_repo = 'user/repo'
interval = 30  # commits in interval seconds will be ignored


def get_uid():
    try:
        uid = os.popen('id').read()
        uid = int(uid.split('=')[1].split('(')[0])
    except:
        uid = None
    return uid

def query_latest_commit():
    url = f'https://api.github.com/repos/{git_repo}/commits'
    r = requests.get(url=url, headers={
                     'Accept': 'application/vnd.github.v3+json'}, params={'per_page': 1})
    r.encoding = 'utf-8'
    if r.status_code != 200:
        return None
    content = json.loads(r.content)
    try:
        commit_time = content[0]['commit']['committer']['date']
    except:
        return None
    # both is set to UTC +0
    time_now = datetime.datetime.utcnow()
    commit_time = datetime.datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')
    delta = (time_now-commit_time).total_seconds()
    if delta > interval:
        return True
    else:
        return False

def update_config():
    os.chdir('/etc/mesh')
    return_code = os.popen('git pull -q')
    if return_code != 0:
        return False
    else:
        return True

if __name__ == '__main__':
    uid = get_uid()
    if uid != 0: #non-root
        exit(1)
    commit = query_latest_commit()
    if commit == None:
        exit(2)
    if commit == True:
        update_res = update_config()
        if update_res != 0:
            exit(3)