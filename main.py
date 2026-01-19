import json
import os
import random
from player import Player, Warrior, Mage, Archer, Enemy
from artifacts import ArtifactBank


class Game:
    def __init__(self):
        self.artifact_bank = ArtifactBank()
        self.current_player = None
        self.users_file = 'users.json'

    def register_user(self):
        """Регистрация нового пользователя"""
        print("\n" + "=" * 50)
        print("РЕГИСТРАЦИЯ")
        print("=" * 50)

        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        # Проверяем, существует ли пользователь
        users = self.load_users()
        if username in users:
            print("Пользователь с таким именем уже существует!")
            return None

        # Сохраняем нового пользователя
        users[username] = password
        self.save_users(users)

        print(f"\nПользователь {username} успешно зарегистрирован!")
        return username

    def login_user(self):
        """Вход пользователя"""
        print("\n" + "=" * 50)
        print("ВХОД В ИГРУ")
        print("=" * 50)

        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        users = self.load_users()
        if username in users and users[username] == password:
            print(f"\nДобро пожаловать, {username}!")
            return username
        else:
            print("\nНеверное имя пользователя или пароль!")
            return None

    def load_users(self):
        """Загружает пользователей из файла"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_users(self, users):
        """Сохраняет пользователей в файл"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def save_game(self, player):
        """Сохраняет игру"""
        filename = f"{player.username}_save.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(player.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"\nИгра сохранена в файл {filename}")

    def load_game(self, username):
        """Загружает игру"""
        filename = f"{username}_save.json"
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return Player.from_dict(data)
            except:
                print("Ошибка загрузки сохранения!")
                return None
        return None

    def create_character(self):
        """Создание персонажа"""
        print("\n" + "=" * 50)
        print("СОЗДАНИЕ ПЕРСОНАЖА")
        print("=" * 50)

        print("1. Воин - высокая живучесть, средний урон")
        print("2. Маг - мощные атаки, низкое здоровье")
        print("3. Лучник - баланс здоровья и урона")

        choice = input("\nВыберите класс (1-3): ")

        name = input("Введите имя персонажа: ")

        if choice == '1':
            character = Warrior(name)
        elif choice == '2':
            character = Mage(name)
        elif choice == '3':
            character = Archer(name)
        else:
            print("Неверный выбор, создан Воин по умолчанию")
            character = Warrior(name)

        print(f"\nПерсонаж {character} создан!")
        return character

    def battle(self, player_char, enemy):
        """Битва между игроком и врагом"""
        print("\n" + "=" * 50)
        print(f"БИТВА: {player_char.name} vs {enemy.name}")
        print("=" * 50)

        round_num = 1
        while player_char.is_alive() and enemy.is_alive():
            print(f"\nРаунд {round_num}")
            print(f"{player_char}")
            print(f"{enemy}")
            print("-" * 30)

            # Ход игрока
            print("\nВаш ход:")
            print("1. Обычная атака")
            print("2. Особое умение")
            print("3. Исцеление (25 HP)")

            choice = input("Выберите действие (1-3): ")

            if choice == '1':
                damage = player_char.attack(enemy)
                print(f"Вы нанесли {damage} урона!")
            elif choice == '2':
                damage = player_char.special_ability()
                print(f"Вы использовали особое умение и нанесли {damage} урона!")
                enemy.health -= damage
            elif choice == '3':
                healed = player_char.heal(25)
                print(f"Вы исцелились на {healed} HP!")
            else:
                print("Неверный выбор, пропускаете ход!")

            # Проверяем, жив ли враг
            if not enemy.is_alive():
                print(f"\n{enemy.name} повержен!")
                break

            # Ход врага
            print(f"\nХод {enemy.name}:")
            if random.random() < 0.3:
                damage = enemy.special_ability()
                print(f"{enemy.name} использует особую атаку и наносит {damage} урона!")
            else:
                damage = enemy.attack(player_char)
                print(f"{enemy.name} атакует и наносит {damage} урона!")

            round_num += 1

        if player_char.is_alive():
            print(f"\nПОБЕДА! Вы победили {enemy.name}!")
            return True
        else:
            print(f"\nПОРАЖЕНИЕ! {enemy.name} победил вас!")
            return False

    def story_branch_1(self):
        """Первая сюжетная ветка - Путь Воина"""
        print("\n" + "=" * 50)
        print("ПУТЬ ВОИНА: Защита деревни")
        print("=" * 50)

        print("\nВы прибыли в деревню, которую атакуют гоблины.")
        print("Жители просят о помощи.")

        choice = input("\n1. Защитить деревню\n2. Пройти мимо\nВыберите действие (1-2): ")

        if choice == '1':
            print("\nВы решаете защитить деревню!")
            enemy = Enemy("Вождь гоблинов", 80, 15, "Гоблин")
            if self.battle(self.current_player.character, enemy):
                print("\nЖители деревни благодарны вам!")
                print("В награду вы получаете 50 золота и артефакт!")
                self.current_player.gold += 50

                # Получаем артефакт из копилки
                if not self.artifact_bank.is_empty():
                    artifact = self.artifact_bank.get_artifact(0)
                    self.current_player.artifacts.append(artifact)
                    print(f"Вы получили артефакт: {artifact['name']}!")

                    if self.artifact_bank.is_empty():
                        self.artifact_bank.generate_new_artifacts()

                self.current_player.choices.append("Защитил деревню")
                self.current_player.story_progress += 1
            else:
                print("\nВы не смогли защитить деревню...")
                self.current_player.choices.append("Не смог защитить деревню")
        else:
            print("\nВы проходите мимо... Деревня будет разрушена.")
            self.current_player.choices.append("Прошел мимо деревни")

    def story_branch_2(self):
        """Вторая сюжетная ветка - Путь Мага"""
        print("\n" + "=" * 50)
        print("ПУТЬ МАГА: Тайная библиотека")
        print("=" * 50)

        print("\nВы находите древнюю библиотеку, полную магических знаний.")
        print("Стражи библиотеки не пускают вас.")

        choice = input(
            "\n1. Сразиться со стражами\n2. Попробовать договориться\n3. Незаметно проникнуть\nВыберите действие (1-3): ")

        if choice == '1':
            print("\nВы решаете сразиться со стражами!")
            enemy = Enemy("Древний страж", 100, 18, "Магический голем")
            if self.battle(self.current_player.character, enemy):
                print("\nВы побеждаете стражей и получаете доступ к знаниям!")
                print("Вы находите древний артефакт!")

                if not self.artifact_bank.is_empty():
                    artifact = self.artifact_bank.get_artifact(0)
                    self.current_player.artifacts.append(artifact)
                    print(f"Вы получили артефакт: {artifact['name']}!")

                    if self.artifact_bank.is_empty():
                        self.artifact_bank.generate_new_artifacts()

                self.current_player.choices.append("Победил стражей библиотеки")
                self.current_player.story_progress += 2
            else:
                print("\nСтражи слишком сильны...")
                self.current_player.choices.append("Проиграл стражам библиотеки")

        elif choice == '2':
            print("\nВы пытаетесь договориться...")
            if self.current_player.gold >= 50:
                print("Стражи соглашаются пропустить вас за 50 золота.")
                self.current_player.gold -= 50
                print("Вы изучаете древние свитки и улучшаете свои навыки!")
                self.current_player.character.damage += 5
                self.current_player.choices.append("Договорился со стражами")
                self.current_player.story_progress += 1
            else:
                print("У вас недостаточно золота для подкупа!")
                self.current_player.choices.append("Не смог договориться")

        else:
            print("\nВы пытаетесь проникнуть незаметно...")
            if random.random() > 0.5:
                print("Успех! Вы проникаете в библиотеку!")
                print("Вы находите полезный предмет.")
                self.current_player.gold += 30
                self.current_player.choices.append("Проник в библиотеку")
                self.current_player.story_progress += 1
            else:
                print("Вас обнаружили! Приходится сражаться!")
                enemy = Enemy("Бдительный страж", 60, 12, "Голем")
                if self.battle(self.current_player.character, enemy):
                    print("Вы побеждаете, но поднимаете тревогу!")
                    self.current_player.choices.append("Обнаружен в библиотеке")
                else:
                    print("Вас захватывают в плен!")
                    self.current_player.choices.append("Попал в плен в библиотеке")

    def story_branch_3(self):
        """Третья сюжетная ветка - Путь Исследователя"""
        print("\n" + "=" * 50)
        print("ПУТЬ ИССЛЕДОВАТЕЛЯ: Затерянные руины")
        print("=" * 50)

        print("\nВы обнаруживаете древние руины, полные опасностей и сокровищ.")
        print("На входе видите несколько путей.")

        choice = input(
            "\n1. Идти прямо в главный зал\n2. Исследовать боковые коридоры\n3. Подняться на верхние уровни\nВыберите путь (1-3): ")

        if choice == '1':
            print("\nВы идете прямо в главный зал...")
            print("Там вас ждет древний хранитель руин!")
            enemy = Enemy("Хранитель руин", 120, 20, "Древний дух")

            if self.battle(self.current_player.character, enemy):
                print("\nВы побеждаете хранителя и находите сокровищницу!")
                print("Вы получаете 100 золота и 2 артефакта!")
                self.current_player.gold += 100

                # Получаем два артефакта
                for _ in range(2):
                    if not self.artifact_bank.is_empty():
                        artifact = self.artifact_bank.get_artifact(0)
                        self.current_player.artifacts.append(artifact)
                        print(f"Вы получили артефакт: {artifact['name']}!")

                        if self.artifact_bank.is_empty():
                            self.artifact_bank.generate_new_artifacts()

                self.current_player.choices.append("Победил хранителя руин")
                self.current_player.story_progress += 3
            else:
                print("\nХранитель слишком силен...")
                self.current_player.choices.append("Проиграл хранителю руин")

        elif choice == '2':
            print("\nВы исследуете боковые коридоры...")
            print("Находите несколько ловушек и небольших сокровищ.")

            if random.random() > 0.3:
                print("Вы успешно обходите ловушки!")
                print("Находите 70 золота и артефакт!")
                self.current_player.gold += 70

                if not self.artifact_bank.is_empty():
                    artifact = self.artifact_bank.get_artifact(0)
                    self.current_player.artifacts.append(artifact)
                    print(f"Вы получили артефакт: {artifact['name']}!")

                    if self.artifact_bank.is_empty():
                        self.artifact_bank.generate_new_artifacts()

                self.current_player.choices.append("Исследовал коридоры руин")
                self.current_player.story_progress += 2
            else:
                print("Вы попадаете в ловушку!")
                damage = 30
                self.current_player.character.health -= damage
                print(f"Вы получаете {damage} урона!")
                self.current_player.choices.append("Попал в ловушку в руинах")

        else:
            print("\nВы поднимаетесь на верхние уровни...")
            print("Там вы находите обсерваторию с древними приборами.")

            print("\nЧто будете делать?")
            sub_choice = input("1. Изучить приборы\n2. Взять все ценности\n3. Уйти quietly\nВыберите действие (1-3): ")

            if sub_choice == '1':
                print("Вы изучаете приборы и получаете новые знания!")
                print("Ваши характеристики улучшаются!")
                self.current_player.character.max_health += 20
                self.current_player.character.health += 20
                self.current_player.character.damage += 3
                self.current_player.choices.append("Изучил приборы в обсерватории")
                self.current_player.story_progress += 2

            elif sub_choice == '2':
                print("Вы собираете все ценности...")
                print("Но внезапно активируется защитный механизм!")
                enemy = Enemy("Защитный голем", 90, 16, "Механизм")

                if self.battle(self.current_player.character, enemy):
                    print("Вы побеждаете голема и забираете сокровища!")
                    self.current_player.gold += 150
                    self.current_player.choices.append("Забрал сокровища из обсерватории")
                    self.current_player.story_progress += 2
                else:
                    print("Голем побеждает вас...")
                    self.current_player.choices.append("Проиграл голему в обсерватории")

            else:
                print("Вы тихо уходите, ничего не трогая...")
                self.current_player.choices.append("Ушел из обсерватории")

    def view_character_info(self):
        """Показывает информацию о персонаже"""
        if not self.current_player or not self.current_player.character:
            print("У вас нет персонажа!")
            return

        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О ПЕРСОНАЖЕ")
        print("=" * 50)
        print(self.current_player.character)
        print(f"Золото: {self.current_player.gold}")
        print(f"Локация: {self.current_player.location}")
        print(f"Прогресс сюжета: {self.current_player.story_progress}")

        if self.current_player.artifacts:
            print("\nАртефакты:")
            for artifact in self.current_player.artifacts:
                print(f"  - {artifact['name']} (+{artifact['power']} силы)")
        else:
            print("\nАртефакты: нет")

        if self.current_player.choices:
            print("\nСделанные выборы:")
            for choice in self.current_player.choices[-5:]:  # Последние 5 выборов
                print(f"  - {choice}")

    def show_menu(self):
        """Показывает главное меню"""
        while True:
            print("\n" + "=" * 50)
            print("ГЛАВНОЕ МЕНЮ")
            print("=" * 50)
            print("1. Начать новую игру")
            print("2. Загрузить игру")
            print("3. Посмотреть артефакты в копилке")
            print("4. Выход")

            choice = input("\nВыберите действие (1-4): ")

            if choice == '1':
                self.start_new_game()
            elif choice == '2':
                self.load_existing_game()
            elif choice == '3':
                self.artifact_bank.view_artifacts()
            elif choice == '4':
                print("До свидания!")
                break
            else:
                print("Неверный выбор!")

    def start_new_game(self):
        """Начинает новую игру"""
        print("\n" + "=" * 50)
        print("НОВАЯ ИГРА")
        print("=" * 50)

        # Регистрация или вход
        auth_choice = input("1. Зарегистрироваться\n2. Войти\nВыберите действие (1-2): ")

        if auth_choice == '1':
            username = self.register_user()
            if not username:
                return
        elif auth_choice == '2':
            username = self.login_user()
            if not username:
                return
        else:
            print("Неверный выбор!")
            return

        # Создание персонажа
        character = self.create_character()
        self.current_player = Player(username, character)

        # Начало игры
        self.game_loop()

    def load_existing_game(self):
        """Загружает существующую игру"""
        print("\n" + "=" * 50)
        print("ЗАГРУЗКА ИГРЫ")
        print("=" * 50)

        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        # Проверка пароля
        users = self.load_users()
        if username not in users or users[username] != password:
            print("Неверное имя пользователя или пароль!")
            return

        # Загрузка игры
        self.current_player = self.load_game(username)
        if self.current_player:
            print(f"\nИгра для {username} успешно загружена!")
            self.game_loop()
        else:
            print("Сохранение не найдено!")

    def game_loop(self):
        """Основной игровой цикл"""
        while True:
            print("\n" + "=" * 50)
            print(f"ИГРА: {self.current_player.username}")
            print(f"Персонаж: {self.current_player.character.name}")
            print("=" * 50)

            print("\n1. Продолжить историю")
            print("2. Просмотреть информацию о персонаже")
            print("3. Посмотреть артефакты в копилке")
            print("4. Сохранить игру")
            print("5. Выйти в главное меню (прогресс не сохранится!)")

            choice = input("\nВыберите действие (1-5): ")

            if choice == '1':
                self.continue_story()
            elif choice == '2':
                self.view_character_info()
            elif choice == '3':
                self.artifact_bank.view_artifacts()
            elif choice == '4':
                self.save_game(self.current_player)
            elif choice == '5':
                print("\nВы выходите без сохранения...")
                print("Прогресс будет потерян, а артефакты вернутся в копилку!")

                confirm = input("Вы уверены? (да/нет): ")
                if confirm.lower() == 'да':
                    # Возвращаем артефакты в копилку
                    if self.current_player.artifacts:
                        self.artifact_bank.return_artifacts(self.current_player.artifacts)
                        print(f"{len(self.current_player.artifacts)} артефактов возвращены в копилку!")

                    print("Выход в главное меню...")
                    break
            else:
                print("Неверный выбор!")

    def continue_story(self):
        """Продолжение сюжета"""
        print("\n" + "=" * 50)
        print("ПРОДОЛЖЕНИЕ ИСТОРИИ")
        print("=" * 50)

        print("\nВыберите сюжетную линию:")
        print("1. Путь Воина - Защита деревни")
        print("2. Путь Мага - Тайная библиотека")
        print("3. Путь Исследователя - Затерянные руины")

        choice = input("\nВыберите путь (1-3): ")

        if choice == '1':
            self.story_branch_1()
        elif choice == '2':
            self.story_branch_2()
        elif choice == '3':
            self.story_branch_3()
        else:
            print("Неверный выбор!")


def main():
    """Главная функция"""
    print("=" * 50)
    print("ДОБРО ПОЖАЛОВАТЬ В RPG ИГРУ!")
    print("=" * 50)

    game = Game()
    game.show_menu()


if __name__ == "__main__":
    main()