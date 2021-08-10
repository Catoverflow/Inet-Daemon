# generate new wg config by config.yml
from tools.wgconfgen import Wg_conf
from tools.confupdate import query_latest_commit, update_config

latest = query_latest_commit()
if latest == False and update_config() == True:
    wgc = Wg_conf()
    wgc.write()