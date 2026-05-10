import random


class Hero:
    def __init__(self, name, level, health, strength):
        self.name = name
        self.level = level
        self.health = health
        self.strength = strength

    def greet(self):
        print(f"Привет, я {self.name}, мой уровень {self.level}")

    def attack(self):
        print(f"{self.name} наносит удар!")

    def rest(self):
        self.health += 1
        print(f"{self.name} отдыхает. Здоровье: {self.health}")


class Warrior(Hero):
    def __init__(self, name, level, health, strength, stamina):
        super().__init__(name, level, health, strength)  
        self.stamina = stamina  

    def attack(self):  
        print(f"{self.name} атакует мечом! (Выносливость: {self.stamina})")


class Mage(Hero):
    def __init__(self, name, level, health, strength, mana):
        super().__init__(name, level, health, strength)
        self.mana = mana

    def attack(self):
        print(f"{self.name} кастует заклинание! (Мана: {self.mana})")


class Assassin(Hero):
    def __init__(self, name, level, health, strength, stealth):
        super().__init__(name, level, health, strength)
        self.stealth = stealth

    def attack(self):
        print(f"{self.name} атакует из-под тишка! (Скрытность: {self.stealth})")


warrior_obj = Warrior("Конан", 10, 100, 20, 50)
mage_obj = Mage("Гэндальф", 12, 80, 15, 100)
assassin_obj = Assassin("Эцио", 11, 90, 18, 80)

print("\n--- Добро пожаловать в игру ---")
print("Выберите героя: 1 - Warrior, 2 - Mage, 3 - Assassin")

choice = input("Введите номер или название: ").strip().lower()

if choice in ["1", "warrior"]:
    player = warrior_obj
elif choice in ["2", "mage"]:
    player = mage_obj
elif choice in ["3", "assassin"]:
    player = assassin_obj
else:
    print("Неверный выбор. По умолчанию выбран Warrior.")
    player = warrior_obj

enemies = [warrior_obj, mage_obj, assassin_obj]
bot = random.choice(enemies)

print(f"\nВы выбрали: {player.__class__.__name__} ({player.name})")
print(f"Ваш противник: {bot.__class__.__name__} ({bot.name})\n")


p_type = player.__class__.__name__
b_type = bot.__class__.__name__

if p_type == b_type:
    print("Ничья! Герои разошлись миром.")
elif (
    (p_type == "Warrior" and b_type == "Assassin")
    or (p_type == "Assassin" and b_type == "Mage")
    or (p_type == "Mage" and b_type == "Warrior")
):
    print(f"Победа! {p_type} сильнее, чем {b_type}!")
else:
    print(f"Поражение! {b_type} одолел {p_type}!")
