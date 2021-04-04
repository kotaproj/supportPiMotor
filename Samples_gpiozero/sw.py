from gpiozero import Button
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# SWのピン設定
PIN_SW1 = 5
PIN_SW2 = 6

sw_pins = {
    "sw1": PIN_SW1,
    "sw2": PIN_SW2,
}

def main():
    # SWピンを入力に設定(プルアップ設定)
    factory = PiGPIOFactory()
    btns = {}
    for key, pin in sw_pins.items():
        btns[key] = Button(pin, pull_up=True, pin_factory=factory)

    # スイッチを押している - print
    try:
        while True:
            for key, btn in btns.items():
                if btn.is_pressed:
                    # スイッチが押されている
                    print(key, "スイッチが押されている")
                else:
                    # スイッチが押されていない
                    pass
            sleep(0.10)
            # sleep(0.5)

    except KeyboardInterrupt:
        print("stop")

    return

if __name__ == "__main__":
    main()
