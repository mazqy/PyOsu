import os
from config.settings import save_setting, get_setting
from config.settings import get_setting

def show_menu_skins():
    osu_path_skins = get_setting('Paths', 'osuskinspath')
    skin_name = get_setting('General', 'skin')

    os.system('cls' if os.name == 'nt' else 'clear')

    print("[Skins] (Not all skins compatible yet)\n")

    if skin_name:
        print("Current skin: " + skin_name + "\n")
    else:
        print("[!] No skin selected yet. Please select one to be able to play.\n")

    skins = []

    skin_index = 1
    for skin in os.listdir(osu_path_skins):
        skins.append(skin)
        print(f"{skin_index}- {skin}")
        skin_index+=1
    while True:
        try:
            skin_input = int(input("\n >>"))
            save_setting('General', 'Skin',skins[skin_input - 1])
            if osu_path_skins in (osu_path_skins+("/approach.png", "/circle.png")):
                input("\n[✓] Skin applyed succesfuly")
                break
            else:
                input("\n[!] This skin is not compatible for playing. Try another one.")            
                
        except:
            print(f"\n[!] Invalid iniput. Please write a number between 1 to {skin_index - 1}.")
    