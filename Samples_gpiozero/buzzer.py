from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# BUZZERのピン設定
BUZZER_PIN = 21

buzzer_pins = {
    "0": BUZZER_PIN,
}

def main():
    # 各ピンをPWM設定
    factory = PiGPIOFactory()
    buzzers = {}
    for key, pin in buzzer_pins.items():
        buzzers[key] = PWMLED(pin, pin_factory=PiGPIOFactory())

    # 音を鳴らす
    try:
        for _ in range(5):
            for key, buzzer in buzzers.items():
                buzzer.frequency = 1000
                buzzer.value = 0.5
                sleep(0.5)
                buzzer.value = 0.0
                sleep(0.5)
    except KeyboardInterrupt:
        print("stop")

    # Mute
    buzzer.value = 0.0
    buzzer.frequency = 100
    return

if __name__ == "__main__":
    main()
