

import time
import pigpio

# BUZZERのピン設定
BUZZER_PIN = 21
FREQ = 25

BUZZER_DICT = {
    "buzzer": BUZZER_PIN,
}


def main():
    # 初期化
    pi = pigpio.pi()

    # PWM設定
    for pin in BUZZER_DICT.values():
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.set_PWM_range(pin, 40000)
        pi.set_PWM_dutycycle(pin, FREQ)

    # SG90を 3秒ビープ音を鳴らす
    try:
        pi.set_PWM_dutycycle(pin, 1000)
        time.sleep(3)
        pi.set_PWM_dutycycle(pin, FREQ)
    except KeyboardInterrupt:
        print("stop")

    # 片づけ
    for pin in BUZZER_DICT.values():
        pi.set_PWM_dutycycle(pin, FREQ)
        pi.set_mode(pin, pigpio.INPUT)
    pi.stop()


if __name__ == "__main__":
    main()
