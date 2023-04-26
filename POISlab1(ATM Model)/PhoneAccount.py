from string import ascii_letters
class PhoneAccount:
    Symbols = "-/."
    Numbers = "1234567890"
    S_RUS = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self,user_phone_number):
        self.verify_user_phone_number(user_phone_number)
        self.__user_phone_number = user_phone_number

    @classmethod
    def verify_user_phone_number(cls, user_phone_number):
        if type(user_phone_number) != str:
            raise TypeError("Мобильный номер банка должен быть строкой")
        if len(user_phone_number) != 13 and len(user_phone_number) != 12:
            raise TypeError(
                "Неверный формат записи мобильного номера банка (используйте + а далее 12 цифр номера или же 11 цифр и + перед ними)")
        numbers = "+" + cls.Numbers
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER

        for number in user_phone_number:
            if len(number) == 0:
                raise TypeError("В мобильном номере банка должно быть 12 цифр и + перед ними или же + и 11 цифр")
            if len(number.strip(numbers)) != 0:
                raise TypeError("В мобильном номере банка можно использовать только цифры и знак + перед ними")

    @property
    def bank_phone_number(self):
        return self.__user_phone_number

    @bank_phone_number.setter
    def bank_phone_number(self, user_phone_number):
        self.verify_user_phone_number(user_phone_number)
        self.__user_phone_number = user_phone_number



