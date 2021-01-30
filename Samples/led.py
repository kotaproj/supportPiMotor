import time
import pigpio

# LEDのピン設定
PIN_RED_LED = 16
PIN_BLUE_LED = 20

LED_DICT = {
    "red": PIN_RED_LED,
    "blue": PIN_BLUE_LED,
}


def main():
    # 初期化
    pi = pigpio.pi()

    # 各ピンを出力に設定
    for pin in LED_DICT.values():
        pi.set_mode(pin, pigpio.OUTPUT)

    # LEDをチカチカ
    try:
        for _ in range(5):
            for name, pin in LED_DICT.items():
                print("LED ON - ", name)
                pi.write(pin, 1)
                time.sleep(0.5)

                print("LED OFF - ", name)
                pi.write(pin, 0)
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("stop")

    # 片づけ
    for pin in LED_DICT.values():
        pi.set_mode(pin, pigpio.INPUT)
    pi.stop()


if __name__ == "__main__":
    main()
