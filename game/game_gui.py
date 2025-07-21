import tkinter as tk
from tkinter import ttk
import random
import os
import numpy as np
from .config import GUI_CONFIG, GAME_CONFIG
from .entities import Character
from .minimax import minimax, BattleState
from .neural_ai import create_neural_ai

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class GameGUI:
    def __init__(self, root, ai_type=None):
        self.root = root
        self.root.title(GUI_CONFIG['WINDOW_TITLE'])
        self.root.geometry(f"{GUI_CONFIG['WINDOW_WIDTH']}x{GUI_CONFIG['WINDOW_HEIGHT']}")

        # Configuração da IA
        self.ai_type = ai_type or GAME_CONFIG['AI_TYPE']
        self.neural_ai = None
        self.turn_count = 1
        self.game_history = []
        
        # Inicializa IA Neural se necessário
        if self.ai_type == 'NEURAL':
            self.neural_ai = create_neural_ai()
            print("🧠 IA Neural carregada na GUI!")

        # Usa configurações centralizadas
        self.max_hp = GAME_CONFIG['MAX_HP']
        
        # Cria personagens usando a classe Character
        self.player = Character("Jogador", self.max_hp, GAME_CONFIG['PLAYER_ATTACK'], GAME_CONFIG['PLAYER_DEFENSE'])
        self.enemy = Character("Inimigo", self.max_hp, GAME_CONFIG['AI_ATTACK'], GAME_CONFIG['AI_DEFENSE'])

        # Carrega imagens com tratamento de erro
        self.load_images()
        self.setup_ui()

    def load_images(self):
        """Carrega imagens com tratamento de erro"""
        self.hero_img = None
        self.villain_img = None
        
        if PIL_AVAILABLE:
            try:
                hero_path = os.path.join("game", "assets", "hero.png")
                villain_path = os.path.join("game", "assets", "villain.png")
                
                if os.path.exists(hero_path):
                    self.hero_img = ImageTk.PhotoImage(
                        Image.open(hero_path).resize(GUI_CONFIG['IMAGE_SIZE'])
                    )
                if os.path.exists(villain_path):
                    self.villain_img = ImageTk.PhotoImage(
                        Image.open(villain_path).resize(GUI_CONFIG['IMAGE_SIZE'])
                    )
            except Exception as e:
                print(f"Erro ao carregar imagens: {e}")
        
        # Fallback para texto se não conseguir carregar imagens
        if not self.hero_img:
            self.hero_img = "🦸"
        if not self.villain_img:
            self.villain_img = "👹"

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Labels para personagens (com fallback para texto)
        if isinstance(self.hero_img, str):
            self.hero_label = tk.Label(frame, text=self.hero_img, font=("Arial", 24))
        else:
            self.hero_label = tk.Label(frame, image=self.hero_img)
        self.hero_label.grid(row=0, column=0, padx=10)

        if isinstance(self.villain_img, str):
            self.villain_label = tk.Label(frame, text=self.villain_img, font=("Arial", 24))
        else:
            self.villain_label = tk.Label(frame, image=self.villain_img)
        self.villain_label.grid(row=0, column=2, padx=10)

        # Labels de HP
        self.player_hp_label = tk.Label(frame, text=f"Jogador: {self.player.hp}/{self.max_hp}")
        self.player_hp_label.grid(row=1, column=0, pady=5)

        self.enemy_hp_label = tk.Label(frame, text=f"Inimigo: {self.enemy.hp}/{self.max_hp}")
        self.enemy_hp_label.grid(row=1, column=2, pady=5)

        # Barras de HP
        self.player_hp_bar = ttk.Progressbar(frame, length=GUI_CONFIG['HP_BAR_LENGTH'], 
                                           maximum=self.max_hp, style="Green.Horizontal.TProgressbar")
        self.player_hp_bar.grid(row=2, column=0, pady=5)

        self.enemy_hp_bar = ttk.Progressbar(frame, length=GUI_CONFIG['HP_BAR_LENGTH'], 
                                          maximum=self.max_hp, style="Green.Horizontal.TProgressbar")
        self.enemy_hp_bar.grid(row=2, column=2, pady=5)

        # Botões de ação
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=20)

        self.attack_btn = tk.Button(btn_frame, text="⚔️ Atacar", command=self.attack, width=10)
        self.attack_btn.pack(side="left", padx=5)

        self.defend_btn = tk.Button(btn_frame, text="🛡️ Defender", command=self.defend, width=10)
        self.defend_btn.pack(side="left", padx=5)

        self.heal_btn = tk.Button(btn_frame, text="💚 Curar", command=self.heal, width=10)
        self.heal_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(btn_frame, text="🔄 Reiniciar", command=self.reset, width=10)
        self.reset_btn.pack(side="left", padx=5)

        # Log de combate
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)

        tk.Label(log_frame, text="Log de Combate:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.log = tk.Text(log_frame, height=12, width=70, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=scrollbar.set)
        
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.update_display()
        
        # Adiciona informação sobre o tipo de IA
        ai_info = f"🤖 IA: {self.ai_type}"
        if self.ai_type == 'NEURAL' and self.neural_ai:
            stats = self.neural_ai.get_performance_stats()
            ai_info += f" (Exp: {stats['experience_count']})"
        
        self.log_message(ai_info)

    def log_message(self, msg):
        """Adiciona mensagem ao log de combate"""
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def animate_bar(self, bar, color="Red"):
        """Anima a barra de HP com mudança de cor temporária"""
        original_style = bar.cget("style")
        bar.config(style=f"{color}.Horizontal.TProgressbar")
        self.root.after(500, lambda: bar.config(style=original_style))

    def update_display(self):
        """Atualiza todas as informações visuais"""
        # Atualiza labels de HP
        self.player_hp_label.config(text=f"Jogador: {self.player.hp}/{self.max_hp}")
        self.enemy_hp_label.config(text=f"Inimigo: {self.enemy.hp}/{self.max_hp}")
        
        # Atualiza barras de HP
        self.player_hp_bar["value"] = self.player.hp
        self.enemy_hp_bar["value"] = self.enemy.hp

    def attack(self):
        """Executa ataque do jogador"""
        if not self.player.is_alive() or not self.enemy.is_alive():
            return
            
        # Reset status de defesa
        self.player.reset_turn()
        self.enemy.reset_turn()
        
        # Jogador ataca
        damage = self.player.attack(self.enemy)
        self.log_message(f"⚔️ Você atacou causando {damage} de dano!")
        
        self.animate_bar(self.enemy_hp_bar, "Red")
        self.update_display()
        
        if self.check_end():
            return
            
        # Turno do inimigo
        self.root.after(1000, self.enemy_turn)

    def defend(self):
        """Executa defesa do jogador"""
        if not self.player.is_alive() or not self.enemy.is_alive():
            return
            
        # Reset status de defesa
        self.player.reset_turn()
        self.enemy.reset_turn()
        
        self.player.defend()
        self.log_message("🛡️ Você se defendeu!")
        
        # Turno do inimigo
        self.root.after(1000, self.enemy_turn)

    def heal(self):
        """Executa cura do jogador"""
        if not self.player.is_alive() or not self.enemy.is_alive():
            return
            
        # Reset status de defesa
        self.player.reset_turn()
        self.enemy.reset_turn()
        
        healing = self.player.heal()
        self.log_message(f"💚 Você se curou em {healing} pontos!")
        
        self.animate_bar(self.player_hp_bar, "Green")
        self.update_display()
        
        if self.check_end():
            return
            
        # Turno do inimigo
        self.root.after(1000, self.enemy_turn)

    def enemy_turn(self):
        """Executa turno do inimigo usando IA selecionada"""
        if not self.player.is_alive() or not self.enemy.is_alive():
            return
            
        self.log_message("🤖 IA está pensando...")
        
        # Salva estado antes da ação (para aprendizado)
        pre_action_state = {
            'player_hp': self.player.hp,
            'enemy_hp': self.enemy.hp,
            'player_defending': self.player.is_defending,
            'enemy_defending': self.enemy.is_defending,
            'turn': self.turn_count
        }
        
        # Escolhe ação baseada no tipo de IA
        if self.ai_type == 'NEURAL' and self.neural_ai:
            ai_action = self.neural_ai.decide_action(
                self.player.hp, self.enemy.hp,
                self.player.is_defending, self.enemy.is_defending,
                self.turn_count
            )
        else:
            # Usa Minimax
            state = BattleState(
                self.player.hp, 
                self.enemy.hp, 
                player_turn=False,
                player_defending=self.player.is_defending,
                enemy_defending=self.enemy.is_defending
            )
            _, ai_action = minimax(state, depth=GAME_CONFIG['MINIMAX_DEPTH'], maximizing_player=True)
        
        # Executa ação da IA
        damage_dealt = 0
        healing_done = 0
        
        if ai_action == "attack":
            damage_dealt = self.enemy.attack(self.player)
            self.log_message(f"👹 Inimigo atacou causando {damage_dealt} de dano!")
            self.animate_bar(self.player_hp_bar, "Red")
        elif ai_action == "heal":
            healing_done = self.enemy.heal()
            self.log_message(f"👹 Inimigo se curou em {healing_done} pontos!")
            self.animate_bar(self.enemy_hp_bar, "Green")
        elif ai_action == "defend":
            self.enemy.defend()
            self.log_message("👹 Inimigo se defendeu!")
        
        # Aprendizado da IA Neural
        if self.ai_type == 'NEURAL' and self.neural_ai and GAME_CONFIG['NEURAL_LEARNING']:
            result_score = self.calculate_action_score(
                pre_action_state, ai_action, damage_dealt, healing_done
            )
            
            self.neural_ai.learn_from_experience(
                pre_action_state['player_hp'], pre_action_state['enemy_hp'],
                ai_action, result_score,
                pre_action_state['player_defending'], pre_action_state['enemy_defending'],
                self.turn_count
            )
        
        # Salva no histórico
        self.game_history.append({
            'turn': self.turn_count,
            'ai_action': ai_action,
            'damage_dealt': damage_dealt,
            'healing_done': healing_done,
            'player_hp_after': self.player.hp,
            'enemy_hp_after': self.enemy.hp
        })
        
        self.turn_count += 1
        self.update_display()
        self.check_end()
    
    def calculate_action_score(self, pre_state, action, damage_dealt, healing_done):
        """Calcula score para uma ação da IA (para aprendizado)"""
        score = 0.0
        
        # Recompensas baseadas na ação
        if action == "attack" and damage_dealt > 0:
            score += damage_dealt / 30.0  # Normaliza dano
            if self.player.hp <= 0:  # Matou o jogador
                score += 2.0
        
        elif action == "heal" and healing_done > 0:
            if pre_state['enemy_hp'] < GAME_CONFIG['MAX_HP'] * 0.5:  # HP baixo
                score += healing_done / 20.0
            else:  # HP alto, cura desnecessária
                score -= 0.5
        
        elif action == "defend":
            if pre_state['enemy_hp'] < GAME_CONFIG['MAX_HP'] * 0.3:  # HP muito baixo
                score += 0.5
            else:
                score += 0.1  # Defesa sempre tem valor pequeno
        
        # Penalidades
        if self.enemy.hp <= 0:  # IA morreu
            score -= 2.0
        
        # Bônus por diferença de HP
        hp_diff = self.enemy.hp - self.player.hp
        score += hp_diff / GAME_CONFIG['MAX_HP']
        
        return np.clip(score, -2.0, 2.0)  # Limita score entre -2 e 2

    def check_end(self):
        """Verifica se o jogo terminou"""
        if not self.player.is_alive():
            self.log_message("💀 Você perdeu!")
            self.disable_actions()
            return True
        elif not self.enemy.is_alive():
            self.log_message("🎉 Você venceu!")
            self.disable_actions()
            return True
        return False

    def disable_actions(self):
        self.attack_btn.config(state="disabled")
        self.defend_btn.config(state="disabled")
        self.heal_btn.config(state="disabled")

    def enable_actions(self):
        self.attack_btn.config(state="normal")
        self.defend_btn.config(state="normal")
        self.heal_btn.config(state="normal")

    def reset(self):
        """Reinicia o jogo"""
        # Recria os personagens
        self.player = Character("Jogador", self.max_hp, GAME_CONFIG['PLAYER_ATTACK'], GAME_CONFIG['PLAYER_DEFENSE'])
        self.enemy = Character("Inimigo", self.max_hp, GAME_CONFIG['AI_ATTACK'], GAME_CONFIG['AI_DEFENSE'])
        
        # Atualiza display
        self.update_display()
        
        # Limpa o log
        self.log.delete(1.0, tk.END)
        self.log_message("🔄 Jogo reiniciado!")
        
        # Reabilita ações
        self.enable_actions()

def run_gui():
    """Função para executar a GUI"""
    root = tk.Tk()

    # Configura estilos das barras de progresso
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Green.Horizontal.TProgressbar", troughcolor='lightgray', background='green')
    style.configure("Red.Horizontal.TProgressbar", troughcolor='lightgray', background='red')

    game = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
