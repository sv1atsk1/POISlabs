import sys
from ATM import *
from CardAccount import *
from BanknoteStorage import *

def autorization():
    banknoteStorage = BanknoteStorage()
    atm = ATM(50000, 0)
    while True:
        command = str(input("")).lower()
        if command == "quit":
            sys.exit()
            #break
        elif command == "help":
            print('all commands: \n '
                  ' create card account \n '
                  ' pay phone \n '
                  ' pay banknote storage \n '
                  ' balance \n '
                  ' withdraw \n '
            )
        elif command == "create card account":
            print("Введите ФИО владельца карты")
            owner_fio = str(input())
            print("Введите номер карты")
            card_number = str(input())
            print("Введите  срок действия карты")
            expiration_date = str(input())
            print("Введите PIN")
            pin = str(input())
            print("Введите CVV")
            cvv = str(input())
            cardaccount = CardAccount(owner_fio,card_number,expiration_date,pin,cvv)
        elif command == "pay phone":
            atm.deposit_phone_money()
            print(atm.__dict__)
        elif command == "pay banknote storage":
            banknoteStorage.deposit_money_in_banknote_storage()
            print(banknoteStorage.__dict__)
        elif command == "balance":
            print(atm.__dict__)
        elif command == "withdraw":
            print("Введите кол-во денег,которые хотите вывести")
            atm.withdraw_money()
            print(atm.__dict__)

autorization()





# if __name__ == "__main__":
#     banknoteStorage = BanknoteStorage()
#     atm = ATM(50000, 0)
#     while True:
#         print("Выберите действие,которое хотите выполнить : \n 1 - Создать аккаунт карты \n 2 - Положить деньги на телефон \n 3 - Пополнить  денег на свой счёт в хранилище банкнот \n "
#               "4 - Посмотреть остаток на кард-счете \n 5 - Снятие наличных денег \n 6 - Выход")
#         answer = int(input())
#         if answer == "6" or str(answer).lower() == "выход":
#             break
#         elif answer == 1:
#             print("Введите ФИО владельца карты")
#             owner_fio = str(input())
#             print("Введите номер карты")
#             card_number = str(input())
#             print("Введите  срок действия карты")
#             expiration_date = str(input())
#             print("Введите PIN")
#             pin = str(input())
#             print("Введите CVV")
#             cvv = str(input())
#             cardaccount = CardAccount(owner_fio,card_number,expiration_date,pin,cvv)
#         elif answer == 2:
#             atm.deposit_phone_money()
#             print(atm.__dict__)
#         elif answer == 3:
#             print("1 - Если вы хотите посмотреть баланс в своём хранилище нажмите\n 2 - Задепать деньги на ваше хранилище банкнот \n 3 - Выход")
#             answerx = int(input())
#             while answerx != 3:
#                 if answerx == 1:
#                     print(banknoteStorage.__dict__)
#                 elif answerx == 2:
#                     banknoteStorage.deposit_money_in_banknote_storage()
#                     print(banknoteStorage.__dict__)
#         elif answer == 4:
#             print(atm.__dict__)
#         elif answer == 5:
#             print("Введите кол-во денег,которые хотите вывести")
#             atm.withdraw_money()
#             print(atm.__dict__)



