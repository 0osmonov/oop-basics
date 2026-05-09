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
        self.strength -= 1  
    def rest(self):
        print(f"{self.name} отдыхает…")
        self.health += 1  


hero1 = Hero("Арагорн", 10, 100, 20)
hero2 = Hero("Леголас", 12, 80, 15)

hero1.greet()
print(f"Статы до: Здоровье {hero1.health}, Сила {hero1.strength}")
hero1.attack()
hero1.rest()
print(f"Статы после: Здоровье {hero1.health}, Сила {hero1.strength}")

print("-" * 20)

hero2.greet()
hero2.attack()
hero2.rest()
print(f"Итог {hero2.name}: Здоровье {hero2.health}, Сила {hero2.strength}")