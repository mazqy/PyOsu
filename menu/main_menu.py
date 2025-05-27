def show_main_menu():
    import os
    import pyfiglet
    os.system('cls' if os.name == 'nt' else 'clear')
    print("{}\n".format(pyfiglet.figlet_format("PyOsu!")))
    print("1- Play")
    print("2- Skin")
    print("3- Settings")
    
    while True:
        try:
            option_input = int(input("\n >>"))
            if option_input in (1, 2, 3):
                return option_input
            else:
                print("\n[!] You can only from 1 to 3")
        except ValueError:
            print("\n[!] You can only write positive numbers")