import os


def show_main_menu():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(" ____         ___            _")
    print("|  _ \ _   _ / _ \ ___ _   _| |")
    print("| |_) | | | | | | / __| | | | |")
    print("|  __/| |_| | |_| \__ \ |_| |_|")
    print("|_|    \__, |\___/|___/\__,_(_)")
    print("       |___/\n")
    print("1- Play")
    print("2- Skin")
    print("3- Settings")
    print("4- Exit")
    print("\n5- Support the project ♡")
    
    while True:
        try:
            option_input = int(input("\n >>"))
            if option_input in (1, 2, 3, 4, 5):
                return option_input
            else:
                print("\n[!] Invalid input. You can only from 1 to 4.")
        except ValueError:
            print("\n[!] invalid input. You can only write positive numbers.")