import subprocess
import time
import json

time.sleep(180)

with open('./path.json') as f:
    jsn = json.load(f)

subprocess.run([jsn["env"], jsn["path"]])
