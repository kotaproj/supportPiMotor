from queue import Queue
import threading
import ast
from systems import SystemsData, RoboMode

# debug
import sys
from icecream import ic

class PreThread(threading.Thread):
    """
    プレゼンター
    """
    def __init__(self, snd_ques={}):
        ic()
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._rcv_que = Queue()
        self._snd_ques = snd_ques
        self._sysdat = SystemsData()
        return

    def stop(self):
        ic()
        self.stop_event.set()
        return


    def run(self):
        ic()
        while True:
            # time.sleep(0.050)
            item = self.rcv_que.get()
            print("[pre_th]", "run : get : ", item)
            if "sw" in item["type"]:
                self._recvice_sw(item)
            elif "subsc" in item["type"]:
                self._recvice_subsc(item)
            else:
                print("[pre_th]", "Error : ", item)

        return
    
    def _recvice_sw(self, item):
        ic()

        def send_que_sw_no1(action):
            led_act = "on" if "press" in action else "off"
            self._snd_ques["led"].put({"type": "led", "name": "no1", "action":led_act})
            return

        def send_que_sw_no2(action):
            led_act = "on" if "press" in action else "off"
            self._snd_ques["led"].put({"type": "led", "name": "no2", "action": led_act})
            return

        name = item["name"]
        action = item["action"]
        if "no1" in name:
            send_que_sw_no1(action)
        elif "no2" in name:
            send_que_sw_no2(action)
        else:
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "command not found!", name)
        return

    def _recvice_subsc(self, item):
        ic()

        def send_que_led(action):
            ic()
            if "led" not in self._snd_ques:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
                return
            val_name = "no1" if "no1" in action else "no2"
            val_act = "on" if "on" in action else "off"
            self._snd_ques["led"].put({"type": "led", "name": val_name, "action": val_act})
            return

        def send_que_buzzer(action):
            ic()
            if "buzzer" not in self._snd_ques:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
                return
            val_time = "500" if "short" in action else "3000"
            note = "C4"
            self._snd_ques["buzzer"].put({"type": "buzzer", "name": "buzzer", "time": val_time, "note": note})
            return

        def send_que_servo(action):
            ic()
            if "servo" not in self._snd_ques:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
                return
            val_name = "left" if "left" in action else "right"
            if "raise" in action:
                val_act = "raise"
            elif "down" in action:
                val_act = "down"
            elif "swing" in action:
                val_act = "swing"
            else:
                return
            self._snd_ques["servo"].put({"type": "servo", "name": val_name, "action": val_act})
            return

        def send_que_dcm(action):
            ic()
            if "dcm" not in self._snd_ques:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
                return

            acts = ["forward", "back", "stop", "left", "right", "brake"]
            
            val_act = ""
            for act in acts:
                if act in action:
                    val_act = act
                    # update : system data
                    self._sysdat.dcm_stat = act
                    # print()
                    print(self._sysdat.dcm_stat)
                    break
            # fast / mid / slow
            val_speed = self._sysdat.dcm_speed
            print(val_speed)

            self._snd_ques["dcm"].put({"type": "dcm", "action": val_act, "speed": val_speed})
            return

        def send_que_oled(action):
            ic()
            if "oled" not in self._snd_ques:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
                return
            val_time = "3000"
            val_disp = action.replace("oled_", "")

            self._snd_ques["oled"].put({"type": "oled", "time": val_time, "disp": val_disp})
            return

        def send_que_js0(action):
            ic()
            # if "js0" not in self._snd_ques:
            #     ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
            #     return

            def update_dcm():
                # 動作時はspeed変更
                dcm_stat = self._sysdat.dcm_stat
                if self._sysdat.dcm_stat in ["forward", "back", "left", "right"]:
                    self._snd_ques["dcm"].put({"type": "dcm", "action": dcm_stat, "speed": self._sysdat.dcm_speed})
                return

            # select : system mode
            # if "js0_on_select" in action:
            if "js0_on_a" in action:
                # next
                self._sysdat.update_next_robo_mode()
                self._snd_ques["led"].put({"type": "led", "name": "noAll", "action": "robo_mode"})

            if "js0_on_r" in action:
                if RoboMode.GEAR == self._sysdat.robo_mode:
                    self._sysdat.update_next_dcm_speed(dirct=True)
                    print("js0_on_r")
                    print(self._sysdat.dcm_speed)
                    update_dcm()
                else:
                    self._snd_ques["servo"].put({"type": "servo", "name": "right", "action": "raise"})

            if "js0_off_r" in action:
                if RoboMode.GEAR == self._sysdat.robo_mode:
                    pass
                else:
                    self._snd_ques["servo"].put({"type": "servo", "name": "right", "action": "down"})

            if "js0_on_l" in action:
                if RoboMode.GEAR == self._sysdat.robo_mode:
                    self._sysdat.update_next_dcm_speed(dirct=False)
                    print("js0_on_l")
                    print(self._sysdat.dcm_speed)
                    update_dcm()
                else:
                    self._snd_ques["servo"].put({"type": "servo", "name": "left", "action": "raise"})

            if "js0_off_l" in action:
                if RoboMode.GEAR == self._sysdat.robo_mode:
                    pass
                else:
                    self._snd_ques["servo"].put({"type": "servo", "name": "left", "action": "down"})

            return

        action = item["action"]
        ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, item)
        if "buzzer" in action:
            send_que_buzzer(action)
        elif "servo" in action:
            send_que_servo(action)
        elif "motor" in action:
            send_que_dcm(action)
        elif "oled" in action:
            send_que_oled(action)
        elif "led" in action:
            send_que_led(action)
        elif "js0" in action:
            send_que_js0(action)
        else:
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "command not found!")
        return

    @property
    def rcv_que(self):
        return self._rcv_que


def main():
    import time

    pre_th = PreThread()
    pre_th.start()
    q = pre_th.rcv_que
    q.put("123")
    time.sleep(1)

    for i in range(5):
        q.put(i)
        time.sleep(1)
    pre_th.stop()
   
    return

if __name__ == "__main__":
    main()