import unittest
from game.engine import GameState, minimax

class TestGameEngine(unittest.TestCase):

    def test_initial_state(self):
        state = GameState()
        self.assertEqual(state.player_hp, 10)
        self.assertEqual(state.ai_hp, 10)
        self.assertTrue(state.player_turn)

    def test_terminal_state(self):
        state = GameState(player_hp=0, ai_hp=5)
        self.assertTrue(state.is_terminal())
        state = GameState(player_hp=5, ai_hp=0)
        self.assertTrue(state.is_terminal())

    def test_evaluate(self):
        self.assertEqual(GameState(player_hp=0, ai_hp=5).evaluate(), -1)
        self.assertEqual(GameState(player_hp=5, ai_hp=0).evaluate(), 1)
        self.assertEqual(GameState(player_hp=5, ai_hp=5).evaluate(), 0)

    def test_minimax_ai_wins(self):
        state = GameState(player_hp=1, ai_hp=3, player_turn=False)
        score, action = minimax(state, 3, True)
        self.assertIn(action, ['attack', 'heal'])  # sem comportamento fixo, mas deve ser válido

if __name__ == "__main__":
    unittest.main()
