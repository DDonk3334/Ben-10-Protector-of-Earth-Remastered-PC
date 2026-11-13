import json
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "settings.json")


class ConfigManager:
    DEFAULTS = {
        "game_path": "",
        "custom_art": "",
        "control_scheme": "keyboard_mouse",
        "resolution": "3",
        "fullscreen": True,
        "vsync": False,
        "fps_60": True,
        "low_end_pc": False
    }

    @staticmethod
    def load():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return {**ConfigManager.DEFAULTS, **data}
            except Exception:
                pass
        return ConfigManager.DEFAULTS.copy()

    @staticmethod
    def save(data):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    @staticmethod
    def apply_settings(data):
        sys_dir = os.path.join(BASE_DIR, "Engine", "memstick", "PSP", "SYSTEM")
        cheats_dir = os.path.join(BASE_DIR, "Engine", "memstick", "PSP", "Cheats")
        os.makedirs(sys_dir, exist_ok=True)
        os.makedirs(cheats_dir, exist_ok=True)

        low_pc = bool(data.get("low_end_pc", False))
        fps_60 = bool(data.get("fps_60", True))
        res_map = {"1": "1", "2": "3", "3": "4", "6": "8"}
        res = "1" if low_pc else res_map.get(str(data.get("resolution", "3")), "4")

        ppsspp_ini = (
            "[General]\n"
            "FirstRun = False\n"
            "RunCount = 5\n"
            f"EnableCheats = {fps_60}\n"
            "PauseWhenMinimized = True\n"
            "IgnoreBadMemAccess = True\n"
            "[CPU]\n"
            "CPUCore = 1\n"
            "SeparateCPUThread = True\n"
            "FastMemory = True\n"
            f"LockedCPUSpeed = {333 if fps_60 else 222}\n"
            "[Graphics]\n"
            "GraphicsBackend = 0 (OPENGL)\n"
            f"FullScreen = {bool(data.get('fullscreen', True))}\n"
            f"InternalResolution = {res}\n"
            f"VSyncInterval = {1 if data.get('vsync', False) else 0}\n"
            "FrameSkip = 0\n"
            "AutoFrameSkip = False\n"
            "HardwareTransform = True\n"
            "SoftwareSkinning = True\n"
            f"AnisotropyLevel = {0 if low_pc else 4}\n"
            f"TexScalingLevel = {1 if low_pc else 2}\n"
            "ShowFPSCounter = 0\n"
            "[Control]\n"
            "ShowTouchControls = False\n"
            "MouseControl = True\n"
        )
        with open(os.path.join(sys_dir, "ppsspp.ini"), "w", encoding="utf-8") as f:
            f.write(ppsspp_ini)

        cheat_text = (
            "_S ULUS-10305\n"
            "_G Ben 10: Protector of Earth\n"
            "_C1 60 FPS\n"
            "_L 0x20359B78 0x00000001\n"
        ) if fps_60 else ""

        for disc_id in ("ULUS10305", "ULES00905"):
            with open(os.path.join(cheats_dir, f"{disc_id}.ini"), "w", encoding="utf-8") as f:
                f.write(cheat_text)

        controls_ini = (
            "[ControlMapping]\n"
            "Up = 1-19,10-19\n"
            "Down = 1-20,10-20\n"
            "Left = 1-21,10-21\n"
            "Right = 1-22,10-22\n"
            "Circle = 1-59,10-97\n"
            "Cross = 1-62,10-96\n"
            "Square = 1-1001,10-99\n"
            "Triangle = 1-1002,10-100\n"
            "Start = 1-111,10-108\n"
            "Select = 1-61,10-109\n"
            "L = 1-45,10-102\n"
            "R = 1-33,10-103\n"
            "An.Up = 1-51,10-4003\n"
            "An.Down = 1-47,10-4002\n"
            "An.Left = 1-29,10-4001\n"
            "An.Right = 1-32,10-4000\n"
        )
        with open(os.path.join(sys_dir, "controls.ini"), "w", encoding="utf-8") as f:
            f.write(controls_ini)
          
