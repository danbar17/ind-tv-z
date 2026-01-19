import json
import os
from abc import ABC, abstractmethod


class Character(ABC):
    """Абстрактный класс персонажа"""

    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.artifacts = []

    @abstractmethod
    def special_ability(self):
        pass

    def attack(self, target):
        damage = self.damage
        target.health -= damage
        return damage

    def is_alive(self):
        return self.health > 0

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        return amount


class Warrior(Character):
    """Класс Воина"""

    def __init__(self, name):
        super().__init__(name, health=120, damage=20)

    def special_ability(self):
        # Урон увеличивается, но снижается здоровье
        self.health -= 5
        return self.damage * 2

    def __str__(self):
        return f"Воин {self.name} (Здоровье: {self.health}/{self.max_health}, Урон: {self.damage})"


class Mage(Character):
    """Класс Мага"""

    def __init__(self, name):
        super().__init__(name, health=80, damage=25)
        self.mana = 100

    def special_ability(self):
        if self.mana >= 20:
            self.mana -= 20
            return self.damage * 3
        return self.damage

    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            damage = self.damage * 1.5
        else:
            damage = self.damage
        target.health -= damage
        return damage

    def __str__(self):
        return f"Маг {self.name} (Здоровье: {self.health}/{self.max_health}, Мана: {self.mana}, Урон: {self.damage})"


class Archer(Character):
    """Класс Лучника"""

    def __init__(self, name):
        super().__init__(name, health=90, damage=22)
        self.arrows = 10

    def special_ability(self):
        if self.arrows > 0:
            self.arrows -= 1
            return self.damage * 2.5
        return self.damage

    def __str__(self):
        return f"Лучник {self.name} (Здоровье: {self.health}/{self.max_health}, Стрелы: {self.arrows}, Урон: {self.damage})"


class Enemy(Character):
    """Класс врага"""

    def __init__(self, name, health, damage, enemy_type):
        super().__init__(name, health, damage)
        self.enemy_type = enemy_type

    def special_ability(self):
        # Простая способность для врага
        return self.damage * 1.5

    def __str__(self):
        return f"{self.enemy_type} {self.name} (Здоровье: {self.health}, Урон: {self.damage})"


class Player:
    """Класс игрока для сохранения прогресса"""

    def __init__(self, username, character=None):
        self.username = username
        self.character = character
        self.artifacts = []
        self.story_progress = 0  # Прогресс сюжета
        self.choices = []  # Сделанные выборы
        self.gold = 100
        self.location = "Начальная деревня"

    def to_dict(self):
        """Конвертирует игрока в словарь для сохранения"""
        return {
            'username': self.username,
            'character': {
                'type': self.character.__class__.__name__,
                'name': self.character.name,
                'health': self.character.health,
                'max_health': self.character.max_health,
                'damage': self.character.damage
            } if self.character else None,
            'artifacts': self.artifacts,
            'story_progress': self.story_progress,
            'choices': self.choices,
            'gold': self.gold,
            'location': self.location
        }

    @staticmethod
    def from_dict(data):
        """Создает игрока из словаря"""
        player = Player(data['username'])
        if data['character']:
            char_data = data['character']
            if char_data['type'] == 'Warrior':
                player.character = Warrior(char_data['name'])
            elif char_data['type'] == 'Mage':
                player.character = Mage(char_data['name'])
            elif char_data['type'] == 'Archer':
                player.character = Archer(char_data['name'])

            player.character.health = char_data['health']
            player.character.max_health = char_data['max_health']
            player.character.damage = char_data['damage']

        player.artifacts = data['artifacts']
        player.story_progress = data['story_progress']
        player.choices = data['choices']
        player.gold = data['gold']
        player.location = data['location']
        return player