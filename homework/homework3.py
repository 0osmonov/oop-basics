from abc import ABC, abstractmethod

class Hero(ABC):
    def __init__(self, name, level, health, strength):
        self.name = name
        self.level = level
        self.__health = health  
        self.strength = strength

    def greet(self):
        print(f"Привет, я {self.name}, мой уровень {self.level}")

    def rest(self):
        self.__health += 1
        print(f"{self.name} отдыхает. Здоровье стало: {self.__health}")

    @abstractmethod
    def attack(self):
        pass

class Warrior(Hero):
    def attack(self):
        print(f"{self.name} атакует мечом!")

class Mage(Hero):
    def attack(self):
        print(f"{self.name} использует магию!")

class Assassin(Hero):
    def attack(self):
        print(f"{self.name} атакует из-под тишка!")

warrior = Warrior("Артур", 10, 100, 20)
mage = Mage("Мерлин", 12, 80, 15)
assassin = Assassin("Тень", 11, 90, 18)

for hero in [warrior, mage, assassin]:
    hero.greet()
    hero.attack()
    hero.rest()
    print("-" * 20)