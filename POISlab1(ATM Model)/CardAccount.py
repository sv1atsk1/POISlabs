from string import ascii_letters

class CardAccount:
    Numbers = "1234567890"
    S_RUS = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self,owner_fio,card_number,expiration_date,PIN,CVV):
        self.verify_fio(owner_fio)
        self.verify_card_number(card_number)
        self.verify_expiration_date(expiration_date)
        self.verify_PIN(PIN)
        self.verify_CVV(CVV)

        self.__owner_fio = owner_fio.split()
        self.__card_number = card_number.split()
        self.__expiration_date = expiration_date.split("/")
        self.__PIN = PIN
        self.__CVV = CVV

    @classmethod
    def verify_fio(cls,fio):
        if type(fio) != str:
            raise TypeError("ФИО должно быть строкой")
        fio_str = fio.split()
        if len(fio_str) != 3:
            raise TypeError("Неверный формат записи")

        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER + "-"

        for letter in fio_str:
            if len(letter) < 1:
                raise TypeError("В ФИО должен быть хотя бы один символ")
            if len(letter.strip(letters)) != 0:
                raise TypeError("В ФИО можно использовать только буквенный символы и дефис")

    @classmethod
    def verify_card_number(cls,card_number):
        if type(card_number) != str:
            raise TypeError("Номер карты должен быть строкой")
        card_number_str = card_number.split()
        if len(card_number_str) != 4:
            raise TypeError("Неверный формат записи номера карты (используйте пробелы после каждого четвертой цифры в номере карты)")
        numbers = cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in card_number_str:
            if len(number) == 0:
                raise TypeError("В номере карты должно быть 16 символов")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В номере карты можно использовать только цифры")

    @classmethod
    def verify_expiration_date(cls,expiration_date):
        if type(expiration_date) != str:
            raise TypeError("Срок Действия карты должен быть строкой")
        expiration_date_str = expiration_date.split("/")
        if len(expiration_date_str) != 2:
            raise TypeError("Неверный формат записи номера карты используйте символ / для разделения месяца и года")
        numbers = cls.Numbers + "/"

        for number in expiration_date_str:
            if len(number) == 0:
                raise TypeError("В сроке действия должно быть 4 цифры разделенных /")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В сроке действия можно использовать только цифры,разделенные /")

    @classmethod
    def verify_PIN(cls,PIN):

        if type(PIN) != str:
            raise TypeError("Пин-код должен быть строкой")
        if len(PIN) != 4:
            raise TypeError("Неверный формат записи пин-кода:используйте только 4 цифры без пробела")
        numbers = cls.Numbers

        for number in PIN:
            if len(number) == 0:
                raise TypeError("В пин-коде должно быть 4 цифры")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В пин-коде можно использовать только цифры")

    @classmethod
    def verify_CVV(cls, CVV):
        if type(CVV) != str:
            raise TypeError("CVV-код должен быть строкой")
        if len(CVV) != 3:
            raise TypeError("Неверный формат записи CVV-кода:используйте только 3 цифры без пробела")
        numbers = cls.Numbers

        for number in CVV:
            if len(number) == 0:
                raise TypeError("В CVV-коде должно быть 3 цифры")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В CVV-коде можно использовать только цифры")

    @property
    def owner_fio(self):
        return self.__owner_fio

    @owner_fio.setter
    def owner_fio(self,owner_fio):
        self.verify_fio(owner_fio)
        self.__owner_fio = owner_fio

    @property
    def card_number(self):
        return self.__card_number

    @card_number.setter
    def card_number(self, card_number):
        self.verify_card_number(card_number)
        self.__card_number = card_number

    @property
    def expiration_date(self):
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        self.verify_expiration_date(expiration_date)
        self.__expiration_date = expiration_date

    @property
    def PIN(self):
        return self.__PIN

    @PIN.setter
    def PIN(self,PIN):
        self.verify_PIN(PIN)
        self.__PIN = PIN

    @property
    def CVV(self):
        return self.__CVV

    @CVV.setter
    def CVV(self, CVV):
        self.verify_CVV(CVV)
        self.__CVV = CVV
