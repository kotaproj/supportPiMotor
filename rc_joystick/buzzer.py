from queue import Queue
import threading
import time
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from gpiozero.pins.pigpio import PiGPIOFactory
from icecream import ic

# BUZZERのピン設定
BUZZER_PIN = 21

# Midi note: 'C4' - ド
# Midi note: 'D4' - レ
# Midi note: 'E4' - ミ
# Midi note: 'F4' - ファ
# Midi note: 'G4' - ソ
# Midi note: 'A4' - ラ
# Midi note: 'B4' - シ
# Midi note: 'C5' - ド

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
        for key, pin in BUZZER_DICT.items():
            self._buzzer[key] = TonalBuzzer(pin, pin_factory=PiGPIOFactory())
        return

    def stop(self):
        self.stop_event.set()
        # cleanup
        for key in self._buzzer:
            self._buzzer[key].stop()
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
            # item["note"] : 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'
            self._buzzer[item["name"]].play(Tone(item["note"]))
            time.sleep(ms_time)
            self._buzzer[item["name"]].stop()
        return

    @property
    def rcv_que(self):
        return self._rcv_que


def main():
    import time

    buzzer_th = BuzzerThread()
    buzzer_th.start()
    q = buzzer_th.rcv_que

    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "note": "C4"}) # do
    time.sleep(1)
    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "note": "D4"}) # re
    time.sleep(1)
    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "note": "E4"}) # mi
    time.sleep(1)
    q.put({"type": "buzzer", "name": "buzzer", "time": "500", "note": "F4"}) # fa
    time.sleep(1)

    buzzer_th.stop()
   
    return

if __name__ == "__main__":
    main()