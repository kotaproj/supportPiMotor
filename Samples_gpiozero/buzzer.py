from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# BUZZERのピン設定
BUZZER_PIN = 21

buzzer_pins = {
    "0": BUZZER_PIN,
}

def main():
    # 各ピンをbuzzer設定
    factory = PiGPIOFactory()
    buzzers = {}
    for key, pin in buzzer_pins.items():
        buzzers[key] = TonalBuzzer(pin, pin_factory=PiGPIOFactory())

    # 音を鳴らす
    try:
        for _ in range(5):
            for key, buzzer in buzzers.items():

                buzzer.play(Tone("A4"))
                sleep(0.5)
                buzzer.play(Tone(220.0)) # Hz
                sleep(0.5)
                buzzer.play(Tone(60)) # middle C in MIDI notation
                sleep(0.5)
                buzzer.stop()
    except KeyboardInterrupt:
        print("stop")

    return

if __name__ == "__main__":
    main()
