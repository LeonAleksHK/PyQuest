"""
Квесты: задания по Python с кодом, вариантами ответов и объяснениями.
Каждый квест — реальная ошибка, которую делают новички.
"""

QUESTS = [
    # ─── УРОВЕНЬ 1: Базовый синтаксис ───────────────────────────────────────
    {
        "name": "Бесконечный цикл",
        "topic": "Циклы while",
        "xp": 50,
        "desc": (
            "Код должен напечатать числа от 1 до 5,\n"
            "но программа зависла навсегда! Найди баг."
        ),
        "code": [
            ("i = 1",              "ok"),
            ("while i <= 5:",      "ok"),
            ("    print(i)",       "bug"),
            ("    # ← что здесь не хватает?", "hint"),
        ],
        "options": [
            {"text": "i += 1",     "correct": True},
            {"text": "print(i+1)", "correct": False},
            {"text": "break",      "correct": False},
            {"text": "i = i",      "correct": False},
        ],
        "hint": (
            "В цикле while переменная-счётчик должна изменяться,\n"
            "иначе условие i <= 5 будет истинно вечно.\n"
            "Добавь i += 1 внутри тела цикла."
        ),
        "explanation": (
            "i += 1 — это сокращение от i = i + 1.\n"
            "Без этой строки i всегда равно 1, цикл не заканчивается.\n"
            "Совет: всегда проверяй, изменяется ли условие цикла!"
        ),
    },
    {
        "name": "Неверный тип",
        "topic": "Типы данных",
        "xp": 55,
        "desc": (
            "Программа спрашивает возраст, но падает\n"
            "с TypeError при сравнении. Почему?"
        ),
        "code": [
            ('age = input("Возраст: ")', "ok"),
            ("if age >= 18:",             "bug"),
            ('    print("Доступ открыт")',"ok"),
        ],
        "options": [
            {"text": "age = int(input(...))", "correct": True},
            {"text": "age = str(age)",        "correct": False},
            {"text": "if age != 18:",          "correct": False},
            {"text": "if int >= 18:",          "correct": False},
        ],
        "hint": (
            "input() ВСЕГДА возвращает строку (str),\n"
            "даже если пользователь ввёл цифру '18'.\n"
            "Нельзя сравнивать строку '18' с числом 18 через >=."
        ),
        "explanation": (
            "int() преобразует строку в целое число.\n"
            "Правильно: age = int(input('Возраст: '))\n"
            "Можно также float() для дробных чисел."
        ),
    },
    {
        "name": "Отступы — это важно",
        "topic": "Синтаксис Python",
        "xp": 45,
        "desc": (
            "Python требует правильных отступов.\n"
            "Где ошибка в этом коде?"
        ),
        "code": [
            ("def greet(name):", "ok"),
            ('print("Привет,", name)', "bug"),
            ("",                 "ok"),
            ("greet('Аня')",     "ok"),
        ],
        "options": [
            {"text": "    print(...) — нужен отступ", "correct": True},
            {"text": "greet() → вызов неверный",      "correct": False},
            {"text": "def → нужен class",              "correct": False},
            {"text": "Нет return",                     "correct": False},
        ],
        "hint": (
            "В Python тело функции ОБЯЗАТЕЛЬНО пишется\n"
            "с отступом (4 пробела или 1 Tab).\n"
            "Без отступа Python не знает, что print внутри функции."
        ),
        "explanation": (
            "Правильно:\n"
            "def greet(name):\n"
            "    print('Привет,', name)  # 4 пробела!\n\n"
            "Python использует отступы вместо {} как в C/Java."
        ),
    },

    # ─── УРОВЕНЬ 2: Списки и индексы ────────────────────────────────────────
    {
        "name": "Индекс за границей",
        "topic": "Списки",
        "xp": 60,
        "desc": (
            "Код должен вывести последний элемент.\n"
            "Но выдаёт IndexError! Как исправить?"
        ),
        "code": [
            ("fruits = ['яблоко', 'банан', 'вишня']", "ok"),
            ("print(fruits[3])", "bug"),
            ("# Список из 3 элементов: 0,1,2", "hint"),
        ],
        "options": [
            {"text": "fruits[-1]",      "correct": True},
            {"text": "fruits[4]",       "correct": False},
            {"text": "fruits.last()",   "correct": False},
            {"text": "fruits[len]",     "correct": False},
        ],
        "hint": (
            "Индексы в Python начинаются с 0.\n"
            "Список ['яблоко','банан','вишня'] → индексы 0, 1, 2.\n"
            "fruits[3] — нет такого элемента!\n"
            "Отрицательный индекс -1 = последний элемент."
        ),
        "explanation": (
            "fruits[-1]  → последний элемент\n"
            "fruits[-2]  → предпоследний\n"
            "Также: fruits[len(fruits)-1] — но -1 гораздо удобнее!"
        ),
    },
    {
        "name": "Изменение при итерации",
        "topic": "Списки",
        "xp": 75,
        "desc": (
            "Код удаляет чётные числа из списка,\n"
            "но пропускает некоторые элементы. Почему?"
        ),
        "code": [
            ("nums = [1, 2, 3, 4, 5, 6]", "ok"),
            ("for n in nums:",             "bug"),
            ("    if n % 2 == 0:",         "ok"),
            ("        nums.remove(n)",     "bug"),
            ("# Результат: [1, 3, 5, 6] ← 6 осталась!", "hint"),
        ],
        "options": [
            {"text": "nums = [n for n in nums if n%2!=0]", "correct": True},
            {"text": "del nums[n]",                         "correct": False},
            {"text": "nums.pop()",                          "correct": False},
            {"text": "for n in nums[::-1]:",                "correct": False},
        ],
        "hint": (
            "Нельзя изменять список во время итерации по нему!\n"
            "При удалении элемента индексы сдвигаются,\n"
            "и следующий элемент пропускается.\n"
            "Лучший способ — list comprehension."
        ),
        "explanation": (
            "List comprehension — самый питоничный способ:\n"
            "nums = [n for n in nums if n % 2 != 0]\n\n"
            "Читается как: 'взять n из nums, если n нечётное'."
        ),
    },
    {
        "name": "Копия или ссылка?",
        "topic": "Ссылки в Python",
        "xp": 80,
        "desc": (
            "Мы хотим изменить копию списка,\n"
            "но оригинал тоже меняется. Как это?"
        ),
        "code": [
            ("original = [1, 2, 3]", "ok"),
            ("copy = original",       "bug"),
            ("copy.append(4)",        "ok"),
            ("print(original)",       "hint"),
            ("# Выводит: [1, 2, 3, 4] — баг!", "hint"),
        ],
        "options": [
            {"text": "copy = original[:]",  "correct": True},
            {"text": "copy = original",     "correct": False},
            {"text": "copy = list(original)", "correct": True},
            {"text": "copy = str(original)", "correct": False},
        ],
        "hint": (
            "В Python = не копирует список, а создаёт ВТОРУЮ ССЫЛКУ\n"
            "на тот же объект в памяти.\n"
            "Для копии используй срез [:] или list()."
        ),
        "explanation": (
            "Три способа скопировать список:\n"
            "1. copy = original[:]          # срез\n"
            "2. copy = list(original)       # конструктор\n"
            "3. copy = original.copy()      # метод\n\n"
            "Для вложенных списков нужен: import copy; copy.deepcopy()"
        ),
    },

    # ─── УРОВЕНЬ 3: Функции ─────────────────────────────────────────────────
    {
        "name": "Область видимости",
        "topic": "Функции",
        "xp": 70,
        "desc": (
            "Функция должна удвоить переменную x.\n"
            "Но внутри функции x не изменяется снаружи!"
        ),
        "code": [
            ("x = 10",          "ok"),
            ("def double():",   "ok"),
            ("    x = x * 2",   "bug"),
            ("double()",        "ok"),
            ("print(x)  # всё ещё 10!", "hint"),
        ],
        "options": [
            {"text": "def double(x): return x*2; x=double(x)", "correct": True},
            {"text": "global x внутри функции",                "correct": False},
            {"text": "x *= 2 без функции",                     "correct": False},
            {"text": "return x в функции",                     "correct": False},
        ],
        "hint": (
            "Внутри функции x = x * 2 создаёт ЛОКАЛЬНУЮ переменную x.\n"
            "Она не изменяет внешний x!\n"
            "Лучшее решение — передавать x как параметр и возвращать результат."
        ),
        "explanation": (
            "Правильный паттерн:\n"
            "def double(x):\n"
            "    return x * 2\n\n"
            "x = double(x)  # x теперь 20\n\n"
            "global x работает, но это плохая практика — избегай!"
        ),
    },
    {
        "name": "Изменяемый аргумент",
        "topic": "Функции",
        "xp": 90,
        "desc": (
            "Функция добавляет элементы в список.\n"
            "Но результат накапливается между вызовами!"
        ),
        "code": [
            ("def add(item, lst=[]):", "bug"),
            ("    lst.append(item)",   "ok"),
            ("    return lst",         "ok"),
            ("",                       "ok"),
            ("print(add('a'))  # ['a']",     "ok"),
            ("print(add('b'))  # ['a','b']!", "hint"),
        ],
        "options": [
            {"text": "def add(item, lst=None):\n  if lst is None: lst=[]", "correct": True},
            {"text": "lst = [] перед return",  "correct": False},
            {"text": "lst.clear() в начале",   "correct": False},
            {"text": "def add(item, lst=list)","correct": False},
        ],
        "hint": (
            "Изменяемые значения по умолчанию (списки, словари)\n"
            "создаются ОДИН РАЗ при определении функции,\n"
            "а не при каждом вызове!\n"
            "Используй None как значение по умолчанию."
        ),
        "explanation": (
            "Правильно:\n"
            "def add(item, lst=None):\n"
            "    if lst is None:\n"
            "        lst = []\n"
            "    lst.append(item)\n"
            "    return lst\n\n"
            "Это один из самых известных подводных камней Python!"
        ),
    },
    {
        "name": "lambda и замыкание",
        "topic": "Функции",
        "xp": 95,
        "desc": (
            "Создаём список функций-умножителей.\n"
            "Но все они умножают на 4, а не на 1,2,3,4!"
        ),
        "code": [
            ("funcs = []",               "ok"),
            ("for i in [1, 2, 3, 4]:",   "ok"),
            ("    funcs.append(lambda x: x * i)", "bug"),
            ("",                          "ok"),
            ("print(funcs[0](5))  # 20 вместо 5!", "hint"),
        ],
        "options": [
            {"text": "lambda x, i=i: x * i",                   "correct": True},
            {"text": "funcs.append(lambda: x * i)",             "correct": False},
            {"text": "def mul(x): return x * i",                "correct": False},
            {"text": "funcs.append(lambda x: x * 1)",           "correct": False},
        ],
        "hint": (
            "lambda x: x * i не сохраняет значение i,\n"
            "а создаёт ссылку на переменную i.\n"
            "После цикла i = 4, и ВСЕ лямбды видят i = 4.\n"
            "Захвати значение i через дефолтный аргумент!"
        ),
        "explanation": (
            "lambda x, i=i: x * i\n"
            "— здесь i=i захватывает ТЕКУЩЕЕ значение i\n"
            "  как дефолтный аргумент во время создания лямбды.\n\n"
            "Это называется 'замыкание' (closure) — важная тема!"
        ),
    },

    # ─── УРОВЕНЬ 4: Ошибки и исключения ─────────────────────────────────────
    {
        "name": "Поймай исключение",
        "topic": "Исключения",
        "xp": 65,
        "desc": (
            "Код падает с ZeroDivisionError.\n"
            "Как правильно обработать ошибку?"
        ),
        "code": [
            ("a, b = 10, 0",   "ok"),
            ("result = a / b", "bug"),
            ("print(result)",  "ok"),
        ],
        "options": [
            {"text": "try/except ZeroDivisionError", "correct": True},
            {"text": "if b == 0: b = 1",             "correct": False},
            {"text": "result = a // b",               "correct": False},
            {"text": "import math; math.inf",         "correct": False},
        ],
        "hint": (
            "В Python ошибки обрабатываются конструкцией try/except.\n"
            "try: — опасный код\n"
            "except ZeroDivisionError: — что делать при ошибке"
        ),
        "explanation": (
            "try:\n"
            "    result = a / b\n"
            "except ZeroDivisionError:\n"
            "    result = 0\n"
            "    print('Деление на ноль!')\n\n"
            "Можно ловить Exception — родитель всех исключений,\n"
            "но лучше указывать конкретный тип!"
        ),
    },
    {
        "name": "Сравнение с None",
        "topic": "Операторы",
        "xp": 60,
        "desc": (
            "Код сравнивает с None через ==.\n"
            "Это работает, но считается плохим стилем. Как правильно?"
        ),
        "code": [
            ("result = find_user(42)", "ok"),
            ("if result == None:",     "bug"),
            ('    print("Не найден")', "ok"),
        ],
        "options": [
            {"text": "if result is None:",  "correct": True},
            {"text": "if result != None:",  "correct": False},
            {"text": "if not result:",      "correct": False},
            {"text": "if result == 'None':", "correct": False},
        ],
        "hint": (
            "None в Python — это единственный объект типа NoneType.\n"
            "Для сравнения с None используй 'is None', а не '== None'.\n"
            "Оператор == может быть переопределён в пользовательском классе!"
        ),
        "explanation": (
            "Правильно: if result is None:\n"
            "Также верно: if result is not None:\n\n"
            "'is' проверяет идентичность объекта (тот же адрес),\n"
            "'==' проверяет равенство значений.\n"
            "PEP 8 требует использовать 'is' с None!"
        ),
    },

    # ─── УРОВЕНЬ 5: ООП и продвинутое ───────────────────────────────────────
    {
        "name": "Забытый self",
        "topic": "ООП",
        "xp": 80,
        "desc": (
            "Класс Dog не может лаять!\n"
            "Метод bark() выдаёт TypeError. Найди причину."
        ),
        "code": [
            ("class Dog:",          "ok"),
            ("    def __init__(self, name):", "ok"),
            ("        self.name = name", "ok"),
            ("    def bark():",      "bug"),
            ('        print(f"{self.name}: Гав!")', "ok"),
            ("",                    "ok"),
            ("d = Dog('Рекс')",     "ok"),
            ("d.bark()  # TypeError!", "hint"),
        ],
        "options": [
            {"text": "def bark(self):",    "correct": True},
            {"text": "def bark(name):",    "correct": False},
            {"text": "self.bark = bark()", "correct": False},
            {"text": "@staticmethod",      "correct": False},
        ],
        "hint": (
            "В Python все методы класса должны принимать self\n"
            "как первый параметр — это ссылка на экземпляр.\n"
            "Без self метод не знает, к какому объекту обращаться."
        ),
        "explanation": (
            "def bark(self):\n"
            "    print(f'{self.name}: Гав!')\n\n"
            "self — соглашение, не ключевое слово.\n"
            "Технически можно написать 'this' или 'me',\n"
            "но это нарушит стиль Python (PEP 8)."
        ),
    },
    {
        "name": "Строковый формат",
        "topic": "Строки",
        "xp": 50,
        "desc": (
            "Нужно вставить переменные в строку.\n"
            "Какой современный способ правильный?"
        ),
        "code": [
            ("name = 'Аня'",   "ok"),
            ("age = 20",       "ok"),
            ('info = "Меня зовут " + name + ", мне " + str(age)', "bug"),
            ("# Много конкатенаций — плохой стиль!", "hint"),
        ],
        "options": [
            {"text": 'f"Меня зовут {name}, мне {age}"', "correct": True},
            {"text": '"Меня зовут %s" % name',           "correct": False},
            {"text": '"{} {}".format(name, age)',        "correct": False},
            {"text": 'str(name) + str(age)',              "correct": False},
        ],
        "hint": (
            "f-строки (f-strings) — современный способ форматирования.\n"
            "Появились в Python 3.6.\n"
            "Пиши f перед кавычками и вставляй {переменную} прямо в текст."
        ),
        "explanation": (
            "f-строка: f'Меня зовут {name}, мне {age} лет'\n\n"
            "Внутри {} можно писать выражения:\n"
            "f'Через 5 лет мне будет {age + 5}'\n"
            "f'Имя заглавными: {name.upper()}'\n\n"
            "Это быстрее и читабельнее конкатенации!"
        ),
    },
    {
        "name": "Словарь: ключ не найден",
        "topic": "Словари",
        "xp": 65,
        "desc": (
            "Получаем значение из словаря.\n"
            "Если ключа нет — программа падает. Как избежать?"
        ),
        "code": [
            ("user = {'name': 'Иван', 'age': 25}", "ok"),
            ('email = user["email"]', "bug"),
            ("# KeyError: 'email'", "hint"),
        ],
        "options": [
            {"text": "user.get('email', 'не указан')", "correct": True},
            {"text": "user['email'] or None",           "correct": False},
            {"text": "try: user['email']",              "correct": False},
            {"text": "user.find('email')",              "correct": False},
        ],
        "hint": (
            "Метод .get(key, default) возвращает значение по ключу,\n"
            "а если ключа нет — возвращает default (по умолчанию None).\n"
            "Никакой ошибки не возникает!"
        ),
        "explanation": (
            "user.get('email')            # None если нет ключа\n"
            "user.get('email', 'N/A')     # 'N/A' если нет ключа\n\n"
            "Также полезно:\n"
            "'email' in user              # проверка наличия ключа\n"
            "user.setdefault('email', '') # добавить если нет"
        ),
    },
]
