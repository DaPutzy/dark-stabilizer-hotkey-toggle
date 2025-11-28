import monitorcontrol
import pynput
import pythoncom
import wmi

'''
CONSTANTS
'''
DARK_STABILIZER_LEVEL_CODE = monitorcontrol.vcp.VCPCode(
    name="dark stabilizer level",
    value=0xF4,
    code_type="rw",
    function="nc",
)

CONST_OFF     = 48
CONST_LEVEL_1 = 49
CONST_LEVEL_2 = 50
CONST_LEVEL_3 = 51

KEY_TOGGLE = pynput.keyboard.Key.page_up
KEY_RESET  = pynput.keyboard.Key.page_down

MANUFACTURER = "DEL"
MODEL = "AW3225QF"

'''
GLOBAL VALUES
'''
current_value = CONST_OFF

'''
FUNCTIONS
'''
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
    global current_value

    pythoncom.CoInitialize()

    if not key == KEY_TOGGLE and not key == KEY_RESET:
        return

    monitor_index = find_monitor_index()

    if monitor_index == -1:
        print("could not find monitor")
        exit(1)

    monitor = monitorcontrol.get_monitors()[monitor_index]
    with monitor:
        # dark_stabilizer_level = monitor._get_vcp_feature(DARK_STABILIZER_LEVEL_CODE)

        if key == KEY_TOGGLE:
            if current_value == CONST_OFF:
                monitor._set_vcp_feature(DARK_STABILIZER_LEVEL_CODE, CONST_LEVEL_1)
                current_value = CONST_LEVEL_1
            elif current_value == CONST_LEVEL_1:
                monitor._set_vcp_feature(DARK_STABILIZER_LEVEL_CODE, CONST_LEVEL_2)
                current_value = CONST_LEVEL_2
            elif current_value == CONST_LEVEL_2:
                monitor._set_vcp_feature(DARK_STABILIZER_LEVEL_CODE, CONST_LEVEL_3)
                current_value = CONST_LEVEL_3
            else:
                monitor._set_vcp_feature(DARK_STABILIZER_LEVEL_CODE, CONST_OFF)
                current_value = CONST_OFF

        if key == KEY_RESET:
            monitor._set_vcp_feature(DARK_STABILIZER_LEVEL_CODE, CONST_OFF)
            current_value = CONST_OFF

'''
MAIN
'''
class Main:
    def __init__(self):
        with pynput.keyboard.Listener(on_press=on_press) as listener:
            listener.join()

if __name__ == "__main__":
    Main()
