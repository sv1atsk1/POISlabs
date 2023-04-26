#from string import ascii_letters
from PhoneAccount import *
class ATM():
    Symbols = "-/."
    Numbers = "1234567890"
    S_RUS = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self,balance,phone_number_balance):
        self.verify_card_balance(balance)
        self.verify_phone_number_balance(phone_number_balance)
        self.__phone_number_balance = phone_number_balance
        self.__balance = balance

    @classmethod
    def verify_card_balance(cls, balance = 0):
        if type(balance) != int:
            raise TypeError("Баланс на карте должен быть целым числом")
        balance_str = str(balance)
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in balance_str:
            if len(number) == 0:
                raise TypeError("Для задания баланса нужно ввести хотя бы одно число")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В номере карты можно использовать только цифры")

    @classmethod
    def verify_phone_number_balance(cls,phone_number_balance = 0):
        if type(phone_number_balance) != int:
            raise TypeError("Баланс на карте должен быть целым числом")
        balance_str = str(phone_number_balance)
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in balance_str:
            if len(number) == 0:
                raise TypeError("Для задания баланса нужно ввести хотя бы одно число")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В номере карты можно использовать только цифры")


    def deposit_money(self,deposit_balance):
        #print("Введите кол-во шекелей для пополнения")
        #deposit_balance = int(input())
        self.balance += deposit_balance
        print(self.balance)

    def deposit_phone_money(self):
        print("Введите сумму,которую желаете положить на телефон")
        phone_number_money_amount = int(input())
        self.phone_number_balance += phone_number_money_amount
        print(self.phone_number_balance)

    def withdraw_money(self):
        withdraw_amount = int(input())
        if withdraw_amount > self.balance or self.balance == 0:
            raise TypeError("Недостаточно денег на счете")
        self.balance -= withdraw_amount
        print(self.balance)

    def balance_check(self):
        print(self.balance)

    @property
    def phone_number_balance(self):
        return self.__phone_number_balance

    @phone_number_balance.setter
    def phone_number_balance(self, phone_number_balance):
        self.verify_phone_number_balance(phone_number_balance)
        self.__phone_number_balance = phone_number_balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance):
        self.verify_card_balance(balance)
        self.__balance = balance

if __name__ == "__main__":
        b = PhoneAccount("+375297261569")
        p = ATM(0,0)
        p.deposit_phone_money()
        print(p.__dict__)




