import os
import subprocess
import time
import json
import syslog

syslog.syslog('wait 60sec')
time.sleep(60)
syslog.syslog('open:path.json')

json_path = os.path.join(os.path.dirname(__file__), "path.json")
with open(json_path) as f:
    jsn = json.load(f)

syslog.syslog('run:subprocess')
subprocess.run([jsn["env"], jsn["path"]])

while True:
    time.sleep(10)