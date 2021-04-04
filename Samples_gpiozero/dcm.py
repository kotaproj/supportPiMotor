from gpiozero import Motor
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

# DCモータのピン設定
PIN_AIN1 = 18
PIN_AIN2 = 23
PIN_BIN1 = 24
PIN_BIN2 = 13

dcm_pins = {
    "left_forward": PIN_AIN2,
    "left_backward": PIN_AIN1,
    "right_forward": PIN_BIN2,
    "right_backward": PIN_BIN1,
}

def main():
    # 初期化
    factory = PiGPIOFactory()
    motor_left = Motor( forward=dcm_pins["left_forward"],
                        backward=dcm_pins["left_backward"],
                        pin_factory=factory)
    motor_right = Motor( forward=dcm_pins["right_forward"],
                        backward=dcm_pins["right_backward"],
                        pin_factory=factory)

    # 前進 -> 停止 -> 後進 -> 停止
    try:
        # 前進 - 1秒
        print("前進 - 1秒")
        motor_left.forward()
        motor_right.forward()
        sleep(1)
        # 停止 - 1秒
        print("停止 - 1秒")
        motor_left.stop()
        motor_right.stop()
        sleep(1)
        # 後進 - 1秒
        print("後進 - 1秒")
        motor_left.backward()
        motor_right.backward()
        sleep(1)
        # 停止
        print("停止")
        motor_left.stop()
        motor_right.stop()
    except KeyboardInterrupt:
        print("stop")
        # 停止
        motor_left.stop()
        motor_right.stop()

    return

if __name__ == "__main__":
    main()
