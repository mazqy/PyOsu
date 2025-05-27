import os
from config.settings import save_setting, get_setting
from config.settings import get_setting

def show_menu_skins():
    osu_path_skins = get_setting('Paths', 'osuskinspath')
    skin_name = get_setting('General', 'skin')

    os.system('cls' if os.name == 'nt' else 'clear')

    print("[Skins] (Not all skins compatible)\n")
    print("Current: " + skin_name + "\n")

    skins = []

    skin_index = 1
    for skin in os.listdir(osu_path_skins):
        skins.append(skin)
        print(f"{skin_index}- {skin}")
        skin_index+=1

    skin_input = int(input("\n >>"))

    save_setting('General', 'Skin',skins[skin_input - 1])

    input("\n[✓] Skin applyed succesfuly")