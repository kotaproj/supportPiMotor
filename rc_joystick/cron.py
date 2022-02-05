import subprocess
import time

time.sleep(180)

subprocess.run(['/home/pi/PyEnv/env_yrobo/bin/python', '/home/pi/kotap/supportPiMotor/rc_joystick/main.py'])
