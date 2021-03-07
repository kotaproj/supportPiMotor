from queue import Queue
import threading
import time
import pigpio
from sys_pig import SysPig
from icecream import ic

# BUZZERのピン設定
BUZZER_PIN = 21
FREQ = 100

BUZZER_DICT = {
    "buzzer" : BUZZER_PIN,
}


class BuzzerThread(threading.Thread):
    """
    ブザー管理
    例:
    queue経由で、{"type":"buzzer", "time": "300", "bfreq":"2000"}
    を取得すると、ブザー音を300msec鳴らす
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._rcv_que = Queue()
        self._buzzer = {}

        self._sys_pig = SysPig()
        self._pi = self._sys_pig.borrow_pigpio()
        for key in BUZZER_DICT:
            self._buzzer[key] = {}
            pin = BUZZER_DICT[key]
            self._buzzer[key]["pin"] = pin
            self._pi.set_mode(pin, pigpio.OUTPUT)
            self._pi.set_PWM_range(pin, 40000)
            self._pi.set_PWM_dutycycle(pin, FREQ)
        return

    def stop(self):
        self.stop_event.set()
        # cleanup
        for key in self._buzzer:
            pin = self._buzzer[key]["pin"]
            self._pi.set_PWM_dutycycle(pin, FREQ)
            self._pi.set_mode(pin, pigpio.INPUT)
        self._sys_pig.release_pigpio()
        return


    def run(self):
        while True:
            # time.sleep(0.050)
            item = self.rcv_que.get()
            ic("[buzzer_th]", "run : get : ", item)
            
            if "buzzer" not in item["type"]:
                ic("[buzzer_th]", "error!")
                continue
            
            ms_time = int(item["time"]) / 1000
            bfreq = int(item["bfreq"])
            pin = self._buzzer[item["name"]]["pin"]
            self._pi.set_PWM_dutycycle(pin, bfreq)
            time.sleep(ms_time)
            self._pi.set_PWM_dutycycle(pin, FREQ)
        return

    @property
    def rcv_que(self):
        return self._rcv_que


def main():
    import time

    buzzer_th = BuzzerThread()
    buzzer_th.start()
    q = buzzer_th.rcv_que

    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "bfreq": "10000"})
    time.sleep(1)
    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "bfreq": "15000"})
    time.sleep(1)
    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "bfreq": "20000"})
    time.sleep(1)
    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "bfreq": "25000"})
    time.sleep(1)

    buzzer_th.stop()
   
    return

if __name__ == "__main__":
    main()