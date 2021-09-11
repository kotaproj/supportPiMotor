from queue import Queue
import threading
import time

from gpiozero import Motor
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

import sys
from icecream import ic

PIN_AIN1 = 18
PIN_AIN2 = 23
PIN_BIN1 = 24
PIN_BIN2 = 13

dcm_pins = {
    "left_forward": PIN_AIN2,
    "left_backward": PIN_AIN1,
    "right_forward": PIN_BIN2,
    "right_backward": PIN_BIN1,
}

MAG_TBL = {
    "slow" : 0.5,
    "mid" : 0.75,
    "fast" : 1.0,
}

class DcmThread(threading.Thread):
    """
    サーボ管理
    例:
    queue経由で、{'action': 'right', 'speed': 'fast', 'type': 'dcm'}
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._rcv_que = Queue()

        factory = PiGPIOFactory()
        self._motor_left = Motor( forward=dcm_pins["left_forward"],
                            backward=dcm_pins["left_backward"],
                            pin_factory=factory)
        self._motor_right = Motor( forward=dcm_pins["right_forward"],
                            backward=dcm_pins["right_backward"],
                            pin_factory=factory)
        return

    def stop(self):
        self.stop_event.set()
        self._motor_left.value = 0.0
        self._motor_right.value = 0.0
        return


    def run(self):
        while True:
            item = self.rcv_que.get()
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, item)
            
            if "dcm" not in item["type"]:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "Error!!!")
                continue

            action = item["action"]
            mag = MAG_TBL[item["speed"]]
            if "forward" in action:
                self._motor_left.value = 1.0 * mag
                self._motor_right.value = 1.0 * mag
            elif "back" in action:
                self._motor_left.value = -1.0 * mag
                self._motor_right.value = -1.0 * mag
            elif "left" in action:
                self._motor_left.value = -1.0 * mag
                self._motor_right.value = 1.0 * mag
            elif "right" in action:
                self._motor_left.value = 1.0 * mag
                self._motor_right.value = -1.0 * mag
            else:   #"stop"
                self._motor_left.value = 0.0
                self._motor_right.value = 0.0
        return

    @property
    def rcv_que(self):
        return self._rcv_que


def main():
    import time

    dcm_th = DcmThread()
    dcm_th.start()
    q = dcm_th.rcv_que

    time.sleep(2)

    q.put({"type": "dcm", "action": "forward", "speed": "fast"})
    time.sleep(2)


    q.put({"type": "dcm", "action": "forward", "speed": "slow"})
    time.sleep(2)

    q.put({"type": "dcm", "action": "back", "speed": "fast"})
    time.sleep(2)


    q.put({"type": "dcm", "action": "left", "speed": "fast"})
    time.sleep(2)

    q.put({"type": "dcm", "action": "right", "speed": "fast"})
    time.sleep(2)

    q.put({"type": "dcm", "action": "stop", "speed": "fast"})
    time.sleep(2)

    dcm_th.stop()
   
    return

if __name__ == "__main__":
    main()
