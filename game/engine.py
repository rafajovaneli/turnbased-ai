import numpy as np
from .entities import Character
from .minimax import minimax, BattleState
from .neural_ai import create_neural_ai
from .config import GAME_CONFIG

def draw_health_bar(name, hp, max_hp=None, bar_length=None):
    """Desenha uma barra de HP visual no console"""
    if max_hp is None:
        max_hp = GAME_CONFIG['MAX_HP']
    if bar_length is None:
        bar_length = GAME_CONFIG['HP_BAR_LENGTH']
    
    filled_length = int(bar_length * hp // max_hp) if max_hp > 0 else 0
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    return f"{name} HP: |{bar}| {hp}/{max_hp}"

def run_game(ai_type=None):
    """Executa o jogo principal no console"""
    if ai_type is None:
        ai_type = GAME_CONFIG['AI_TYPE']
    
    print("⚔️  Início do combate por turnos!")
    print(f"🤖 Tipo de IA: {ai_type}")

    # Usa configurações centralizadas
    max_hp = GAME_CONFIG['MAX_HP']
    player = Character("Jogador", max_hp, GAME_CONFIG['PLAYER_ATTACK'], GAME_CONFIG['PLAYER_DEFENSE'])
    ai_character = Character("Inimigo", max_hp, GAME_CONFIG['AI_ATTACK'], GAME_CONFIG['AI_DEFENSE'])

    # Inicializa IA Neural se necessário
    neural_ai = None
    if ai_type == 'NEURAL':
        neural_ai = create_neural_ai()
        print("🧠 IA Neural carregada!")

    turn = 1
    game_history = []  # Para aprendizado da IA neural
    
    while player.is_alive() and ai_character.is_alive():
        print("\n" + "=" * 30)
        print(f"----- TURNO {turn} -----")
        print("=" * 30 + "\n")
        
        print(draw_health_bar(player.name, player.hp))
        print(draw_health_bar(ai_character.name, ai_character.hp))

        # Salva estado antes das ações (para aprendizado)
        pre_action_state = {
            'player_hp': player.hp,
            'ai_hp': ai_character.hp,
            'player_defending': player.is_defending,
            'ai_defending': ai_character.is_defending,
            'turn': turn
        }

        # Reset status de defesa no início do turno
        player.reset_turn()
        ai_character.reset_turn()

        # TURNO DO JOGADOR
        print("\nEscolha sua ação:")
        print("1 - Atacar")
        print("2 - Defender")
        print("3 - Curar")
        
        try:
            action = input("> ").strip()
            
            player_action = None
            if action == "1":
                damage = player.attack(ai_character)
                player_action = "attack"
            elif action == "2":
                player.defend()
                player_action = "defend"
            elif action == "3":
                healing = player.heal()
                player_action = "heal"
            else:
                print("Ação inválida. Você perdeu o turno.")
                player_action = "invalid"
        except KeyboardInterrupt:
            print("\n\nJogo interrompido pelo jogador.")
            return

        if not ai_character.is_alive():
            break

        # TURNO DO INIMIGO
        print("\nIA está pensando...")

        # Escolhe ação baseada no tipo de IA
        if ai_type == 'NEURAL' and neural_ai:
            ai_action = neural_ai.decide_action(
                player.hp, ai_character.hp,
                player.is_defending, ai_character.is_defending,
                turn
            )
        else:
            # Usa Minimax
            state = BattleState(player.hp, ai_character.hp, player_turn=False, 
                              player_defending=player.is_defending, 
                              enemy_defending=ai_character.is_defending)
            _, ai_action = minimax(state, depth=GAME_CONFIG['MINIMAX_DEPTH'], maximizing_player=True)

        print(f"IA escolheu: {ai_action}")

        # Executa ação da IA
        ai_damage_dealt = 0
        ai_healing_done = 0
        
        if ai_action == "attack":
            ai_damage_dealt = ai_character.attack(player)
        elif ai_action == "heal":
            ai_healing_done = ai_character.heal()
        elif ai_action == "defend":
            ai_character.defend()

        # Aprendizado da IA Neural
        if ai_type == 'NEURAL' and neural_ai and GAME_CONFIG['NEURAL_LEARNING']:
            # Calcula score baseado no resultado da ação
            result_score = calculate_action_score(
                pre_action_state, ai_action, ai_damage_dealt, ai_healing_done,
                player.hp, ai_character.hp
            )
            
            neural_ai.learn_from_experience(
                pre_action_state['player_hp'], pre_action_state['ai_hp'],
                ai_action, result_score,
                pre_action_state['player_defending'], pre_action_state['ai_defending'],
                turn
            )

        # Salva histórico do jogo
        game_history.append({
            'turn': turn,
            'player_action': player_action,
            'ai_action': ai_action,
            'player_hp_after': player.hp,
            'ai_hp_after': ai_character.hp
        })

        turn += 1

    # Resultado final
    print("\n🏁 Fim do jogo!")
    game_won = player.is_alive()
    
    if game_won:
        print("🎉 Você venceu!")
    else:
        print("💀 Você perdeu!")
    
    # Aprendizado final da IA Neural
    if ai_type == 'NEURAL' and neural_ai and GAME_CONFIG['NEURAL_LEARNING']:
        final_score = 1.0 if not game_won else -1.0  # IA ganha = +1, perde = -1
        
        # Aprende com o resultado final
        for i, history_entry in enumerate(game_history[-5:]):  # Últimas 5 ações
            weight = (i + 1) / 5  # Ações mais recentes têm mais peso
            neural_ai.learn_from_experience(
                history_entry['player_hp_after'], history_entry['ai_hp_after'],
                history_entry['ai_action'], final_score * weight,
                turn_count=history_entry['turn']
            )
        
        print(f"🧠 IA Neural aprendeu com este jogo!")
        stats = neural_ai.get_performance_stats()
        print(f"📊 Experiências acumuladas: {stats['experience_count']}")


def calculate_action_score(pre_state, action, damage_dealt, healing_done, 
                          player_hp_after, ai_hp_after):
    """Calcula score para uma ação da IA (para aprendizado)"""
    score = 0.0
    
    # Recompensas baseadas na ação
    if action == "attack" and damage_dealt > 0:
        score += damage_dealt / 30.0  # Normaliza dano
        if player_hp_after <= 0:  # Matou o jogador
            score += 2.0
    
    elif action == "heal" and healing_done > 0:
        if pre_state['ai_hp'] < GAME_CONFIG['MAX_HP'] * 0.5:  # HP baixo
            score += healing_done / 20.0
        else:  # HP alto, cura desnecessária
            score -= 0.5
    
    elif action == "defend":
        if pre_state['ai_hp'] < GAME_CONFIG['MAX_HP'] * 0.3:  # HP muito baixo
            score += 0.5
        else:
            score += 0.1  # Defesa sempre tem valor pequeno
    
    # Penalidades
    if ai_hp_after <= 0:  # IA morreu
        score -= 2.0
    
    # Bônus por diferença de HP
    hp_diff = ai_hp_after - player_hp_after
    score += hp_diff / GAME_CONFIG['MAX_HP']
    
    return np.clip(score, -2.0, 2.0)  # Limita score entre -2 e 2


def run_game_with_neural_ai():
    """Executa jogo especificamente com IA Neural"""
    run_game(ai_type='NEURAL')


def run_game_with_minimax():
    """Executa jogo especificamente com Minimax"""
    run_game(ai_type='MINIMAX')
    
if __name__ == "__main__":
    run_game()