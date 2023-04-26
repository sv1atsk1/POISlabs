from string import ascii_letters


class Bank:
    Symbols = "-/."
    Numbers = "1234567890"
    S_RUS = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self, bank_name, bank_address, bank_phone_number):
        self.verify_bank_phone_number(bank_phone_number)
        self.verify_bank_name(bank_name)
        self.verify_bank_address(bank_address)

        self.__bank_name = bank_name
        self.__bank_address = bank_address
        self.__bank_phone_number = bank_phone_number

    @classmethod
    def verify_bank_name(cls, bank_name):
        if type(bank_name) != str:
            raise TypeError("Название банка должно быть строкой")

        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER + "-"

        for letter in bank_name:
            if len(letter) < 1:
                raise TypeError("В названии банка должен быть хотя бы один символ")
            if len(letter.strip(letters)) != 0:
                raise TypeError("В названии банка  можно использовать только буквы и дефис")

    @classmethod
    def verify_bank_address(cls, bank_address):
        if type(bank_address) != str:
            raise TypeError("Адрес банка должен быть строкой")

        bank_address_str = bank_address.split()
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER + cls.Numbers + cls.Symbols
        if len(bank_address_str) != 2:
            raise TypeError("Неверный формат записи адреса банка,используйте пробелы между названием улицы и номером дома)")

        for letter in bank_address_str:
            if len(letter) < 1:
                raise TypeError("В адресе банка должен быть хотя бы один символ")
            if len(letter.strip(letters)) != 0:
                raise TypeError("В адресе банка  можно использовать только буквы,цифры,слеш вправо и дефис")

    @classmethod
    def verify_bank_phone_number(cls, bank_phone_number):
        if type(bank_phone_number) != str:
            raise TypeError("Мобильный номер банка должен быть строкой")
        if len(bank_phone_number) != 13 and len(bank_phone_number) != 12:
            raise TypeError("Неверный формат записи мобильного номера банка (используйте + а далее 12 цифр номера или же 11 цифр и + перед ними)")
        numbers = "+" + cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in bank_phone_number:
            if len(number) == 0:
                raise TypeError("В мобильном номере банка должно быть 12 цифр и + перед ними или же + и 11 цифр")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В мобильном номере банка можно использовать только цифры и знак + перед ними")

    @property
    def bank_name(self):
        return self.__bank_name

    @bank_name.setter
    def bank_name(self,bank_name):
        self.verify_bank_name(bank_name)
        self.__bank_name = bank_name

    @property
    def bank_address(self):
        return self.__bank_address

    @bank_address.setter
    def bank_address(self, bank_address):
        self.verify_bank_address(bank_address)
        self.__bank_address = bank_address

    @property
    def bank_phone_number(self):
        return self.__bank_phone_number

    @bank_phone_number.setter
    def bank_phone_number(self, bank_phone_number):
        self.verify_bank_phone_number(bank_phone_number)
        self.__bank_phone_number = bank_phone_number