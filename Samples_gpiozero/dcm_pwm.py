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
        # 最高速で前進 - 1秒
        print("最高速で前進 - 1秒")
        motor_left.value = 1.0
        motor_right.value = 1.0
        sleep(1)
        # 少し遅く前進 - 1秒
        print("少し遅く前進 - 1秒")
        motor_left.value = 0.75
        motor_right.value = 0.75
        sleep(1)
        # 遅く前進 - 2秒
        print("遅く前進 - 1秒")
        motor_left.value = 0.5
        motor_right.value = 0.5
        sleep(1)
        # 停止 - 1秒
        motor_left.value = 0.0
        motor_right.value = 0.0
        sleep(1)
        # 最高速で後進 - 1秒
        print("最高速で後進 - 1秒")
        motor_left.value = -1.0
        motor_right.value = -1.0
        sleep(1)
        # 少し遅く後進 - 1秒
        print("少し遅く後進 - 1秒")
        motor_left.value = -0.75
        motor_right.value = -0.75
        sleep(1)
        # 遅く後進 - 2秒
        print("遅く後進 - 1秒")
        motor_left.value = -0.5
        motor_right.value = -0.5
        sleep(1)
        # 停止 - 1秒
        motor_left.value = 0.0
        motor_right.value = 0.0
        sleep(1)
    except KeyboardInterrupt:
        print("stop")
        # 停止
        motor_left.value = 0.0
        motor_right.value = 0.0

    return

if __name__ == "__main__":
    main()
