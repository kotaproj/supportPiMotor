import time
import pigpio

# DCモータのピン設定
PIN_AIN1 = 18
PIN_AIN2 = 23
PIN_BIN1 = 24
PIN_BIN2 = 13

DCM_DICT = {
    "ain1": PIN_AIN1,
    "ain2": PIN_AIN2,
    "bin1": PIN_BIN1,
    "bin2": PIN_BIN2,
}

# Duty設定
MIN_DUTY = 25
MAX_DUTY = 10000
SLOW_DUTY = MAX_DUTY * 0.5
MID_DUTY = MAX_DUTY * 0.75
FAST_DUTY = MAX_DUTY


def main():
    # 初期化
    pi = pigpio.pi()

    # 各ピンの設定
    for pin in DCM_DICT.values():
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.set_PWM_range(pin, MAX_DUTY)
        pi.set_PWM_dutycycle(pin, MIN_DUTY)

    # 前進 -> 停止 -> 後進 -> 停止
    try:
        # 最高速で前進 - 1秒
        print("最高速で前進 - 1秒")
        pi.set_PWM_dutycycle(DCM_DICT["ain1"], FAST_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["ain2"], MIN_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["bin1"], FAST_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["bin2"], MIN_DUTY)
        time.sleep(1)
        # 少し遅く前進 - 1秒
        print("少し遅く前進 - 1秒")
        pi.set_PWM_dutycycle(DCM_DICT["ain1"], MID_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["ain2"], MIN_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["bin1"], MID_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["bin2"], MIN_DUTY)
        time.sleep(1)
        # 遅く前進 - 2秒
        print("遅く前進 - 2秒")
        pi.set_PWM_dutycycle(DCM_DICT["ain1"], SLOW_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["ain2"], MIN_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["bin1"], SLOW_DUTY)
        pi.set_PWM_dutycycle(DCM_DICT["bin2"], MIN_DUTY)
        time.sleep(2)
        # 停止 - 1秒
        pi.write(DCM_DICT["ain1"], 0)
        pi.write(DCM_DICT["ain2"], 0)
        pi.write(DCM_DICT["bin1"], 0)
        pi.write(DCM_DICT["bin2"], 0)
    except KeyboardInterrupt:
        print("stop")
        # 停止
        pi.write(DCM_DICT["ain1"], 0)
        pi.write(DCM_DICT["ain2"], 0)
        pi.write(DCM_DICT["bin1"], 0)
        pi.write(DCM_DICT["bin2"], 0)

    # 片づけ
    for pin in DCM_DICT.values():
        pi.set_mode(pin, pigpio.INPUT)
    pi.stop()


if __name__ == "__main__":
    main()
