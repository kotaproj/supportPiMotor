from queue import Queue
import threading
import time
import pigpio
from sys_pig import SysPig

# debug
import sys
from icecream import ic

# SWのピン設定
PIN_SW_NO1 = 5
PIN_SW_NO2 = 6

SW_DICT = {
    "no1" : PIN_SW_NO1,
    "no2" : PIN_SW_NO2,
}

TACK_JUDGE = [False, False, True, True]


class SwThread(threading.Thread):
    """
    タクトスイッチ管理
    """
    def __init__(self, snd_que=None):
        ic()
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._snd_que = snd_que
        self._sw = {}

        self._sys_pig = SysPig()
        self._pi = self._sys_pig.borrow_pigpio()
        # スイッチピンを入力、プルアップに設定
        for key in SW_DICT:
            pin = SW_DICT[key]
            self._pi.set_mode(pin, pigpio.INPUT)
            self._pi.set_pull_up_down(pin, pigpio.PUD_UP)
            self._sw[key] = {}
            self._sw[key]["pin"] = pin
            self._sw[key]["log"] = []
        return


    def stop(self):
        ic()
        self.stop_event.set()
        self._sys_pig.release_pigpio()
        return


    def run(self):
        ic()
        while True:
            time.sleep(0.050)
            for name in self._sw:
                if self._read_poll(name):
                    ic()
                    ic("[sw_th]", "pushed - ", name)
        return
    
    def _send_msg(self, name):
        if self._snd_que is None:
            return
        ic()
        ic("[sw_th]", "_send_msg:", name)
        self._snd_que.put({"type": "sw", "name": name})
        return

    def _read_pin_logic(self, name):
        if self._pi.read(self._sw[name]["pin"]) == 0:
            return True
        else:
            return False

    def _read_poll(self, name):
        logic = self._read_pin_logic(name)
        self._sw[name]["log"].append(logic)
        # 4回未満は未処理
        if len(self._sw[name]["log"]) < 5:
            return False

        # TASK_JUDGEと完全一致なら押した
        self._sw[name]["log"].pop(0)
        if TACK_JUDGE == self._sw[name]["log"]:
            self._send_msg(name)
            return True
        
        return False

def main():
    q = Queue()
    sw_th = SwThread(q)
    sw_th.start()
    time.sleep(10)
    sw_th.stop()
    
    while True:
        if q.empty():
            print("!!! q.empty !!!")
            break
        print(q.get())
    return

if __name__ == "__main__":
    main()