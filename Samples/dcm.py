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


def main():
    # 初期化
    pi = pigpio.pi()

    # 各ピンの設定
    for pin in DCM_DICT.values():
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin, 0)

    # 前進 -> 停止 -> 後進 -> 停止
    try:
        # 前進 - 1秒
        print("前進 - 1秒")
        pi.write(DCM_DICT["ain1"], 1)
        pi.write(DCM_DICT["ain2"], 0)
        pi.write(DCM_DICT["bin1"], 1)
        pi.write(DCM_DICT["bin2"], 0)
        time.sleep(1)
        # 停止 - 1秒
        print("停止 - 1秒")
        pi.write(DCM_DICT["ain1"], 0)
        pi.write(DCM_DICT["ain2"], 0)
        pi.write(DCM_DICT["bin1"], 0)
        pi.write(DCM_DICT["bin2"], 0)
        time.sleep(1)
        # 後進 - 1秒
        print("後進 - 1秒")
        pi.write(DCM_DICT["ain1"], 0)
        pi.write(DCM_DICT["ain2"], 1)
        pi.write(DCM_DICT["bin1"], 0)
        pi.write(DCM_DICT["bin2"], 1)
        time.sleep(1)
        # 停止
        print("停止")
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
