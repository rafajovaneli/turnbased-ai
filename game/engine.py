from game.entities import Character
from game.minimax import minimax, BattleState

def draw_health_bar(name, hp, max_hp=300, bar_length=20):
    filled_length = int(bar_length * hp // max_hp)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    return f"{name} HP: |{bar}| {hp}/{max_hp}"

def render_hp_bar(hp, max_hp=300, bar_length=20):
    filled = int((hp / max_hp) * bar_length)
    empty = bar_length - filled
    return "[" + "█" * filled + " " * empty + f"] {hp}/{max_hp}"

def run_game():
    print("⚔️  Início do combate por turnos!")

    player = Character("Jogador", 300, 20, 5)
    ai = Character("Inimigo", 300, 25, 4)

    turn = 1
    while player.is_alive() and ai.is_alive():
        print(f"----- TURNO {turn} -----")
        print(draw_health_bar(player.name, player.hp))
        print(draw_health_bar(ai.name, ai.hp))

        # TURNO DO JOGADOR
        print("Escolha sua ação:")
        print("1 - Atacar")
        print("2 - Defender")
        print("3 - Curar")
        action = input("> ").strip()

        if action == "1":
            player.attack(ai)
        elif action == "2":
            player.defend()
        elif action == "3":
            player.heal()
        else:
            print("Ação inválida. Você perdeu o turno.")

        if not ai.is_alive():
            break

        # TURNO DO INIMIGO
        print("IA está pensando...")

        # Usa Minimax em vez de lógica fixa
        state = BattleState(player.hp, ai.hp, player_turn=False)
        _, ai_action = minimax(state, depth=6, maximizing_player=True)

        print(f"IA escolheu: {ai_action}")  # <-- log útil

        if ai_action == "attack":
            ai.attack(player)
        elif ai_action == "heal":
            ai.heal()

    # Resultado final
    print("🏁 Fim do jogo!")
    if player.is_alive():
        print("🎉 Você venceu!")
    else:
        print("💀 Você perdeu!")
    
if __name__ == "__main__":
    run_game()