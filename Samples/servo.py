import time
import pigpio

# SG90のピン設定
SERVO_LEFT_PIN = 17  # SG90-1
SERVO_RIGHT_PIN = 27  # SG90-2

MIN_DEGREE = 500        # 000 : -90degree
# MID_DEGREE = 1450     # 090 : 0degree
MAX_DEGREE = 2350       # 180 : +90degree

LEFT_OFFSET = 0
RIGHT_OFFSET = 0

SERVO_DICT = {
    "left": SERVO_LEFT_PIN,
    "right": SERVO_RIGHT_PIN,
}


def cal_degree2pulse(name, degree):
    if "left" in name:
        degree = 180 - degree
        offset = LEFT_OFFSET
    else:
        offset = RIGHT_OFFSET
    return (MAX_DEGREE - MIN_DEGREE)/180 * degree + MIN_DEGREE + offset


def main():
    # 初期化
    pi = pigpio.pi()

    # SG90を 30度 <-> 90度で角度を変える
    try:
        for _ in range(5):
            for name, pin in SERVO_DICT.items():
                print(name, "arm - ", "30degree")
                pulse = cal_degree2pulse(name, 30)
                pi.set_servo_pulsewidth(pin, pulse)
                time.sleep(1.0)

                print(name, "arm - ", "90degree")
                pulse = cal_degree2pulse(name, 90)
                pi.set_servo_pulsewidth(pin, pulse)
                time.sleep(1.0)
    except KeyboardInterrupt:
        print("stop")

    # 片づけ
    for pin in SERVO_DICT.values():
        pi.set_mode(pin, pigpio.INPUT)
    pi.stop()


if __name__ == "__main__":
    main()
