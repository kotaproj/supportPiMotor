from queue import Queue
import threading
import time
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
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
        self._leds = {}

        # 各ピンをLED設定
        factory = PiGPIOFactory()
        for key, pin in LED_DICT.items():
            self._leds[key] = LED(pin, pin_factory=PiGPIOFactory())
        return

    def stop(self):
        self.stop_event.set()
        return


    def run(self):
        while True:
            value = self.rcv_que.get()
            ic("[led_th]", value)
            
            if "led" not in value["type"]:
                ic("[led_th]", "error!!!")
                continue
            
            if value["name"] in self._leds:
                name = value["name"]
                on_off = True if ("on" in value["action"]) else False
                self._write_leds(name, on_off)
        return

    @property
    def rcv_que(self):
        return self._rcv_que

    def _write_leds(self, name, on_off):
        if on_off:
            self._leds[name].on()
        else:
            self._leds[name].off()
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