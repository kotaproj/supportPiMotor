from queue import Queue
import threading
import time
from time import sleep
from commands import SUBSC_DICT
from eightbitdo_zero2 import EightBitDoZero2

# debug
import sys
from icecream import ic

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
            return

        def on_down():
            self._send_msg(SUBSC_DICT["pim:motor_back"])
            return

        def off_up_or_down():
            self._send_msg(SUBSC_DICT["pim:motor_stop"])
            return

        def on_right():
            self._send_msg(SUBSC_DICT["pim:motor_right"])
            return

        def on_left():
            self._send_msg(SUBSC_DICT["pim:motor_left"])
            return

        def off_right_or_left():
            self._send_msg(SUBSC_DICT["pim:motor_stop"])
            return

        def on_y():
            self._send_msg(SUBSC_DICT["pim:buzzer_short"])
            return

        def off_y():
            return

        def on_x():
            self._send_msg(SUBSC_DICT["pim:oled_ip"])
            return

        def off_x():
            self._send_msg(SUBSC_DICT["pim:oled_clear"])
            return

        def on_a():
            self._send_msg(SUBSC_DICT["pim:led_no1_on"])
            return

        def off_a():
            self._send_msg(SUBSC_DICT["pim:led_no1_off"])
            return

        def on_b():
            self._send_msg(SUBSC_DICT["pim:led_no2_on"])
            return

        def off_b():
            self._send_msg(SUBSC_DICT["pim:led_no2_off"])
            return

        def on_r():
            self._send_msg(SUBSC_DICT["pim:servo_right_raise"])
            return

        def off_r():
            self._send_msg(SUBSC_DICT["pim:servo_right_down"])
            return

        def on_l():
            self._send_msg(SUBSC_DICT["pim:servo_left_raise"])
            return

        def off_l():
            self._send_msg(SUBSC_DICT["pim:servo_left_down"])
            return

        def on_start():
            return

        def off_start():
            return

        def on_select():
            return

        def off_select():
            return


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
        controller.listen()
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
