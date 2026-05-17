rates = {
    "KGS": 1,
    "USD": 89,
    "EUR": 96,
    "RUB": 1.2
}

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def convert_to_kgs(self):
        return self.amount * rates[self.currency]

    def __str__(self):
        return f"{self.amount} {self.currency}"

    def __add__(self, other):
        if self.currency == other.currency:
            new_amount = self.amount + other.amount
            return Money(new_amount, self.currency)
        else:
            total_kgs = self.convert_to_kgs() + other.convert_to_kgs()
            return Money(total_kgs, "KGS")

    def __sub__(self, other):
        if self.currency == other.currency:
            new_amount = self.amount - other.amount
            return Money(new_amount, self.currency)
        else:
            total_kgs = self.convert_to_kgs() - other.convert_to_kgs()
            return Money(total_kgs, "KGS")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.amount * other, self.currency)
        return "Ошибка: Умножать можно только на число!"

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.amount / other, self.currency)
        return "Ошибка: Делить можно только на число!"


money1 = Money(100, "USD")   
money2 = Money(5000, "KGS")  

result_add = money1 + money2
print(f"Сложение: {money1} + {money2} = {result_add}") 

result_sub = money1 - money2
print(f"Вычитание: {money1} - {money2} = {result_sub}") 

money_usd = Money(50, "USD")
result_mul = money_usd * 2
print(f"Умножение: {money_usd} * 2 = {result_mul}") 

money_eur = Money(100, "EUR")
result_div = money_eur / 2
print(f"Деление: {money_eur} / 2 = {result_div}")