from retry import retry
import monitorcontrol
import pynput

########################
#      CONSTANTS       #
########################

VCP_CODE = monitorcontrol.vcp.VCPCode(
    name="dark stabilizer level",
    value=0xF4,
    code_type="rw",
    function="nc",
)

# 48 = OFF
# 49 = LVL 1
# 50 = LVL 2
# 51 = LVL 3
VCP_CODE_VALUES = [48, 49, 50, 51]

KEY_INCREASE = pynput.keyboard.Key.page_up
KEY_DECREASE = pynput.keyboard.Key.page_down

MODEL = "AW3225QF"

########################
#         MAIN         #
########################

class Main:

    vcp_code_index = 0

    monitor = None

    # sometimes get_vcp_capabilities fails for no reason
    @retry(tries=5, delay=5)
    def get_monitor(self):
        for monitor in monitorcontrol.get_monitors():
            with monitor:
                capabilities = monitor.get_vcp_capabilities()

                if capabilities.get("model") == MODEL:
                    return monitor

        return None

    def __init__(self):
        self.monitor = self.get_monitor()

        if self.monitor is None:
            print("could not find monitor")
            exit(1)

        print("ready")

        with pynput.keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    # noinspection PyProtectedMember
    def on_press(self, key):
        if not key == KEY_INCREASE and not key == KEY_DECREASE:
            return

        with self.monitor:
            if key == KEY_INCREASE:
                self.vcp_code_index = 0 if self.vcp_code_index == 3 else self.vcp_code_index + 1

            if key == KEY_DECREASE:
                self.vcp_code_index = 3 if self.vcp_code_index == 0 else self.vcp_code_index - 1

            self.monitor._set_vcp_feature(VCP_CODE, VCP_CODE_VALUES[self.vcp_code_index])

if __name__ == "__main__":
    Main()
