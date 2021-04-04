from gpiozero import LED
from gpiozero import Button
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# LEDのピン設定
PIN_LED1 = 16
PIN_LED2 = 20

led_pins = {
    "1": PIN_LED1,
    "2": PIN_LED2,
}

# SWのピン設定
PIN_SW1 = 5
PIN_SW2 = 6

sw_pins = {
    "1": PIN_SW1,
    "2": PIN_SW2,
}



def main():
    # pigpio
    factory = PiGPIOFactory()

    # LED設定
    leds = {}
    for key, pin in led_pins.items():
        leds[key] = LED(pin, pin_factory=factory)

    # SWピンを入力に設定(プルアップ設定)
    btns = {}
    for key, pin in sw_pins.items():
        btns[key] = Button(pin, pull_up=True, pin_factory=factory)


    # スイッチを押している間LEDを点灯
    try:
        while True:
            for key, btn in btns.items():
                if btn.is_pressed:
                    # スイッチが押されている
                    leds[key].on()
                else:
                    # スイッチが押されていない
                    leds[key].off()
            sleep(0.10)

    except KeyboardInterrupt:
        print("stop")

    return

if __name__ == "__main__":
    main()
