import random


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
        # Gera dano aleatório entre 0 e 20, com mais chance de ser maior que 10
        damage = random.choices(
            population=range(0, 21),
            weights=[1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            k=1
        )[0]

        # Se o alvo está defendendo, reduz o dano
        if target.is_defending:
            damage = max(1, damage - target.defense)
        else:
            damage = max(1, damage)

        target.hp -= damage
        print(f"{self.name} atacou {target.name} causando {damage} de dano!")
        return damage

    def defend(self):
        self.is_defending = True
        print(f"{self.name} entrou em modo de defesa!")

    def heal(self):
        healing = random.randint(5, 20)
        self.hp = min(self.max_hp, self.hp + healing)
        print(f"{self.name} se curou em {healing} pontos!")

    def reset_turn(self):
        self.is_defending = False
