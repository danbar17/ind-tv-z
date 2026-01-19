import json
import random
import os


class ArtifactBank:
    """Копилка артефактов"""

    def __init__(self, filename='artifacts.json'):
        self.filename = filename
        self.artifacts = self.load_artifacts()

        # Если файл не существует или пустой, генерируем начальные артефакты
        if not self.artifacts:
            self.generate_initial_artifacts()

    def load_artifacts(self):
        """Загружает артефакты из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_artifacts(self):
        """Сохраняет артефакты в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.artifacts, f, ensure_ascii=False, indent=2)

    def generate_initial_artifacts(self):
        """Генерирует начальные артефакты"""
        artifact_templates = [
            {"name": "Меч Драконоборца", "type": "weapon", "power": 15, "value": 100},
            {"name": "Щит Небесного Стража", "type": "shield", "power": 10, "value": 80},
            {"name": "Амулет Вечной Жизни", "type": "amulet", "power": 20, "value": 150},
            {"name": "Кольцо Огня", "type": "ring", "power": 12, "value": 70},
            {"name": "Плащ Теней", "type": "cloak", "power": 8, "value": 60},
            {"name": "Ботинки Скорости", "type": "boots", "power": 5, "value": 40},
            {"name": "Посох Арканы", "type": "staff", "power": 18, "value": 120},
            {"name": "Лук Эльфийского Леса", "type": "bow", "power": 14, "value": 90},
        ]

        self.artifacts = random.sample(artifact_templates, 5)
        self.save_artifacts()

    def generate_new_artifacts(self):
        """Генерирует новые артефакты, когда все забраны"""
        print("\n" + "=" * 50)
        print("ВСЕ АРТЕФАКТЫ НАЙДЕНЫ!")
        print("Генерация новых артефактов...")
        print("=" * 50)

        new_artifacts = [
            {"name": "Легендарный Меч Света", "type": "weapon", "power": 25, "value": 200},
            {"name": "Доспехи Древнего Бога", "type": "armor", "power": 30, "value": 250},
            {"name": "Артефакт Забытой Цивилизации", "type": "artifact", "power": 35, "value": 300},
            {"name": "Кристалл Вечной Магии", "type": "crystal", "power": 22, "value": 180},
            {"name": "Перо Феникса", "type": "feather", "power": 18, "value": 160},
            {"name": "Коготь Дракона", "type": "claw", "power": 28, "value": 220},
            {"name": "Сфера Предвидения", "type": "orb", "power": 20, "value": 170},
            {"name": "Сердце Вулкана", "type": "heart", "power": 32, "value": 280},
        ]

        self.artifacts = random.sample(new_artifacts, 6)
        self.save_artifacts()

        print(f"Сгенерировано {len(self.artifacts)} новых артефактов!")
        for artifact in self.artifacts:
            print(f"  - {artifact['name']} (+{artifact['power']} силы)")

    def get_artifact(self, index):
        """Получает артефакт по индексу"""
        if 0 <= index < len(self.artifacts):
            return self.artifacts.pop(index)
        return None

    def return_artifacts(self, artifacts_list):
        """Возвращает артефакты в копилку"""
        self.artifacts.extend(artifacts_list)
        self.save_artifacts()

    def view_artifacts(self):
        """Показывает все доступные артефакты"""
        if not self.artifacts:
            print("Копилка артефактов пуста!")
            return

        print("\n" + "=" * 50)
        print("ДОСТУПНЫЕ АРТЕФАКТЫ:")
        print("=" * 50)
        for i, artifact in enumerate(self.artifacts, 1):
            print(f"{i}. {artifact['name']}")
            print(f"   Тип: {artifact['type']}")
            print(f"   Сила: +{artifact['power']}")
            print(f"   Стоимость: {artifact['value']} золота")
            print()

    def is_empty(self):
        """Проверяет, пуста ли копилка"""
        return len(self.artifacts) == 0