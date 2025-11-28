## Alienware Dark Stabilizer Hotkey Toggle

Allows you to toggle the feature via keyboard.

### Changes you may need to make

You may need to change the manufacturer, model or keyboard keys depending on your preference.

### How to build

```shell
python.exe -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
pyinstaller --noconsole --onefile .\script.py
```

### Helpful Resources
* https://github.com/ScriptGod1337/kvm?tab=readme-ov-file#monitortool-hook
* https://github.com/scottaxcell/winddcutil
* https://www.nirsoft.net/utils/control_my_monitor.html
