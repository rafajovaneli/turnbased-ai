#!/usr/bin/env python3
"""
Demonstração da IA Neural no jogo de combate por turnos
"""

import sys
from game import run_game_with_neural_ai, run_game_with_minimax, run_window_manager
from game.neural_ai import create_neural_ai
from game.config import GAME_CONFIG

def demo_neural_ai():
    """Demonstra as capacidades da IA Neural"""
    print("🧠 DEMONSTRAÇÃO DA IA NEURAL")
    print("=" * 50)
    
    # Cria instância da IA Neural
    neural_ai = create_neural_ai()
    
    # Mostra estatísticas iniciais
    stats = neural_ai.get_performance_stats()
    print(f"📊 Estatísticas Iniciais:")
    print(f"   • Experiências: {stats['experience_count']}")
    print(f"   • Épocas de treinamento: {stats['training_epochs']}")
    print(f"   • Modelo existe: {stats['model_exists']}")
    
    print("\n🎮 Testando decisões da IA Neural:")
    print("-" * 30)
    
    # Testa algumas decisões
    test_scenarios = [
        {"player_hp": 300, "enemy_hp": 300, "desc": "Início do jogo"},
        {"player_hp": 100, "enemy_hp": 200, "desc": "Jogador em desvantagem"},
        {"player_hp": 50, "enemy_hp": 50, "desc": "Ambos com HP baixo"},
        {"player_hp": 250, "enemy_hp": 100, "desc": "Jogador em vantagem"},
        {"player_hp": 30, "enemy_hp": 200, "desc": "Situação crítica"}
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        action = neural_ai.decide_action(
            scenario["player_hp"], 
            scenario["enemy_hp"], 
            turn_count=i
        )
        
        print(f"{i}. {scenario['desc']}")
        print(f"   Player HP: {scenario['player_hp']}, Enemy HP: {scenario['enemy_hp']}")
        print(f"   IA escolheu: {action}")
        
        # Simula aprendizado
        result_score = 0.5 if action == "attack" else 0.2
        neural_ai.learn_from_experience(
            scenario["player_hp"], scenario["enemy_hp"],
            action, result_score, turn_count=i
        )
        print(f"   Aprendizado aplicado (score: {result_score})")
        print()
    
    # Estatísticas finais
    final_stats = neural_ai.get_performance_stats()
    print(f"📊 Estatísticas Finais:")
    print(f"   • Experiências: {final_stats['experience_count']}")
    print(f"   • Diferença: +{final_stats['experience_count'] - stats['experience_count']}")
    
    print("\n" + "=" * 50)
    print("Demonstração concluída!")

def menu_principal():
    """Menu principal da demonstração"""
    while True:
        print("\n🎮 DEMONSTRAÇÃO - COMBATE POR TURNOS COM IA NEURAL")
        print("=" * 55)
        print("1. 🧠 Testar IA Neural (Console)")
        print("2. 🎯 Testar IA Minimax (Console)")
        print("3. 🖥️  Interface Gráfica Completa")
        print("4. 📊 Demonstração da IA Neural")
        print("5. ⚙️  Configurações Atuais")
        print("6. ❌ Sair")
        print("-" * 55)
        
        try:
            escolha = input("Escolha uma opção (1-6): ").strip()
            
            if escolha == "1":
                print("\n🧠 Iniciando jogo com IA Neural...")
                run_game_with_neural_ai()
                
            elif escolha == "2":
                print("\n🎯 Iniciando jogo com IA Minimax...")
                run_game_with_minimax()
                
            elif escolha == "3":
                print("\n🖥️ Abrindo interface gráfica...")
                run_window_manager()
                
            elif escolha == "4":
                demo_neural_ai()
                
            elif escolha == "5":
                mostrar_configuracoes()
                
            elif escolha == "6":
                print("\n👋 Obrigado por testar!")
                break
                
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

def mostrar_configuracoes():
    """Mostra configurações atuais do jogo"""
    print("\n⚙️ CONFIGURAÇÕES ATUAIS")
    print("=" * 30)
    
    print("🎮 Configurações de Jogo:")
    print(f"   • HP Máximo: {GAME_CONFIG['MAX_HP']}")
    print(f"   • Ataque Jogador: {GAME_CONFIG['PLAYER_ATTACK']}")
    print(f"   • Ataque IA: {GAME_CONFIG['AI_ATTACK']}")
    print(f"   • Defesa Jogador: {GAME_CONFIG['PLAYER_DEFENSE']}")
    print(f"   • Defesa IA: {GAME_CONFIG['AI_DEFENSE']}")
    
    print("\n🤖 Configurações de IA:")
    print(f"   • Tipo de IA: {GAME_CONFIG['AI_TYPE']}")
    print(f"   • Profundidade Minimax: {GAME_CONFIG['MINIMAX_DEPTH']}")
    print(f"   • Aprendizado Neural: {GAME_CONFIG['NEURAL_LEARNING']}")
    
    print("\n💚 Configurações de Cura:")
    print(f"   • Cura Mínima: {GAME_CONFIG['HEAL_MIN']}")
    print(f"   • Cura Máxima: {GAME_CONFIG['HEAL_MAX']}")
    
    print("\n🎯 Níveis de Dificuldade:")
    for nivel, config in GAME_CONFIG['DIFFICULTY_LEVELS'].items():
        print(f"   • {nivel}: Ataque={config['AI_ATTACK']}, Profundidade={config['MINIMAX_DEPTH']}")

if __name__ == "__main__":
    try:
        menu_principal()
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)