import time
import pigpio

# LEDのピン設定
PIN_RED_LED = 16
PIN_BLUE_LED = 20

LED_DICT = {
    "red": PIN_RED_LED,
    "blue": PIN_BLUE_LED,
}

# SWのピン設定
PIN_RED_SW = 5
PIN_BLUE_SW = 6

SW_DICT = {
    "red": PIN_RED_SW,
    "blue": PIN_BLUE_SW,
}


def main():
    # 初期化
    pi = pigpio.pi()

    # LEDピンを出力に設定
    for pin in LED_DICT.values():
        pi.set_mode(pin, pigpio.OUTPUT)
    # SWピンを入力に設定(プルアップ設定)
    for pin in SW_DICT.values():
        pi.set_mode(pin, pigpio.INPUT)
        pi.set_pull_up_down(pin, pigpio.PUD_UP)

    # スイッチを押している間LEDを点灯
    try:
        while True:
            for key in SW_DICT:
                if pi.read(SW_DICT[key]) == 0:
                    # スイッチが押されている
                    pi.write(LED_DICT[key], 1)
                else:
                    # スイッチが押されていない
                    pi.write(LED_DICT[key], 0)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("stop")

    # 片づけ
    for pin in LED_DICT.values():
        pi.set_mode(pin, pigpio.INPUT)
    for pin in SW_DICT.values():
        pi.set_mode(pin, pigpio.INPUT)
    pi.stop()


if __name__ == "__main__":
    main()
