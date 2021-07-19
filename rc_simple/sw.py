from queue import Queue
import threading
import time
from gpiozero import Button
from gpiozero.pins.pigpio import PiGPIOFactory

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
        self._sws = {}
        factory = PiGPIOFactory()
        for key, pin in SW_DICT.items():
            self._sws[key] = Button(pin, pull_up=True, pin_factory=factory)
        return


    def stop(self):
        ic()
        self.stop_event.set()
        for sw in self._sws.values():
            sw.close()
        return


    def run(self):
        ic()
        def press_no1():
            self._send_msg("no1", "pressed")

        def release_no1():
            self._send_msg("no1", "released")

        def press_no2():
            self._send_msg("no2", "pressed")

        def release_no2():
            self._send_msg("no2", "released")

        self._sws["no1"].when_pressed = press_no1
        self._sws["no1"].when_released = release_no1
        self._sws["no2"].when_pressed = press_no2
        self._sws["no2"].when_released = release_no2

        while True:
            time.sleep(1.0)
        return
    
    def _send_msg(self, name, action):
        if self._snd_que is None:
            return
        ic()
        ic("[sw_th]", "_send_msg:", name)
        self._snd_que.put({"type": "sw", "name": name, "action":action})
        return

def main():
    q = Queue()
    sw_th = SwThread(q)
    sw_th.start()
    time.sleep(3)
    sw_th.stop()
    
    while True:
        if q.empty():
            print("!!! q.empty !!!")
            break
        print(q.get())
    return

if __name__ == "__main__":
    main()