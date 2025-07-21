import random
from .config import GAME_CONFIG


class Character:
    def __init__(self, name, hp, atk, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.is_defending = False

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        # Usa o ataque base do personagem com variação aleatória
        base_damage = self.atk
        variation = random.randint(-5, 5)
        damage = max(1, base_damage + variation)

        # Se o alvo está defendendo, reduz o dano
        if target.is_defending:
            damage = max(1, damage - target.defense)

        target.hp = max(0, target.hp - damage)
        print(f"{self.name} atacou {target.name} causando {damage} de dano!")
        return damage

    def defend(self):
        self.is_defending = True
        print(f"{self.name} entrou em modo de defesa!")

    def heal(self):
        healing = random.randint(GAME_CONFIG['HEAL_MIN'], GAME_CONFIG['HEAL_MAX'])
        self.hp = min(self.max_hp, self.hp + healing)
        print(f"{self.name} se curou em {healing} pontos!")
        return healing

    def reset_turn(self):
        self.is_defending = False
