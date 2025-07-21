import tkinter as tk
from tkinter import ttk
import random
import os
import time
import threading
import numpy as np
from .config import GUI_CONFIG, GAME_CONFIG, STYLE_CONFIG
from .entities import Character
from .minimax import minimax, BattleState
from .neural_ai import create_neural_ai

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ModernGameGUI:
    """GUI moderna e aprimorada para o jogo"""
    
    def __init__(self, root, ai_type='MINIMAX'):
        self.root = root
        self.ai_type = ai_type
        self.setup_window()
        
        # Estado do jogo
        self.max_hp = GAME_CONFIG['MAX_HP']
        self.turn_count = 1
        self.game_history = []
        self.is_game_active = True
        self.thinking_animation_active = False
        
        # Personagens
        self.player = Character("Jogador", self.max_hp, GAME_CONFIG['PLAYER_ATTACK'], GAME_CONFIG['PLAYER_DEFENSE'])
        self.enemy = Character("IA", self.max_hp, GAME_CONFIG['AI_ATTACK'], GAME_CONFIG['AI_DEFENSE'])
        
        # IA Neural
        self.neural_ai = None
        if self.ai_type == 'NEURAL':
            self.neural_ai = create_neural_ai()
            print(f"🧠 IA Neural carregada! Experiências: {self.neural_ai.get_performance_stats()['experience_count']}")
        
        # Estatísticas da sessão
        self.session_stats = {
            'games_played': 0,
            'games_won': 0,
            'total_damage_dealt': 0,
            'total_damage_received': 0,
            'actions_taken': {'attack': 0, 'defend': 0, 'heal': 0},
            'ai_actions': {'attack': 0, 'defend': 0, 'heal': 0}
        }
        
        self.setup_ui()
        self.start_game()
        
    def setup_window(self):
        """Configura a janela principal"""
        ai_color = STYLE_CONFIG['COLORS']['MINIMAX'] if self.ai_type == 'MINIMAX' else STYLE_CONFIG['COLORS']['NEURAL']
        ai_name = "Minimax" if self.ai_type == 'MINIMAX' else "Neural"
        
        self.root.title(f"⚔️ Combate vs IA {ai_name}")
        self.root.geometry("1000x700")
        self.root.configure(bg=STYLE_CONFIG['COLORS']['LIGHT'])
        self.root.resizable(True, True)
        
        # Centraliza a janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
        
    def setup_ui(self):
        """Configura a interface moderna"""
        # Header com informações da IA
        self.create_header()
        
        # Área principal de combate
        self.create_combat_area()
        
        # Painel lateral com controles e estatísticas
        self.create_side_panel()
        
        # Footer com informações do turno
        self.create_footer()
        
        # Configura estilos
        self.setup_styles()
        
    def create_header(self):
        """Cria o cabeçalho com informações da IA"""
        header_frame = tk.Frame(self.root, bg=STYLE_CONFIG['COLORS']['DARK'], height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título principal
        title_text = f"⚔️ COMBATE POR TURNOS"
        title_label = tk.Label(header_frame, text=title_text,
                              font=STYLE_CONFIG['FONTS']['TITLE'],
                              fg='white', bg=STYLE_CONFIG['COLORS']['DARK'])
        title_label.pack(side="left", padx=20, pady=20)
        
        # Informações da IA
        ai_color = STYLE_CONFIG['COLORS']['MINIMAX'] if self.ai_type == 'MINIMAX' else STYLE_CONFIG['COLORS']['NEURAL']
        ai_icon = "🎯" if self.ai_type == 'MINIMAX' else "🧠"
        ai_name = "Minimax" if self.ai_type == 'MINIMAX' else "Neural"
        
        ai_info_frame = tk.Frame(header_frame, bg=STYLE_CONFIG['COLORS']['DARK'])
        ai_info_frame.pack(side="right", padx=20, pady=10)
        
        ai_label = tk.Label(ai_info_frame, text=f"{ai_icon} IA {ai_name}",
                           font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                           fg=ai_color, bg=STYLE_CONFIG['COLORS']['DARK'])
        ai_label.pack()
        
        # Status da IA
        if self.ai_type == 'NEURAL' and self.neural_ai:
            stats = self.neural_ai.get_performance_stats()
            status_text = f"Experiências: {stats['experience_count']}"
        else:
            status_text = f"Profundidade: {GAME_CONFIG['MINIMAX_DEPTH']}"
            
        self.ai_status_label = tk.Label(ai_info_frame, text=status_text,
                                       font=STYLE_CONFIG['FONTS']['SMALL'],
                                       fg='lightgray', bg=STYLE_CONFIG['COLORS']['DARK'])
        self.ai_status_label.pack()
        
    def create_combat_area(self):
        """Cria a área principal de combate"""
        combat_frame = tk.Frame(self.root, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        combat_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Arena de combate
        arena_frame = tk.LabelFrame(combat_frame, text="🏟️ Arena de Combate",
                                   font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                                   bg=STYLE_CONFIG['COLORS']['LIGHT'],
                                   fg=STYLE_CONFIG['COLORS']['DARK'])
        arena_frame.pack(fill="x", pady=(0, 20))
        
        # Personagens lado a lado
        chars_frame = tk.Frame(arena_frame, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        chars_frame.pack(pady=20)
        
        # Jogador
        self.create_character_display(chars_frame, "player", "left")
        
        # VS no meio
        vs_frame = tk.Frame(chars_frame, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        vs_frame.pack(side="left", padx=40)
        
        vs_label = tk.Label(vs_frame, text="⚔️\nVS", 
                           font=('Arial', 24, 'bold'),
                           fg=STYLE_CONFIG['COLORS']['WARNING'],
                           bg=STYLE_CONFIG['COLORS']['LIGHT'])
        vs_label.pack()
        
        self.turn_indicator = tk.Label(vs_frame, text="Turno 1",
                                      font=STYLE_CONFIG['FONTS']['NORMAL'],
                                      fg=STYLE_CONFIG['COLORS']['DARK'],
                                      bg=STYLE_CONFIG['COLORS']['LIGHT'])
        self.turn_indicator.pack(pady=10)
        
        # IA
        self.create_character_display(chars_frame, "enemy", "right")
        
        # Log de combate melhorado
        self.create_combat_log(combat_frame)
        
    def create_character_display(self, parent, char_type, side):
        """Cria display de personagem melhorado"""
        is_player = char_type == "player"
        character = self.player if is_player else self.enemy
        color = STYLE_CONFIG['COLORS']['PLAYER'] if is_player else STYLE_CONFIG['COLORS']['ENEMY']
        
        char_frame = tk.Frame(parent, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        char_frame.pack(side=side, padx=20)
        
        # Avatar
        avatar_frame = tk.Frame(char_frame, bg=color, width=100, height=100)
        avatar_frame.pack(pady=10)
        avatar_frame.pack_propagate(False)
        
        avatar_text = "🦸" if is_player else ("🎯" if self.ai_type == 'MINIMAX' else "🧠")
        avatar_label = tk.Label(avatar_frame, text=avatar_text,
                               font=('Arial', 48),
                               fg='white', bg=color)
        avatar_label.pack(expand=True)
        
        # Nome
        name = "JOGADOR" if is_player else f"IA {self.ai_type}"
        name_label = tk.Label(char_frame, text=name,
                             font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                             fg=color, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        name_label.pack()
        
        # HP
        hp_frame = tk.Frame(char_frame, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        hp_frame.pack(pady=10)
        
        hp_label_var = tk.StringVar(value=f"{character.hp}/{self.max_hp}")
        hp_label = tk.Label(hp_frame, textvariable=hp_label_var,
                           font=STYLE_CONFIG['FONTS']['NORMAL'],
                           fg=STYLE_CONFIG['COLORS']['DARK'],
                           bg=STYLE_CONFIG['COLORS']['LIGHT'])
        hp_label.pack()
        
        # Barra de HP moderna
        hp_bar_frame = tk.Frame(hp_frame, bg='white', relief='sunken', bd=2)
        hp_bar_frame.pack(pady=5)
        
        hp_bar = tk.Canvas(hp_bar_frame, width=200, height=20, bg='white', highlightthickness=0)
        hp_bar.pack(padx=2, pady=2)
        
        # Status indicators
        status_frame = tk.Frame(char_frame, bg=STYLE_CONFIG['COLORS']['LIGHT'])
        status_frame.pack(pady=5)
        
        status_label = tk.Label(status_frame, text="",
                               font=STYLE_CONFIG['FONTS']['SMALL'],
                               fg=STYLE_CONFIG['COLORS']['DARK'],
                               bg=STYLE_CONFIG['COLORS']['LIGHT'])
        status_label.pack()
        
        # Salva referências
        if is_player:
            self.player_hp_label = hp_label_var
            self.player_hp_bar = hp_bar
            self.player_status_label = status_label
        else:
            self.enemy_hp_label = hp_label_var
            self.enemy_hp_bar = hp_bar
            self.enemy_status_label = status_label
            
    def create_combat_log(self, parent):
        """Cria log de combate melhorado"""
        log_frame = tk.LabelFrame(parent, text="📜 Log de Combate",
                                 font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                                 bg=STYLE_CONFIG['COLORS']['LIGHT'],
                                 fg=STYLE_CONFIG['COLORS']['DARK'])
        log_frame.pack(fill="both", expand=True)
        
        # Frame para o texto e scrollbar
        text_frame = tk.Frame(log_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.combat_log = tk.Text(text_frame, height=12, wrap=tk.WORD,
                                 font=STYLE_CONFIG['FONTS']['MONO'],
                                 bg='#2C3E50', fg='#ECF0F1',
                                 insertbackground='white',
                                 selectbackground='#34495E')
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.combat_log.yview)
        self.combat_log.configure(yscrollcommand=scrollbar.set)
        
        self.combat_log.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar tags para cores
        self.combat_log.tag_configure("player", foreground=STYLE_CONFIG['COLORS']['PLAYER'])
        self.combat_log.tag_configure("enemy", foreground=STYLE_CONFIG['COLORS']['ENEMY'])
        self.combat_log.tag_configure("system", foreground=STYLE_CONFIG['COLORS']['INFO'])
        self.combat_log.tag_configure("damage", foreground=STYLE_CONFIG['COLORS']['DANGER'])
        self.combat_log.tag_configure("heal", foreground=STYLE_CONFIG['COLORS']['SUCCESS'])
        self.combat_log.tag_configure("thinking", foreground=STYLE_CONFIG['COLORS']['WARNING'])
        
    def create_side_panel(self):
        """Cria painel lateral com controles"""
        side_frame = tk.Frame(self.root, bg=STYLE_CONFIG['COLORS']['SECONDARY'], width=300)
        side_frame.pack(side="right", fill="y", padx=0, pady=0)
        side_frame.pack_propagate(False)
        
        # Título do painel
        panel_title = tk.Label(side_frame, text="🎮 CONTROLES",
                              font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                              fg='white', bg=STYLE_CONFIG['COLORS']['SECONDARY'])
        panel_title.pack(pady=20)
        
        # Botões de ação
        self.create_action_buttons(side_frame)
        
        # Estatísticas
        self.create_stats_panel(side_frame)
        
        # Controles do jogo
        self.create_game_controls(side_frame)
        
    def create_action_buttons(self, parent):
        """Cria botões de ação modernos"""
        actions_frame = tk.LabelFrame(parent, text="⚔️ Suas Ações",
                                     font=STYLE_CONFIG['FONTS']['NORMAL'],
                                     fg='white', bg=STYLE_CONFIG['COLORS']['SECONDARY'])
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão Atacar
        self.attack_btn = tk.Button(actions_frame, text="⚔️ ATACAR",
                                   command=self.player_attack,
                                   font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                                   bg=STYLE_CONFIG['COLORS']['DANGER'],
                                   fg='white', relief='flat',
                                   height=2, cursor='hand2')
        self.attack_btn.pack(fill="x", padx=10, pady=5)
        
        # Botão Defender
        self.defend_btn = tk.Button(actions_frame, text="🛡️ DEFENDER",
                                   command=self.player_defend,
                                   font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                                   bg=STYLE_CONFIG['COLORS']['INFO'],
                                   fg='white', relief='flat',
                                   height=2, cursor='hand2')
        self.defend_btn.pack(fill="x", padx=10, pady=5)
        
        # Botão Curar
        self.heal_btn = tk.Button(actions_frame, text="💚 CURAR",
                                 command=self.player_heal,
                                 font=STYLE_CONFIG['FONTS']['SUBTITLE'],
                                 bg=STYLE_CONFIG['COLORS']['SUCCESS'],
                                 fg='white', relief='flat',
                                 height=2, cursor='hand2')
        self.heal_btn.pack(fill="x", padx=10, pady=5)
        
    def create_stats_panel(self, parent):
        """Cria painel de estatísticas"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estatísticas",
                                   font=STYLE_CONFIG['FONTS']['NORMAL'],
                                   fg='white', bg=STYLE_CONFIG['COLORS']['SECONDARY'])
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Estatísticas da sessão
        self.stats_labels = {}
        stats_data = [
            ("Jogos:", "games_played"),
            ("Vitórias:", "games_won"),
            ("Dano Causado:", "total_damage_dealt"),
            ("Dano Recebido:", "total_damage_received")
        ]
        
        for label_text, key in stats_data:
            row_frame = tk.Frame(stats_frame, bg=STYLE_CONFIG['COLORS']['SECONDARY'])
            row_frame.pack(fill="x", padx=10, pady=2)
            
            tk.Label(row_frame, text=label_text,
                    font=STYLE_CONFIG['FONTS']['SMALL'],
                    fg='lightgray', bg=STYLE_CONFIG['COLORS']['SECONDARY'],
                    anchor='w').pack(side="left")
            
            value_label = tk.Label(row_frame, text="0",
                                  font=STYLE_CONFIG['FONTS']['SMALL'],
                                  fg='white', bg=STYLE_CONFIG['COLORS']['SECONDARY'],
                                  anchor='e')
            value_label.pack(side="right")
            self.stats_labels[key] = value_label
            
    def create_game_controls(self, parent):
        """Cria controles do jogo"""
        controls_frame = tk.LabelFrame(parent, text="🎛️ Controles",
                                      font=STYLE_CONFIG['FONTS']['NORMAL'],
                                      fg='white', bg=STYLE_CONFIG['COLORS']['SECONDARY'])
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão Novo Jogo
        new_game_btn = tk.Button(controls_frame, text="🔄 NOVO JOGO",
                                command=self.new_game,
                                font=STYLE_CONFIG['FONTS']['NORMAL'],
                                bg=STYLE_CONFIG['COLORS']['WARNING'],
                                fg='white', relief='flat',
                                cursor='hand2')
        new_game_btn.pack(fill="x", padx=10, pady=5)
        
        # Botão Trocar IA
        switch_ai_btn = tk.Button(controls_frame, text="🤖 TROCAR IA",
                                 command=self.switch_ai,
                                 font=STYLE_CONFIG['FONTS']['NORMAL'],
                                 bg=STYLE_CONFIG['COLORS']['INFO'],
                                 fg='white', relief='flat',
                                 cursor='hand2')
        switch_ai_btn.pack(fill="x", padx=10, pady=5)
        
    def create_footer(self):
        """Cria rodapé com informações do turno"""
        footer_frame = tk.Frame(self.root, bg=STYLE_CONFIG['COLORS']['DARK'], height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        self.footer_label = tk.Label(footer_frame, text="🎮 Seu turno! Escolha uma ação.",
                                    font=STYLE_CONFIG['FONTS']['NORMAL'],
                                    fg='white', bg=STYLE_CONFIG['COLORS']['DARK'])
        self.footer_label.pack(pady=10)
        
    def setup_styles(self):
        """Configura estilos adicionais"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilos para barras de progresso
        style.configure("Player.Horizontal.TProgressbar",
                       troughcolor='lightgray',
                       background=STYLE_CONFIG['COLORS']['PLAYER'])
        
        style.configure("Enemy.Horizontal.TProgressbar",
                       troughcolor='lightgray',
                       background=STYLE_CONFIG['COLORS']['ENEMY'])
                       
    def start_game(self):
        """Inicia um novo jogo"""
        self.log_message("🎮 Novo jogo iniciado!", "system")
        ai_name = "Minimax" if self.ai_type == 'MINIMAX' else "Neural"
        self.log_message(f"🤖 Enfrentando IA {ai_name}", "system")
        
        if self.ai_type == 'NEURAL' and self.neural_ai:
            stats = self.neural_ai.get_performance_stats()
            self.log_message(f"🧠 IA Neural com {stats['experience_count']} experiências", "system")
        
        self.update_display()
        
    def log_message(self, message, tag="system"):
        """Adiciona mensagem ao log com formatação"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.combat_log.insert(tk.END, formatted_message, tag)
        self.combat_log.see(tk.END)
        
    def update_display(self):
        """Atualiza todos os elementos visuais"""
        # Atualiza HP labels
        self.player_hp_label.set(f"{self.player.hp}/{self.max_hp}")
        self.enemy_hp_label.set(f"{self.enemy.hp}/{self.max_hp}")
        
        # Atualiza barras de HP
        self.update_hp_bar(self.player_hp_bar, self.player.hp, STYLE_CONFIG['COLORS']['PLAYER'])
        self.update_hp_bar(self.enemy_hp_bar, self.enemy.hp, STYLE_CONFIG['COLORS']['ENEMY'])
        
        # Atualiza status
        player_status = "🛡️ Defendendo" if self.player.is_defending else ""
        enemy_status = "🛡️ Defendendo" if self.enemy.is_defending else ""
        
        self.player_status_label.config(text=player_status)
        self.enemy_status_label.config(text=enemy_status)
        
        # Atualiza indicador de turno
        self.turn_indicator.config(text=f"Turno {self.turn_count}")
        
        # Atualiza estatísticas
        self.update_stats()
        
        # Atualiza status da IA
        if self.ai_type == 'NEURAL' and self.neural_ai:
            stats = self.neural_ai.get_performance_stats()
            self.ai_status_label.config(text=f"Experiências: {stats['experience_count']}")
            
    def update_hp_bar(self, canvas, hp, color):
        """Atualiza barra de HP com animação"""
        canvas.delete("all")
        
        # Calcula porcentagem
        percentage = hp / self.max_hp
        bar_width = 196  # 200 - 4 (padding)
        fill_width = int(bar_width * percentage)
        
        # Cor baseada na porcentagem de HP
        if percentage > 0.6:
            bar_color = color
        elif percentage > 0.3:
            bar_color = STYLE_CONFIG['COLORS']['WARNING']
        else:
            bar_color = STYLE_CONFIG['COLORS']['DANGER']
            
        # Desenha a barra
        if fill_width > 0:
            canvas.create_rectangle(2, 2, fill_width + 2, 18, fill=bar_color, outline="")
        
        # Texto do HP
        canvas.create_text(100, 10, text=f"{hp}/{self.max_hp}", 
                          font=STYLE_CONFIG['FONTS']['SMALL'], fill='black')
                          
    def update_stats(self):
        """Atualiza painel de estatísticas"""
        for key, label in self.stats_labels.items():
            value = self.session_stats[key]
            label.config(text=str(value))
            
    def player_attack(self):
        """Jogador ataca"""
        if not self.is_game_active:
            return
            
        self.disable_actions()
        self.session_stats['actions_taken']['attack'] += 1
        
        # Reset status
        self.player.reset_turn()
        self.enemy.reset_turn()
        
        damage = self.player.attack(self.enemy)
        self.session_stats['total_damage_dealt'] += damage
        
        self.log_message(f"⚔️ Você atacou causando {damage} de dano!", "player")
        self.animate_damage(self.enemy_hp_bar)
        
        self.update_display()
        
        if self.check_game_end():
            return
            
        # Turno da IA
        self.root.after(1000, self.ai_turn)
        
    def player_defend(self):
        """Jogador defende"""
        if not self.is_game_active:
            return
            
        self.disable_actions()
        self.session_stats['actions_taken']['defend'] += 1
        
        # Reset status
        self.player.reset_turn()
        self.enemy.reset_turn()
        
        self.player.defend()
        self.log_message("🛡️ Você se defendeu!", "player")
        
        self.update_display()
        
        # Turno da IA
        self.root.after(1000, self.ai_turn)
        
    def player_heal(self):
        """Jogador cura"""
        if not self.is_game_active:
            return
            
        self.disable_actions()
        self.session_stats['actions_taken']['heal'] += 1
        
        # Reset status
        self.player.reset_turn()
        self.enemy.reset_turn()
        
        healing = self.player.heal()
        self.log_message(f"💚 Você se curou em {healing} pontos!", "heal")
        self.animate_heal(self.player_hp_bar)
        
        self.update_display()
        
        if self.check_game_end():
            return
            
        # Turno da IA
        self.root.after(1000, self.ai_turn)
        
    def ai_turn(self):
        """Turno da IA com comportamento específico"""
        if not self.is_game_active:
            return
            
        self.footer_label.config(text="🤖 IA está pensando...")
        
        # Animação de pensamento
        self.start_thinking_animation()
        
        # Tempo de pensamento baseado no tipo de IA
        thinking_time = GAME_CONFIG[f'{self.ai_type}_CONFIG']['THINKING_TIME']
        
        # Executa ação da IA após o tempo de pensamento
        self.root.after(int(thinking_time * 1000), self.execute_ai_action)
        
    def start_thinking_animation(self):
        """Inicia animação de pensamento"""
        self.thinking_animation_active = True
        self.thinking_dots = 0
        self.animate_thinking()
        
    def animate_thinking(self):
        """Anima indicador de pensamento"""
        if not self.thinking_animation_active:
            return
            
        dots = "." * (self.thinking_dots % 4)
        ai_name = "Minimax" if self.ai_type == 'MINIMAX' else "Neural"
        self.footer_label.config(text=f"🤖 IA {ai_name} pensando{dots}")
        
        self.thinking_dots += 1
        self.root.after(300, self.animate_thinking)
        
    def execute_ai_action(self):
        """Executa ação da IA"""
        self.thinking_animation_active = False
        
        # Salva estado para aprendizado
        pre_state = {
            'player_hp': self.player.hp,
            'enemy_hp': self.enemy.hp,
            'player_defending': self.player.is_defending,
            'enemy_defending': self.enemy.is_defending,
            'turn': self.turn_count
        }
        
        # Escolhe ação baseada no tipo de IA
        if self.ai_type == 'NEURAL' and self.neural_ai:
            action = self.neural_ai.decide_action(
                self.player.hp, self.enemy.hp,
                self.player.is_defending, self.enemy.is_defending,
                self.turn_count
            )
            
            # Mostra processo de aprendizado
            if GAME_CONFIG['NEURAL_CONFIG']['SHOW_LEARNING']:
                self.log_message("🧠 Analisando padrões de jogo...", "thinking")
                
        else:
            # Minimax com análise detalhada
            if GAME_CONFIG['MINIMAX_CONFIG']['SHOW_ANALYSIS']:
                self.log_message("🎯 Calculando melhor jogada...", "thinking")
                
            state = BattleState(
                self.player.hp, self.enemy.hp, player_turn=False,
                player_defending=self.player.is_defending,
                enemy_defending=self.enemy.is_defending
            )
            
            score, action = minimax(state, depth=GAME_CONFIG['MINIMAX_DEPTH'], maximizing_player=True)
            
            if GAME_CONFIG['MINIMAX_CONFIG']['SHOW_ANALYSIS']:
                self.log_message(f"🎯 Avaliação: {score:.2f}", "thinking")
        
        # Executa ação
        self.session_stats['ai_actions'][action] += 1
        damage_dealt = 0
        healing_done = 0
        
        ai_name = "Minimax" if self.ai_type == 'MINIMAX' else "Neural"
        
        if action == "attack":
            damage_dealt = self.enemy.attack(self.player)
            self.session_stats['total_damage_received'] += damage_dealt
            self.log_message(f"⚔️ IA {ai_name} atacou causando {damage_dealt} de dano!", "enemy")
            self.animate_damage(self.player_hp_bar)
            
        elif action == "heal":
            healing_done = self.enemy.heal()
            self.log_message(f"💚 IA {ai_name} se curou em {healing_done} pontos!", "heal")
            self.animate_heal(self.enemy_hp_bar)
            
        elif action == "defend":
            self.enemy.defend()
            self.log_message(f"🛡️ IA {ai_name} se defendeu!", "enemy")
        
        # Aprendizado da IA Neural
        if self.ai_type == 'NEURAL' and self.neural_ai and GAME_CONFIG['NEURAL_LEARNING']:
            result_score = self.calculate_action_score(pre_state, action, damage_dealt, healing_done)
            
            self.neural_ai.learn_from_experience(
                pre_state['player_hp'], pre_state['enemy_hp'],
                action, result_score,
                pre_state['player_defending'], pre_state['enemy_defending'],
                self.turn_count
            )
            
            if GAME_CONFIG['NEURAL_CONFIG']['SHOW_LEARNING'] and abs(result_score) > 0.5:
                learning_msg = "📈 Ação bem-sucedida!" if result_score > 0 else "📉 Ajustando estratégia..."
                self.log_message(learning_msg, "thinking")
        
        self.turn_count += 1
        self.update_display()
        
        if self.check_game_end():
            return
            
        # Próximo turno do jogador
        self.enable_actions()
        self.footer_label.config(text="🎮 Seu turno! Escolha uma ação.")
        
    def calculate_action_score(self, pre_state, action, damage_dealt, healing_done):
        """Calcula score para aprendizado da IA Neural"""
        score = 0.0
        
        if action == "attack" and damage_dealt > 0:
            score += damage_dealt / 30.0
            if self.player.hp <= 0:
                score += 2.0
                
        elif action == "heal" and healing_done > 0:
            if pre_state['enemy_hp'] < GAME_CONFIG['MAX_HP'] * 0.5:
                score += healing_done / 20.0
            else:
                score -= 0.5
                
        elif action == "defend":
            if pre_state['enemy_hp'] < GAME_CONFIG['MAX_HP'] * 0.3:
                score += 0.5
            else:
                score += 0.1
        
        if self.enemy.hp <= 0:
            score -= 2.0
            
        hp_diff = self.enemy.hp - self.player.hp
        score += hp_diff / GAME_CONFIG['MAX_HP']
        
        return np.clip(score, -2.0, 2.0)
        
    def animate_damage(self, hp_bar):
        """Anima efeito de dano"""
        # Pisca vermelho
        original_bg = hp_bar.cget('bg')
        hp_bar.config(bg=STYLE_CONFIG['COLORS']['DANGER'])
        self.root.after(200, lambda: hp_bar.config(bg=original_bg))
        
    def animate_heal(self, hp_bar):
        """Anima efeito de cura"""
        # Pisca verde
        original_bg = hp_bar.cget('bg')
        hp_bar.config(bg=STYLE_CONFIG['COLORS']['SUCCESS'])
        self.root.after(200, lambda: hp_bar.config(bg=original_bg))
        
    def check_game_end(self):
        """Verifica se o jogo terminou"""
        if not self.player.is_alive():
            self.game_over(False)
            return True
        elif not self.enemy.is_alive():
            self.game_over(True)
            return True
        return False
        
    def game_over(self, player_won):
        """Finaliza o jogo"""
        self.is_game_active = False
        self.disable_actions()
        
        self.session_stats['games_played'] += 1
        if player_won:
            self.session_stats['games_won'] += 1
            
        if player_won:
            self.log_message("🎉 VITÓRIA! Você venceu!", "player")
            self.footer_label.config(text="🎉 Parabéns! Você venceu!")
        else:
            self.log_message("💀 DERROTA! A IA venceu!", "enemy")
            self.footer_label.config(text="💀 Que pena! A IA venceu!")
            
        # Aprendizado final da IA Neural
        if self.ai_type == 'NEURAL' and self.neural_ai and GAME_CONFIG['NEURAL_LEARNING']:
            final_score = -1.0 if player_won else 1.0
            
            # Aprende com o resultado final
            for i in range(min(5, len(self.game_history))):
                weight = (i + 1) / 5
                # Implementar aprendizado final se necessário
                
            self.log_message("🧠 IA Neural aprendeu com este jogo!", "thinking")
            
        self.update_display()
        
    def disable_actions(self):
        """Desabilita botões de ação"""
        self.attack_btn.config(state="disabled")
        self.defend_btn.config(state="disabled")
        self.heal_btn.config(state="disabled")
        
    def enable_actions(self):
        """Habilita botões de ação"""
        self.attack_btn.config(state="normal")
        self.defend_btn.config(state="normal")
        self.heal_btn.config(state="normal")
        
    def new_game(self):
        """Inicia novo jogo"""
        self.is_game_active = True
        self.turn_count = 1
        self.game_history = []
        
        # Recria personagens
        self.player = Character("Jogador", self.max_hp, GAME_CONFIG['PLAYER_ATTACK'], GAME_CONFIG['PLAYER_DEFENSE'])
        self.enemy = Character("IA", self.max_hp, GAME_CONFIG['AI_ATTACK'], GAME_CONFIG['AI_DEFENSE'])
        
        # Limpa log
        self.combat_log.delete(1.0, tk.END)
        
        self.start_game()
        self.enable_actions()
        
    def switch_ai(self):
        """Troca tipo de IA"""
        new_ai_type = 'NEURAL' if self.ai_type == 'MINIMAX' else 'MINIMAX'
        
        # Cria nova janela com IA diferente
        new_window = tk.Toplevel(self.root)
        ModernGameGUI(new_window, new_ai_type)


def run_modern_gui(ai_type='MINIMAX'):
    """Executa a GUI moderna"""
    root = tk.Tk()
    app = ModernGameGUI(root, ai_type)
    root.mainloop()


if __name__ == "__main__":
    run_modern_gui()