from queue import Queue
import threading
import time
from time import sleep
from commands import SUBSC_DICT
from eightbitdo_zero2 import EightBitDoZero2
import os
from stat import filemode
import subprocess

# debug
import sys
from icecream import ic
import syslog

DEVICE_PATH = "/dev/input/js0"

class JsThread(threading.Thread):
    """
    JoyStick管理
    """
    def __init__(self, snd_que=None):
        ic()
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)
        self._snd_que = snd_que
        return


    def stop(self):
        ic()
        self.stop_event.set()
        return


    def run(self):
        ic()

        def on_up():
            self._send_msg(SUBSC_DICT["pim:motor_forward"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_up"])
            return

        def on_down():
            self._send_msg(SUBSC_DICT["pim:motor_back"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_down"])
            return

        def off_up_or_down():
            self._send_msg(SUBSC_DICT["pim:motor_stop"])
            # self._send_msg(SUBSC_DICT["pim:js0_off_up_or_down"])
            return

        def on_right():
            self._send_msg(SUBSC_DICT["pim:motor_right"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_right"])
            return

        def on_left():
            self._send_msg(SUBSC_DICT["pim:motor_left"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_left"])
            return

        def off_right_or_left():
            self._send_msg(SUBSC_DICT["pim:motor_stop"])
            # self._send_msg(SUBSC_DICT["pim:js0_off_right_or_left"])
            return

        def on_y():
            self._send_msg(SUBSC_DICT["pim:buzzer_short"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_y"])
            return

        def off_y():
            # self._send_msg(SUBSC_DICT["pim:js0_off_y"])
            return

        def on_x():
            self._send_msg(SUBSC_DICT["pim:oled_ip"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_x"])
            return

        def off_x():
            self._send_msg(SUBSC_DICT["pim:oled_clear"])
            # self._send_msg(SUBSC_DICT["pim:js0_off_x"])
            return

        def on_a():
            # self._send_msg(SUBSC_DICT["pim:led_no1_on"])
            self._send_msg(SUBSC_DICT["pim:js0_on_a"])
            return

        def off_a():
            # self._send_msg(SUBSC_DICT["pim:led_no1_off"])
            self._send_msg(SUBSC_DICT["pim:js0_off_a"])
            return

        def on_b():
            self._send_msg(SUBSC_DICT["pim:led_no2_on"])
            # self._send_msg(SUBSC_DICT["pim:js0_on_b"])
            return

        def off_b():
            self._send_msg(SUBSC_DICT["pim:led_no2_off"])
            # self._send_msg(SUBSC_DICT["pim:js0_off_b"])
            return

        def on_r():
            self._send_msg(SUBSC_DICT["pim:js0_on_r"])
            return

        def off_r():
            self._send_msg(SUBSC_DICT["pim:js0_off_r"])
            return

        def on_l():
            self._send_msg(SUBSC_DICT["pim:js0_on_l"])
            return

        def off_l():
            self._send_msg(SUBSC_DICT["pim:js0_off_l"])
            return

        def on_start():
            self._send_msg(SUBSC_DICT["pim:js0_on_start"])
            return

        def off_start():
            self._send_msg(SUBSC_DICT["pim:js0_off_start"])
            return

        def on_select():
            self._send_msg(SUBSC_DICT["pim:js0_on_select"])
            return

        def off_select():
            self._send_msg(SUBSC_DICT["pim:js0_off_select"])
            return

		# find : /dev/input/js*
        while True:
            if os.path.exists(DEVICE_PATH):
                syslog.syslog(('find:' + DEVICE_PATH))
                break
            time.sleep(1) 

        # Check permissions. - wait:crw------- -> crw-rw----
        while True:
            fmode = filemode(os.stat(DEVICE_PATH).st_mode)
            syslog.syslog(str(fmode))
            if fmode.count("r") >= 2:
                break
            time.sleep(5)

        controller = EightBitDoZero2(
            device_path=DEVICE_PATH,
            on_up=on_up,
            on_down=on_down,
            off_up_or_down=off_up_or_down,
            on_right=on_right,
            on_left=on_left,
            off_right_or_left=off_right_or_left,
            on_y=on_y,
            off_y=off_y,
            on_x=on_x,
            off_x=off_x,
            on_a=on_a,
            off_a=off_a,
            on_b=on_b,
            off_b=off_b,
            on_r=on_r,
            off_r=off_r,
            on_l=on_l,
            off_l=off_l,
            on_start=on_start,
            off_start=off_start,
            on_select=on_select,
            off_select=off_select,
        )

        # Start listen
        try:
           syslog.syslog('controller.listen')
           controller.listen()
        except Exception as e:
           syslog.syslog(('except' + str(e)))
        
        return

   
    def _send_msg(self, item):
        ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, item)
        if self._snd_que is None:
            return
        self._snd_que.put(item)
        return


def main():
    q = Queue()
    js_th = JsThread(q)
    js_th.start()
    time.sleep(60*5)
    js_th.stop()
    
    while True:
        if q.empty():
            print("!!! q.empty !!!")
            break
        print(q.get())
    return

if __name__ == "__main__":
    main()
