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

        score = (self.enemy_hp * 2) - (self.player_hp * 1.5)
        if self.enemy_hp > self.player_hp:
            score += 10
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
                damage = 20 if not self.enemy_defending else 10
                new_enemy_hp = max(0, new_enemy_hp - damage)
            elif action == 'heal':
                new_player_hp = min(100, new_player_hp + 10)
            elif action == 'defend':
                new_player_defending = True
        else:
            if action == 'attack':
                damage = 25 if not self.player_defending else 12
                new_player_hp = max(0, new_player_hp - damage)
            elif action == 'heal':
                new_enemy_hp = min(100, new_enemy_hp + 10)
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