from abc import ABC, abstractmethod



class Hero:
    def __init__(self, name, lvl, hp):
        self.name = name
        self.lvl = lvl
        self.hp = hp

    def action(self):
        return f"{self.name} готов к бою!"

class MageHero(Hero):
    def __init__(self, name, lvl, hp, mp):
        super().__init__(name, lvl, hp)
        self.mp = mp

    def action(self):
        return f"Маг {self.name} кастует заклинание! MP: {self.mp}"

class WarriorHero(MageHero): # По условию наследуемся от MageHero
    def __init__(self, name, lvl, hp, mp):
        super().__init__(name, lvl, hp, mp)

    def action(self):
        return f"Воин {self.name} рубит мечом! Уровень: {self.lvl}"
    

    """@2"""


class BankAccount:
    def __init__(self, hero, balance, password, bank_name):
        self.hero = hero
        self._balance = balance      # Защищенный
        self.__password = password    # Приватный
        self.bank_name = bank_name

    def login(self, password):
        return self.__password == password

    @property
    def full_info(self):
        return f"Герой: {self.hero.name}, Баланс: {self._balance}"

    def get_bank_name(self):
        return self.bank_name

    def bonus_for_level(self):
        # В примере 50 уровень * 10 = 500 SOM
        return self.hero.lvl * 10

    # Магические методы
    def __str__(self):
        return f"{self.hero.name} | Баланс: {self._balance} SOM"

    def __add__(self, other):
        # Проверяем, что оба объекта - счета и их герои одного класса
        if isinstance(other, BankAccount) and type(self.hero) == type(other.hero):
            return self._balance + other._balance
        return "Ошибка: Нельзя сложить счета героев разных классов!"

    def __eq__(self, other):
        if isinstance(other, BankAccount):
            # Сравниваем тип героя и его уровень
            return type(self.hero) == type(other.hero) and self.hero.lvl == other.hero.lvl
        return False
    







class SmsService(ABC):
    @abstractmethod
    def send_otp(self, phone):
        pass

class KGSms(SmsService):
    def send_otp(self, phone):
        return f"<text>Код: 1234</text><phone>{phone}</phone>"

class RUSms(SmsService):
    def send_otp(self, phone):
        return {"text": "Код: 1234", "phone": f"{phone}"}