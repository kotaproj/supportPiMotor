from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

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


def cal_degree(name, degree):
    if "left" in name:
        degree *= (-1)
        offset = LEFT_OFFSET
    else:
        offset = RIGHT_OFFSET
    return degree + offset

def main():
    # 初期化
    factory = PiGPIOFactory()
    servos = {}
    for key, pin in servo_pis.items():
        servos[key] = AngularServo(pin, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)

    # SG90を 30度 <-> 90度で角度を変える
    try:
        for _ in range(5):
            for name, pin in servos.items():
                print(name, "arm - ", "30degree")
                servos[name].angle = cal_degree(name, 30)
                sleep(1.0)

                print(name, "arm - ", "90degree")
                servos[name].angle = cal_degree(name, 90)
                sleep(1.0)
    except KeyboardInterrupt:
        print("stop")

    return

if __name__ == "__main__":
    main()