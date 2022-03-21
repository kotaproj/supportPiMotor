from queue import Queue
import threading
import time
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import sys
from icecream import ic

from systems import SystemsData, RoboMode

# LEDのピン設定
PIN_LED_NO1 = 16
PIN_LED_NO2 = 20

LED_DICT = {
    "no1" : PIN_LED_NO1,
    "no2" : PIN_LED_NO2,
}


ROBO_MODE_DICT = {
    RoboMode.ARM : {"no1": "off", "no2": "off"},
    RoboMode.GEAR : {"no1": "off", "no2": "on"},
    RoboMode.TIMER : {"no1": "on", "no2": "off"},
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

        # system data
        self._sysdat = SystemsData()
        return

    def stop(self):
        for key in LED_DICT:
            self._write_leds_cmd(key, "off")
        self.stop_event.set()
        return


    def run(self):
        while True:
            value = self.rcv_que.get()
            ic("[led_th]", value)
            
            if "led" not in value["type"]:
                ic("[led_th]", "error!!!")
                continue
            
            # system data
            if "robo_mode" in value["action"]:
                led_onoffs = ROBO_MODE_DICT[self._sysdat.robo_mode]
                for k, v in led_onoffs.items():
                    ic(led_onoffs, k, v)
                    self._write_leds_cmd(k, v)
                continue

            # on/off
            if value["name"] in self._leds:
                name = value["name"]
                if value["action"] in ["on", "off", "blink"]:
                    self._write_leds_cmd(name, value["action"])
                else:
                    ic("[led_th]", "error!!! - action")
        return

    @property
    def rcv_que(self):
        return self._rcv_que

    def _write_leds_cmd(self, name, cmd):
        if "on" in cmd:
            self._leds[name].on()
        elif "off" in cmd:
            self._leds[name].off()
        elif "blink" in cmd:
            self._leds[name].blink()
        return

def main():
    import time

    led_th = LedThread()
    led_th.start()
    q = led_th.rcv_que

    q.put({"type": "led", "name": "no1", "action": "on"})
    time.sleep(3)
    # q.put({"type": "led", "name": "no1", "action": "off"})
    # time.sleep(1)
    # q.put({"type": "led", "name": "no2", "action": "on"})
    # time.sleep(3)
    # q.put({"type": "led", "name": "no2", "action": "off"})
    # time.sleep(1)

    q.put({"type": "led", "name": "noAll", "action": "robo_mode"})
    time.sleep(3)
    led_th.stop()
   
    return

if __name__ == "__main__":
    main()