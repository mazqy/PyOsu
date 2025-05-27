from menu.main_menu import show_main_menu
from menu.settings_menu import show_menu_settings
from menu.skins_menu import show_menu_skins
from engine import game
import cProfile

if __name__ == "__main__":
    while True:
        option = show_main_menu()
        match option:
            case 1:
                cProfile.run("game()")
                input("")
            case 2:
                show_menu_skins()
            case 3:
                show_menu_settings()