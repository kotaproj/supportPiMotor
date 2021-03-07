from queue import Queue
import threading
import time
import pigpio
from sys_pig import SysPig

import sys
from icecream import ic

MIN_DUTY = 25
MAX_DUTY = 10000
SLOW_DUTY = MAX_DUTY * 0.5
MID_DUTY = MAX_DUTY * 0.75
FAST_DUTY = MAX_DUTY

PIN_AIN1 = 18
PIN_AIN2 = 23
PIN_BIN1 = 24
PIN_BIN2 = 13

DCM_DICT = {
    "ain1" : PIN_AIN1,
    "ain2" : PIN_AIN2,
    "bin1" : PIN_BIN1,
    "bin2" : PIN_BIN2,
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
        self._dcm = {}

        self._sys_pig = SysPig()
        self._pi = self._sys_pig.borrow_pigpio()
        for key in DCM_DICT:
            self._dcm[key] = {}
            pin = DCM_DICT[key]
            self._dcm[key]["pin"] = pin
            self._pi.set_mode(pin, pigpio.OUTPUT)
            self._pi.set_PWM_range(pin, MAX_DUTY)
            self._pi.set_PWM_dutycycle(pin, MIN_DUTY)
        return

    def stop(self):
        self.stop_event.set()
        # cleanup
        for key in self._dcm:
            pin = self._dcm[key]["pin"]
            self._pi.set_mode(pin, pigpio.INPUT)
        self._sys_pig.release_pigpio()
        return


    def run(self):
        while True:
            # time.sleep(0.050)
            item = self.rcv_que.get()
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, item)
            
            if "dcm" not in item["type"]:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "Error!!!")
                continue
            self._recvice(item)
        return

    @property
    def rcv_que(self):
        return self._rcv_que
    
    def _recvice(self, item):
        action = item["action"]
        speed = item["speed"]
        abpins = self._cal_duty_list(action, speed)
        for key, val in abpins.items():
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, key, val)
            pin = self._dcm[key]["pin"]
            self._pi.set_PWM_dutycycle(pin, val)
        return

    def _cal_duty_list(self, action, speed):
        """[A1, A2], [B1, B2]のdutyリストを返却する

        Args:
            action ([type]): [description]
            speed ([type]): [description]
        """
        if "stop" in action:
            return {
                "ain1" : MIN_DUTY,
                "ain2" : MIN_DUTY,
                "bin1" : MIN_DUTY,
                "bin2" : MIN_DUTY,
            }
        if "brake" in action:
            return {
                "ain1" : MAX_DUTY,
                "ain2" : MAX_DUTY,
                "bin1" : MAX_DUTY,
                "bin2" : MAX_DUTY,
            }

        mag = MAG_TBL[speed]
        if "forward" in action:
            return {
                "ain1" : MAX_DUTY * mag,
                "ain2" : MIN_DUTY,
                "bin1" : MAX_DUTY * mag,
                "bin2" : MIN_DUTY,
            }
        elif "back" in action:
            return {
                "ain1" : MIN_DUTY,
                "ain2" : MAX_DUTY * mag,
                "bin1" : MIN_DUTY,
                "bin2" : MAX_DUTY * mag,
            }
        elif "left" in action:
            return {
                "ain1" : MIN_DUTY,
                "ain2" : MIN_DUTY,
                "bin1" : MIN_DUTY,
                "bin2" : MAX_DUTY * mag,
            }
        elif "right" in action:
            return {
                "ain1" : MIN_DUTY,
                "ain2" : MAX_DUTY * mag,
                "bin1" : MIN_DUTY,
                "bin2" : MIN_DUTY,
            }
        ic("[dcm_th]: Error :", action)
        return None


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