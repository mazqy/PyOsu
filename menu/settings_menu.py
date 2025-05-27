import os
from config.settings import get_setting, save_setting

def show_menu_settings():
    settings = {
        "Audio": {
            "Volume": get_setting('Audio', 'Volume', cast=float),
            "HitsoundVolume": get_setting('Audio', 'HitsoundVolume', cast=float),
        },
        "Game": {
            "Dim": get_setting('Game', 'Dim', cast=float),
            "PlayAreaDim": get_setting('Game', 'PlayAreaDim', cast=float),
        },
        "General": {
            "CursorSize": get_setting('General', 'CursorSize', cast=float),
        },
        "Screen": {
            "FPS": get_setting('Screen', 'FPS', cast=int),
            "Width": get_setting('Screen', 'Width', cast=int),
            "Height": get_setting('Screen', 'Height', cast=int),
            "Fullscreen": get_setting('Screen', 'Fullscreen', cast=bool),
        }
    }

    os.system('cls' if os.name == 'nt' else 'clear')
    print("[Settings]\n")

    print("--Screen--")
    print(" 1- Width:", settings["Screen"]["Width"])
    print(" 2- Height:", settings["Screen"]["Height"])
    print(" 3- Fullscreen Mode:", settings["Screen"]["Fullscreen"])
    print(" 4- FPS:", settings["Screen"]["FPS"])

    print("\n--In Game--")
    print(" 5- Background DIM:", settings["Game"]["Dim"])
    print(" 6- Play Area DIM:", settings["Game"]["PlayAreaDim"])

    print("\n--Audio--")
    print(" 7- Music Volume:", settings["Audio"]["Volume"])
    print(" 8- Hitsounds Volume:", settings["Audio"]["HitsoundVolume"])
    print('\n[i] 1 equals 100% volume')

    setting_map = {
        1: ("Screen", "Width", int),
        2: ("Screen", "Height", int),
        3: ("Screen", "Fullscreen", bool),
        4: ("Screen", "FPS", int),
        5: ("Game", "Dim", float),
        6: ("Game", "PlayAreaDim", float),
        7: ("Audio", "Volume", float),
        8: ("Audio", "HitsoundVolume", float)
    }

    while True:
        try:
            setting_input = int(input("\n >>"))
            if setting_input in setting_map:
                section, key, value_type = setting_map[setting_input]
                raw_input = input(f"\n>>Enter new value for {key}: ")

                if value_type == bool:
                    value = raw_input.lower() in ('1', 'true', 'yes', 'on')
                else:
                    value = value_type(raw_input)

                save_setting(section, key, value)
                input(f"[✓] {key} updated to {value}")
                break
            else:
                input("\n[!] You can only choose from 1 to {}".format(len(setting_map)))
        except:
            input("\n[!] Invalid input. Please enter a valid value.")
