from queue import Queue
import threading
import time
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from icecream import ic

# SG90のピン設定
SERVO_LEFT_PIN = 17  # SG90-1
SERVO_RIGHT_PIN = 27  # SG90-2

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90       # 180 : +90degree

LEFT_OFFSET = 0
RIGHT_OFFSET = 0

servo_pis = {
    "left": SERVO_LEFT_PIN,
    "right": SERVO_RIGHT_PIN,
}


class ServoThread(threading.Thread):
    """
    サーボ管理
    例:
    queue経由で、{"type":"servo", "name": "right", "action": "raise/down/swing"}
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._rcv_que = Queue()
        self._servo = {}
        factory = PiGPIOFactory()
        for key, pin in servo_pis.items():
            self._servo[key] = AngularServo(pin, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)
        return

    def stop(self):
        self.stop_event.set()
        return


    def run(self):
        while True:
            item = self.rcv_que.get()
            ic("[servo_th]", "run : get : ", item)
            
            if "servo" not in item["type"]:
                ic("[servo_th]", "error!")
                continue
            self._recvice(item)
        return

    @property
    def rcv_que(self):
        return self._rcv_que
    
    def _recvice(self, item):
        name = item["name"]
        action = item["action"]
        if action in ["raise", "down"]:
            deg = 90 if action == "raise" else -90
            self._servo[name].angle = self._cal_degree(name, deg)
        elif action in ["swing"]:
            # for deg in ([45, 90] * 5):
            for deg in ([-45, 90] * 5):
                self._servo[name].angle = self._cal_degree(name, deg)
                time.sleep(0.30)
        else:
            ic("[ServoThread] - _recvice - error!!!")
        return

    def _cal_degree(self, name, degree):
        if "left" in name:
            degree *= (-1)
            offset = LEFT_OFFSET
        else:
            offset = RIGHT_OFFSET
        return degree + offset

def main():
    import time

    servo_th = ServoThread()
    servo_th.start()
    q = servo_th.rcv_que

    q.put({"type": "servo", "name": "left", "action": "raise"})
    time.sleep(2)
    q.put({"type": "servo", "name": "left", "action": "down"})
    time.sleep(2)
    q.put({"type": "servo", "name": "right", "action": "raise"})
    time.sleep(2)
    q.put({"type": "servo", "name": "right", "action": "down"})
    time.sleep(2)
    q.put({"type": "servo", "name": "left", "action": "swing"})
    time.sleep(5)
    q.put({"type": "servo", "name": "right", "action": "swing"})
    time.sleep(5)

    servo_th.stop()
   
    return

if __name__ == "__main__":
    main()
