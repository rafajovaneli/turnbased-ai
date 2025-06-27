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
        # Reduz dano se o alvo estiver defendendo
        damage = self.atk - (target.defense if not target.is_defending else target.defense * 2)
        damage = max(1, damage)
        target.hp -= damage
        print(f"{self.name} atacou {target.name} causando {damage} de dano!")
        return damage

    def defend(self):
        self.is_defending = True
        print(f"{self.name} entrou em modo de defesa!")

    def heal(self):
        healing = 10
        self.hp = min(self.max_hp, self.hp + healing)
        print(f"{self.name} se curou em {healing} pontos!")

    def reset_turn(self):
        self.is_defending = False
