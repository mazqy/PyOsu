from menu.main_menu import show_main_menu
from menu.settings_menu import show_menu_settings
from menu.skins_menu import show_menu_skins
from engine import game
from config.settings import get_setting, save_setting
import cProfile
import webbrowser

support_url = "https://ko-fi.com/mazqy"


if get_setting('Principal', 'configured') == "False":
    from config.auto_config import show_autoconfig
    show_autoconfig()
    save_setting('Principal', 'configured', True)

if __name__ == "__main__":
    while True:
        option = show_main_menu()
        match option:
            case 1:
                try:
                    cProfile.run('game()', sort='time')
                    input("[.] Press Enter to go back to the menu.")
                except Exception as e:
                    print("[!] Whoops, something gone wrong.\n")
                    print("[i] Probably because you did not select a skin.\n")
                    input(f"Error: {e}")
            case 2:
                show_menu_skins()
            case 3:
                show_menu_settings()
            case 4:
                break
            case 5:
                webbrowser.open(support_url)