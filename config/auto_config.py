import pygame as pg
import platform
import os
import tkinter as tk
from tkinter import filedialog
from config.settings import save_setting

op_system = platform.system()
info_message = "Screen: {}x{}; Monitor/s HZ: {}"

def detect_win_settings():
    import win32api
    import ctypes
    print("Loading settings for your computer...")
    osu_path = os.path.join(f"C:/Users/{os.getlogin()}/AppData/Local/osu!")
    ctypes.windll.user32.SetProcessDPIAware()
    try:
        pg.init()
        display_info = pg.display.Info()
        screen_height = display_info.current_h
        screen_width = display_info.current_w
        device = win32api.EnumDisplayDevices()
        device_config = win32api.EnumDisplaySettings(device.DeviceName, -1)
        monitor_hz = device_config.DisplayFrequency
        save_setting('Screen', 'width', screen_width)
        save_setting('Screen', 'height', screen_height)
        save_setting('Screen', 'FPS', monitor_hz*2)
        pg.quit()
    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        input("[!] Failed to detect some display settings. Default settings will be applyed instead.")

    if os.path.exists(osu_path):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Osu! path found: {}\n".format(osu_path))
        try:
            change_option = input("Change Osu! path? (y/n)")
            if change_option.lower().strip() == "y":
                root = tk.Tk()
                root.withdraw()
                osu_path = filedialog.askdirectory(title="Select Osu! folder")

            elif change_option.lower().strip() == "n":
                pass
            save_setting('Paths', 'osumainpath', osu_path)
            save_setting('Paths', 'osuskinspath', os.path.join(osu_path + "/Skins"))
            save_setting('Paths', 'osusongspath', os.path.join(osu_path + "/Songs"))
        except:
            print('[!] Invalid input. Please enter "y" for yes, "n" for no, or just press Enter.')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("[!] Osu! path not found. You may not have Osu! installed or rather have the Osu! folder in another location.\n")
        print("[i] To check, open Osu! and open settings, then click the button that opens the folder where it locates.\n")

        try:
            change_option = input("Change found Osu! path? (y/n)")
            if change_option.lower().strip() == "y":
                root = tk.Tk()
                root.withdraw()
                osu_path = filedialog.askdirectory(title="Select Osu! folder")
                save_setting('Paths', 'osumainpath', osu_path)
                save_setting('Paths', 'osuskinspath', os.path.join(osu_path + "/Skins"))
                save_setting('Paths', 'osusongspath', os.path.join(osu_path + "/Songs"))

            elif change_option.lower().strip() == "n":
                pass
        except:
            print('[!] Invalid input. Please enter "y" for yes, "n" for no, or just press Enter.')
        
    
def detect_linux_settings():
    import subprocess
    pg.init()
    display_info = pg.display.Info()
    screen_height = display_info.current_h
    screen_width = display_info.current_w
    
    try:
        monitor_hz = "Unknown"
        exit = subprocess.check_output("xrandr --verbose", shell=True, encoding="utf-8")
        for line in exit.splitlines():
            if "Refresh" in line:
                monitor_hz = line.split(":")[1].strip()
        
        save_setting('Screen', 'width', screen_width)
        save_setting('Screen', 'height', screen_height)
        save_setting('Screen', 'FPS', monitor_hz*2)
    except:
        return "[!] Failed to detect some display settings. Default settings will be applyed instead."
        


def show_autoconfig():
    if op_system == 'Windows':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(detect_win_settings())
    elif op_system == 'Linux':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(detect_linux_settings())
    else:
        print('[✗] PyOsu! does not support "{}" operating system. You cannot use PyOsu! yet.'.format(op_system))