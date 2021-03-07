from queue import Queue
import threading
import time
import pigpio
from sys_pig import SysPig
import sys
from icecream import ic

# LEDのピン設定
PIN_LED_NO1 = 16
PIN_LED_NO2 = 20

LED_DICT = {
    "no1" : PIN_LED_NO1,
    "no2" : PIN_LED_NO2,
}


class LedThread(threading.Thread):
    """
    LED管理
    例:
    queue経由で、{"name":"no1", "action":"on"}
    を取得すると、LED1を点灯
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._rcv_que = Queue()
        self._led = {}

        self._sys_pig = SysPig()
        self._pi = self._sys_pig.borrow_pigpio()
        # BCM指定, 各ピンを出力に設定
        for key in LED_DICT:
            pin = LED_DICT[key]
            self._pi.set_mode(pin, pigpio.OUTPUT)
            self._led[key] = {}
            self._led[key]["pin"] = pin
        return

    def stop(self):
        self.stop_event.set()
        # cleanup
        for key in self._led:
            pin = self._led[key]["pin"]
            self._pi.set_mode(pin, pigpio.INPUT)
        self._sys_pig.release_pigpio()
        return


    def run(self):
        while True:
            value = self.rcv_que.get()
            ic("[led_th]", value)
            
            if "led" not in value["type"]:
                ic("[led_th]", "error!!!")
                continue
            
            if value["name"] in self._led:
                name = value["name"]
                on_off = True if ("on" in value["action"]) else False
                self._write_led(name, on_off)
        return

    @property
    def rcv_que(self):
        return self._rcv_que

    def _write_led(self, name, on_off):
        gpio_logic = 1 if on_off else 0
        self._pi.write(self._led[name]["pin"], gpio_logic)
        return


def main():
    import time

    led_th = LedThread()
    led_th.start()
    q = led_th.rcv_que

    q.put({"type": "led", "name": "no1", "action": "on"})
    time.sleep(3)
    q.put({"type": "led", "name": "no1", "action": "off"})
    time.sleep(1)
    q.put({"type": "led", "name": "no2", "action": "on"})
    time.sleep(3)
    q.put({"type": "led", "name": "no2", "action": "off"})
    time.sleep(1)

    led_th.stop()
   
    return

if __name__ == "__main__":
    main()