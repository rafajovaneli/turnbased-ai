from .config import GAME_CONFIG

class BattleState:
    def __init__(self, player_hp, enemy_hp, player_turn, player_defending=False, enemy_defending=False):
        self.player_hp = player_hp
        self.enemy_hp = enemy_hp
        self.player_turn = player_turn
        self.player_defending = player_defending
        self.enemy_defending = enemy_defending

    def is_terminal(self):
        return self.player_hp <= 0 or self.enemy_hp <= 0

    def evaluate(self):
        if self.player_hp <= 0:
            return 10000  # IA venceu
        elif self.enemy_hp <= 0:
            return -10000  # jogador venceu

        # Avaliação mais balanceada
        hp_diff = self.enemy_hp - self.player_hp
        score = hp_diff * 10
        
        # Bônus por ter mais HP
        if self.enemy_hp > self.player_hp:
            score += 50
        elif self.player_hp > self.enemy_hp:
            score -= 50
            
        return score

    def get_actions(self):
        return ['attack', 'heal', 'defend']

    def apply_action(self, action):
        new_player_hp = self.player_hp
        new_enemy_hp = self.enemy_hp
        new_player_defending = False
        new_enemy_defending = False

        if self.player_turn:
            if action == 'attack':
                damage = GAME_CONFIG['PLAYER_ATTACK']
                if self.enemy_defending:
                    damage = max(1, damage - GAME_CONFIG['AI_DEFENSE'])
                new_enemy_hp = max(0, new_enemy_hp - damage)
            elif action == 'heal':
                healing = (GAME_CONFIG['HEAL_MIN'] + GAME_CONFIG['HEAL_MAX']) // 2
                new_player_hp = min(GAME_CONFIG['MAX_HP'], new_player_hp + healing)
            elif action == 'defend':
                new_player_defending = True
        else:
            if action == 'attack':
                damage = GAME_CONFIG['AI_ATTACK']
                if self.player_defending:
                    damage = max(1, damage - GAME_CONFIG['PLAYER_DEFENSE'])
                new_player_hp = max(0, new_player_hp - damage)
            elif action == 'heal':
                healing = (GAME_CONFIG['HEAL_MIN'] + GAME_CONFIG['HEAL_MAX']) // 2
                new_enemy_hp = min(GAME_CONFIG['MAX_HP'], new_enemy_hp + healing)
            elif action == 'defend':
                new_enemy_defending = True

        return BattleState(
            new_player_hp,
            new_enemy_hp,
            not self.player_turn,
            player_defending=new_player_defending,
            enemy_defending=new_enemy_defending
        )

def minimax(state, depth, maximizing_player):
    if state.is_terminal() or depth == 0:
        return state.evaluate(), None

    best_action = None

    if maximizing_player:
        max_eval = float('-inf')
        for action in state.get_actions():
            new_state = state.apply_action(action)
            eval_score, _ = minimax(new_state, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_action = action
        return max_eval, best_action

    else:
        min_eval = float('inf')
        for action in state.get_actions():
            new_state = state.apply_action(action)
            eval_score, _ = minimax(new_state, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_action = action
        return min_eval, best_action


__all__ = ["minimax", "BattleState"]