def show_main_menu():
    import os
    import pyfiglet
    os.system('cls' if os.name == 'nt' else 'clear')
    print("{}\n".format(pyfiglet.figlet_format("PyOsu!")))
    print("1- Play")
    print("2- Skin")
    print("3- Settings")
    print("4- Exit")
    
    while True:
        try:
            option_input = int(input("\n >>"))
            if option_input in (1, 2, 3, 4):
                return option_input
            else:
                print("\n[!] Invalid input. You can only from 1 to 4.")
        except ValueError:
            print("\n[!] invalid input. You can only write positive numbers.")