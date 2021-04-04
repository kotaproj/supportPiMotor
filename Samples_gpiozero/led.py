from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# LEDのピン設定
PIN_LED1 = 16
PIN_LED2 = 20

led_pins = {
    "led1": PIN_LED1,
    "led2": PIN_LED2,
}

def main():
    # 各ピンをLED設定
    factory = PiGPIOFactory()
    leds = {}
    for key, pin in led_pins.items():
        leds[key] = LED(pin, pin_factory=PiGPIOFactory())

    # LEDをチカチカ
    try:
        for _ in range(5):
            for key, led in leds.items():
                print("LED ON - ", key)
                led.on()
                sleep(0.5)
                print("LED OFF - ", key)
                led.off()
                sleep(0.5)
    except KeyboardInterrupt:
        print("stop")


if __name__ == "__main__":
    main()