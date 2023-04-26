from string import ascii_letters

class BanknoteStorage:

    Numbers = "1234567890"
    S_RUS = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self, EUR_amount = 1500, RUB_amount = 500, BYN_amount = 300, USD_amount = 400):
        self.verify_USD_banknote_storage_balance(USD_amount)
        self.verify_BYN_banknote_storage_balance(BYN_amount)
        self.verify_RUB_banknote_storage_balance(RUB_amount)
        self.verify_EUR_banknote_storage_balance(EUR_amount)
        self.__EUR = EUR_amount
        self.__RUB = RUB_amount
        self.__BYN = BYN_amount
        self.__USD = USD_amount

    @classmethod
    def verify_EUR_banknote_storage_balance(cls, EUR_amount):
        if type(EUR_amount) != int:
            raise TypeError("Баланс в валютах должен быть целым числом")
        EUR_balance_str = str(EUR_amount)
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in EUR_balance_str:
            if len(number) == 0:
                raise TypeError("Для задания баланса нужно ввести хотя бы одно число")
            if len(number.strip(numbers)) != 0:
                raise TypeError("Для задания баланса в ваших валютах нужно использовать только цифры")

    @classmethod
    def verify_BYN_banknote_storage_balance(cls, BYN_amount):
        if type(BYN_amount) != int:
            raise TypeError("Баланс в валютах должен быть целым числом")
        BYN_balance_str = str(BYN_amount)
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in BYN_balance_str:
            if len(number) == 0:
                raise TypeError("Для задания баланса нужно ввести хотя бы одно число")
            if len(number.strip(numbers)) != 0:
                raise TypeError("Для задания баланса в ваших валютах нужно использовать только цифры")

    @classmethod
    def verify_USD_banknote_storage_balance(cls, USD_amount):
        if type(USD_amount) != int:
            raise TypeError("Баланс в валютах должен быть целым числом")
        USD_balance_str = str(USD_amount)
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in USD_balance_str:
            if len(number) == 0:
                raise TypeError("Для задания баланса нужно ввести хотя бы одно число")
            if len(number.strip(numbers)) != 0:
                raise TypeError("Для задания баланса в ваших валютах нужно использовать только цифры")

    @classmethod
    def verify_RUB_banknote_storage_balance(cls, RUB_amount):
        if type(RUB_amount) != int:
            raise TypeError("Баланс в валютах должен быть целым числом")
        RUB_balance_str = str(RUB_amount)
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in RUB_balance_str:
            if len(number) == 0:
                raise TypeError("Для задания баланса нужно ввести хотя бы одно число")
            if len(number.strip(numbers)) != 0:
                raise TypeError("Для задания баланса в ваших валютах нужно использовать только цифры")

    def deposit_money_in_banknote_storage(self):
        while True:
            print("Какую валюту вы хотите внести в хранилище банкнот \n""1 - BYN \n 2- RUB \n 3 - EUR \n 4 - USD \n 5 - Выход")
            answer = input()
            if answer == "5" or answer.lower() == "выход":
                break
            elif answer == "1":
                print("Введите количество денег,которые желаете положить в хранилище (BYN)")
                amount = int(input())
                self.BYN_amount += amount
            elif answer == "2":
                print("Введите количество денег,которые желаете положить в хранилище (RUB)")
                amount = int(input())
                self.RUB_amount += amount
            elif answer == "3":
                print("Введите количество денег,которые желаете положить в хранилище (EUR)")
                amount = int(input())
                self.EUR_amount += amount
            elif answer == "4":
                print("Введите количество денег,которые желаете положить в хранилище (USD)")
                amount = int(input())
                self.USD_amount += amount

    def check_banknote_storage(self):
        print(self.EUR_amount, self.BYN_amount, self.RUB_amount, self.USD_amount)

    @property
    def USD_amount(self):
        return self.__USD

    @USD_amount.setter
    def USD_amount(self, USD_amount):
        self.verify_USD_banknote_storage_balance(USD_amount)
        self.__USD = USD_amount

    @property
    def BYN_amount(self):
        return self.__BYN

    @BYN_amount.setter
    def BYN_amount(self, BYN_amount):
        self.verify_BYN_banknote_storage_balance(BYN_amount)
        self.__BYN = BYN_amount

    @property
    def RUB_amount(self):
        return self.__RUB

    @RUB_amount.setter
    def RUB_amount(self, RUB_amount):
        self.verify_RUB_banknote_storage_balance(RUB_amount)
        self.__RUB = RUB_amount

    @property
    def EUR_amount(self):
        return self.__EUR

    @EUR_amount.setter
    def EUR_amount(self, EUR_amount):
        self.verify_EUR_banknote_storage_balance(EUR_amount)
        self.__USD = EUR_amount

if __name__ == "__main__":
    p = BanknoteStorage(0,0,0,0)
    p.deposit_money_in_banknote_storage()
    print(p.__dict__)


