import unittest
from game.entities import Character
from game.minimax import BattleState, minimax
from game.config import GAME_CONFIG

class TestGameEngine(unittest.TestCase):

    def test_character_creation(self):
        """Testa criação de personagem"""
        player = Character("Teste", 100, 20, 5)
        self.assertEqual(player.name, "Teste")
        self.assertEqual(player.hp, 100)
        self.assertEqual(player.max_hp, 100)
        self.assertEqual(player.atk, 20)
        self.assertEqual(player.defense, 5)
        self.assertTrue(player.is_alive())

    def test_character_attack(self):
        """Testa sistema de ataque"""
        attacker = Character("Atacante", 100, 20, 5)
        target = Character("Alvo", 100, 15, 3)
        
        initial_hp = target.hp
        damage = attacker.attack(target)
        
        self.assertGreater(damage, 0)
        self.assertEqual(target.hp, initial_hp - damage)

    def test_character_defense(self):
        """Testa sistema de defesa"""
        defender = Character("Defensor", 100, 20, 5)
        attacker = Character("Atacante", 100, 20, 3)
        
        # Sem defesa
        defender_hp = defender.hp
        damage_normal = attacker.attack(defender)
        
        # Reseta HP e testa com defesa
        defender.hp = defender_hp
        defender.defend()
        damage_defended = attacker.attack(defender)
        
        # Dano com defesa deve ser menor
        self.assertLessEqual(damage_defended, damage_normal)

    def test_character_heal(self):
        """Testa sistema de cura"""
        character = Character("Curandeiro", 100, 20, 5)
        character.hp = 50  # Reduz HP
        
        initial_hp = character.hp
        healing = character.heal()
        
        self.assertGreater(healing, 0)
        self.assertEqual(character.hp, min(character.max_hp, initial_hp + healing))

    def test_battle_state_terminal(self):
        """Testa estados terminais do combate"""
        # Jogador morto
        state1 = BattleState(0, 50, True)
        self.assertTrue(state1.is_terminal())
        
        # Inimigo morto
        state2 = BattleState(50, 0, True)
        self.assertTrue(state2.is_terminal())
        
        # Ambos vivos
        state3 = BattleState(50, 50, True)
        self.assertFalse(state3.is_terminal())

    def test_battle_state_evaluation(self):
        """Testa avaliação de estados de combate"""
        # Jogador perdeu
        state1 = BattleState(0, 50, True)
        self.assertEqual(state1.evaluate(), 10000)
        
        # Inimigo perdeu
        state2 = BattleState(50, 0, True)
        self.assertEqual(state2.evaluate(), -10000)
        
        # Estado equilibrado
        state3 = BattleState(50, 50, True)
        self.assertEqual(state3.evaluate(), 0)

    def test_minimax_returns_valid_action(self):
        """Testa se minimax retorna ações válidas"""
        state = BattleState(100, 100, False)  # Turno da IA
        score, action = minimax(state, depth=3, maximizing_player=True)
        
        valid_actions = ['attack', 'heal', 'defend']
        self.assertIn(action, valid_actions)
        self.assertIsInstance(score, (int, float))

    def test_config_values(self):
        """Testa se as configurações estão definidas"""
        self.assertIn('MAX_HP', GAME_CONFIG)
        self.assertIn('PLAYER_ATTACK', GAME_CONFIG)
        self.assertIn('AI_ATTACK', GAME_CONFIG)
        self.assertGreater(GAME_CONFIG['MAX_HP'], 0)
        self.assertGreater(GAME_CONFIG['PLAYER_ATTACK'], 0)

if __name__ == "__main__":
    unittest.main()
