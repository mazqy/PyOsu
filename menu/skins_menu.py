import os
from config.settings import save_setting, get_setting

def show_menu_skins():
    osu_path = os.path.join(f"C:/Users/{os.getlogin()}/AppData/Local/osu!")
    osu_path_skins = os.path.join(osu_path + "/Skins")
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