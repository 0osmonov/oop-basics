import time

# --- ЗАДАНИЕ 1: Проверка администратора ---

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

# Декоратор для проверки роли
def is_admin(func):
    def wrapper(user, *args, **kwargs):
        if user.role == "admin":
            return func(user, *args, **kwargs)
        else:
            print(f"У пользователя {user.name} нет доступа!")
    return wrapper

@is_admin
def delete_video(user):
    print(f"Видео удалено (выполнил: {user.name})")

# Проверка Задания 1
admin = User("Ardager", "admin")
common_user = User("Bek", "user")

print("--- Проверка доступа ---")
delete_video(admin)        # Выполнится
delete_video(common_user)  # Выведет "У вас нет доступа"


# --- ЗАДАНИЕ 2: Декоратор таймера ---

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()    # Засекаем время начала
        result = func(*args, **kwargs) # Выполняем саму функцию
        end_time = time.time()      # Засекаем время конца
        print(f"Время выполнения: {round(end_time - start_time, 1)} секунд")
        return result
    return wrapper

@timer
def download_video():
    time.sleep(2) # Имитация задержки загрузки
    print("Видео загружено")

# Проверка Задания 2
print("\n--- Проверка таймера ---")
download_video()