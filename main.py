from controller import *

while True:
    print("\n--- SYSTEM FIRM TŁUMACZENIOWYCH ---")
    print("1. Dodaj firmę")
    print("2. Wyświetl firmy")
    print("3. Edytuj firmę")
    print("4. Usuń firmę")
    print("5. Mapa firm")
    print("0. Wyjście")

    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        add_firma()

    elif wybor == "2":
        read_firmy()

    elif wybor == "3":
        update_firma()

    elif wybor == "4":
        delete_firma()

    elif wybor == "5":
        get_mapa_firm()

    elif wybor == "0":
        break

    else:
        print("Nieprawidłowa opcja")


