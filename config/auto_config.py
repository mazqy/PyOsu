import pygame as pg
import platform

op_system = platform.system()

def detect_win_settings():
    import win32api
    pg.init()
    display_info = pg.display.Info()
    screen_height = display_info.current_h
    screen_width = display_info.current_w
    device = win32api.EnumDisplayDevices()
    device_config = win32api.EnumDisplaySettings(device.DeviceName, -1)
    pg.quit()
    return "Screen: {}x{}; Monitor/s HZ: {}".format(screen_width, screen_height, device_config.DisplayFrequency)

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
        
        return "Screen: {}x{}; Monitor/s HZ: {}".format(screen_width, screen_height, monitor_hz)
    except:
        return "[!] Failed to detect some Linux display settings. Default settings will be applyed instead."


if op_system == 'Windows':
    print(detect_win_settings())
    input("")
elif op_system == 'Linux':
    print(detect_linux_settings())
    input("")
else:
    print('[✗] PyOsu! does not support "{}" operating system'.format(op_system))