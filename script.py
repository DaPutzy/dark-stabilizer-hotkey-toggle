import monitorcontrol
import pynput
import pythoncom
import wmi

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

MANUFACTURER = "DEL" # somehow its DEL not DELL?
MODEL        = "AW3225QF"

########################
#    GLOBAL VALUES     #
########################

current_value_index = 0

########################
#      FUNCTIONS       #
########################

def to_string(value):
    return "".join(chr(c) for c in value if c > 0)

def find_monitor_index():
    w = wmi.WMI(namespace='root\\wmi')

    for index, info in enumerate(w.WmiMonitorID(), 0):
        # print(f"ascii: {to_string(info.ManufacturerName)}")
        # print(f"ascii: {to_string(info.UserFriendlyName)}")

        if info.Active == True and to_string(info.ManufacturerName) == MANUFACTURER and to_string(info.UserFriendlyName) == MODEL:
            return index

    return -1

# noinspection PyProtectedMember
def on_press(key):
    global current_value_index

    pythoncom.CoInitialize()

    if not key == KEY_INCREASE and not key == KEY_DECREASE:
        return

    monitor_index = find_monitor_index()

    if monitor_index == -1:
        print("could not find monitor")
        exit(1)

    monitor = monitorcontrol.get_monitors()[monitor_index]
    with monitor:
        if key == KEY_INCREASE:
            current_value_index = 0 if current_value_index == 3 else current_value_index + 1

        if key == KEY_DECREASE:
            current_value_index = 3 if current_value_index == 0 else current_value_index - 1

        monitor._set_vcp_feature(VCP_CODE, VCP_CODE_VALUES[current_value_index])

########################
#         MAIN         #
########################

class Main:
    def __init__(self):
        with pynput.keyboard.Listener(on_press=on_press) as listener:
            listener.join()

if __name__ == "__main__":
    Main()
