import tkinter as tk
from tkinter import ttk, messagebox
from .game_gui import GameGUI
from .config import GAME_CONFIG, GUI_CONFIG, STYLE_CONFIG

class WindowManager:
    """Gerenciador de janelas do jogo"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Combate por Turnos - Menu")
        self.root.geometry(f"{GUI_CONFIG['MENU_WIDTH']}x{GUI_CONFIG['MENU_HEIGHT']}")
        self.root.resizable(False, False)
        self.center_window()
        self.setup_styles()
        self.create_menu()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (GUI_CONFIG['MENU_WIDTH'] // 2)
        y = (self.root.winfo_screenheight() // 2) - (GUI_CONFIG['MENU_HEIGHT'] // 2)
        self.root.geometry(f"{GUI_CONFIG['MENU_WIDTH']}x{GUI_CONFIG['MENU_HEIGHT']}+{x}+{y}")
        
    def setup_styles(self):
        """Configura estilos das barras de progresso"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Green.Horizontal.TProgressbar", 
                       troughcolor='lightgray', background='green')
        style.configure("Red.Horizontal.TProgressbar", 
                       troughcolor='lightgray', background='red')
        
    def create_menu(self):
        """Cria o menu principal"""
        # Título
        title_label = tk.Label(self.root, text="⚔️ COMBATE POR TURNOS ⚔️", 
                              font=STYLE_CONFIG['FONTS']['TITLE'], 
                              fg=STYLE_CONFIG['COLORS']['PRIMARY'])
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(self.root, text="Sistema de IA com Minimax", 
                                 font=STYLE_CONFIG['FONTS']['SMALL'], 
                                 fg="gray")
        subtitle_label.pack()
        
        # Botões
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        # Botão Jogo Simples
        simple_btn = tk.Button(btn_frame, text="🎮 Jogo Simples", 
                              command=self.open_simple_game,
                              font=STYLE_CONFIG['FONTS']['SUBTITLE'], 
                              width=20, height=2,
                              bg="lightgreen", relief="raised")
        simple_btn.pack(pady=5)
        
        # Botão Jogo Avançado
        advanced_btn = tk.Button(btn_frame, text="🎯 Jogo Avançado", 
                                command=self.open_advanced_game,
                                font=STYLE_CONFIG['FONTS']['SUBTITLE'], 
                                width=20, height=2,
                                bg="lightblue", relief="raised")
        advanced_btn.pack(pady=5)
        
        # Botão Configurações
        config_btn = tk.Button(btn_frame, text="⚙️ Configurações", 
                              command=self.show_config,
                              font=STYLE_CONFIG['FONTS']['SUBTITLE'], 
                              width=20, height=2,
                              bg="lightyellow", relief="raised")
        config_btn.pack(pady=5)
        
        # Botão Sair
        exit_btn = tk.Button(btn_frame, text="❌ Sair", 
                            command=self.confirm_exit,
                            font=STYLE_CONFIG['FONTS']['SUBTITLE'], 
                            width=20, height=2,
                            bg="lightcoral", relief="raised")
        exit_btn.pack(pady=5)
        
        # Rodapé
        footer_label = tk.Label(self.root, text="Desenvolvido com Python & Tkinter", 
                               font=STYLE_CONFIG['FONTS']['SMALL'], 
                               fg="gray")
        footer_label.pack(side="bottom", pady=10)
        
    def confirm_exit(self):
        """Confirma saída da aplicação"""
        if messagebox.askquestion("Sair", "Deseja realmente sair do jogo?") == "yes":
            self.root.quit()
        
    def open_simple_game(self):
        """Abre jogo em janela simples"""
        self.show_ai_selection_dialog(simple=True)
        
    def open_advanced_game(self):
        """Abre jogo em janela avançada"""
        self.show_ai_selection_dialog(simple=False)
        
    def create_advanced_game_window(self):
        """Cria janela de jogo avançada com abas"""
        game_window = tk.Toplevel(self.root)
        game_window.title("Combate Avançado")
        game_window.geometry("900x700")
        game_window.resizable(True, True)
        
        # Notebook para abas
        notebook = ttk.Notebook(game_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba do Jogo - cria uma janela separada
        game_frame = ttk.Frame(notebook)
        notebook.add(game_frame, text="🎮 Arena de Combate")
        
        # Botão para abrir jogo em janela separada
        open_game_btn = tk.Button(game_frame, 
                                 text="🚀 Abrir Arena de Combate", 
                                 command=lambda: GameGUI(tk.Toplevel(game_window)),
                                 font=("Arial", 14), 
                                 bg="lightgreen", 
                                 height=3)
        open_game_btn.pack(expand=True)
        
        info_label = tk.Label(game_frame, 
                             text="Clique no botão acima para abrir o jogo\nem uma janela separada",
                             font=("Arial", 12), 
                             fg="gray")
        info_label.pack(pady=20)
        
        # Aba de Estatísticas
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="📊 Estatísticas")
        self.create_stats_tab(stats_frame)
        
        # Aba de Configurações
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="⚙️ Config")
        self.create_config_tab(config_frame)
        
    def create_stats_tab(self, parent):
        """Cria aba de estatísticas"""
        title = tk.Label(parent, text="📊 Estatísticas do Jogo", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        stats_text = f"""
Configurações Atuais:
• HP Máximo: {GAME_CONFIG['MAX_HP']}
• Ataque Jogador: {GAME_CONFIG['PLAYER_ATTACK']}
• Ataque IA: {GAME_CONFIG['AI_ATTACK']}
• Profundidade Minimax: {GAME_CONFIG['MINIMAX_DEPTH']}
• Cura: {GAME_CONFIG['HEAL_MIN']}-{GAME_CONFIG['HEAL_MAX']}

Sistema de IA:
• Algoritmo: Minimax
• Avaliação: Baseada em HP e vantagem tática
• Dificuldade: Adaptativa
        """
        
        stats_label = tk.Label(parent, text=stats_text, 
                              font=("Arial", 11), justify="left")
        stats_label.pack(pady=20)
        
    def create_config_tab(self, parent):
        """Cria aba de configurações"""
        title = tk.Label(parent, text="⚙️ Configurações", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # Frame para configurações
        config_frame = tk.Frame(parent)
        config_frame.pack(pady=20)
        
        # HP Máximo
        hp_frame = tk.Frame(config_frame)
        hp_frame.pack(fill="x", pady=5)
        
        tk.Label(hp_frame, text="HP Máximo:", width=15, anchor="w").pack(side="left")
        hp_var = tk.IntVar(value=GAME_CONFIG['MAX_HP'])
        hp_scale = tk.Scale(hp_frame, from_=100, to=500, orient="horizontal", 
                           variable=hp_var, length=200)
        hp_scale.pack(side="left")
        
        # Botão para aplicar mudanças
        apply_btn = tk.Button(config_frame, text="💾 Aplicar Mudanças",
                             command=lambda: self.apply_config(hp_var.get()),
                             bg="lightgreen", font=("Arial", 10))
        apply_btn.pack(pady=20)
        
    def apply_config(self, new_hp):
        """Aplica novas configurações"""
        GAME_CONFIG['MAX_HP'] = new_hp
        messagebox.showinfo("Configurações", 
                           f"HP máximo alterado para {new_hp}!")
        
    def show_config(self):
        """Mostra janela de configurações"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configurações")
        config_window.geometry("400x300")
        
        title = tk.Label(config_window, text="⚙️ Configurações do Jogo", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=20)
        
        info_text = f"""
Configurações Atuais:

HP Máximo: {GAME_CONFIG['MAX_HP']}
Ataque do Jogador: {GAME_CONFIG['PLAYER_ATTACK']}
Ataque da IA: {GAME_CONFIG['AI_ATTACK']}
Defesa do Jogador: {GAME_CONFIG['PLAYER_DEFENSE']}
Defesa da IA: {GAME_CONFIG['AI_DEFENSE']}
Profundidade Minimax: {GAME_CONFIG['MINIMAX_DEPTH']}
Cura Mínima: {GAME_CONFIG['HEAL_MIN']}
Cura Máxima: {GAME_CONFIG['HEAL_MAX']}
        """
        
        info_label = tk.Label(config_window, text=info_text, 
                             font=("Arial", 10), justify="left")
        info_label.pack(pady=10)
        
        close_btn = tk.Button(config_window, text="Fechar", 
                             command=config_window.destroy,
                             bg="lightcoral")
        close_btn.pack(pady=10)
    
    def show_ai_selection_dialog(self, simple=True):
        """Mostra diálogo para seleção do tipo de IA"""
        ai_window = tk.Toplevel(self.root)
        ai_window.title("Escolha o Tipo de IA")
        ai_window.geometry("500x450")  # Aumentei o tamanho
        ai_window.resizable(False, False)
        
        # Centraliza a janela
        ai_window.update_idletasks()
        x = (ai_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (ai_window.winfo_screenheight() // 2) - (450 // 2)
        ai_window.geometry(f"500x450+{x}+{y}")
        
        # Título
        title = tk.Label(ai_window, text="🤖 Escolha o Tipo de IA", 
                        font=STYLE_CONFIG['FONTS']['TITLE'], 
                        fg=STYLE_CONFIG['COLORS']['PRIMARY'])
        title.pack(pady=15)
        
        # Descrições das IAs
        desc_frame = tk.Frame(ai_window)
        desc_frame.pack(pady=10, padx=20, fill="x")  # Removido expand=True
        
        # Minimax
        minimax_frame = tk.LabelFrame(desc_frame, text="🎯 Minimax (Clássica)", 
                                     font=STYLE_CONFIG['FONTS']['SUBTITLE'])
        minimax_frame.pack(fill="x", pady=5)
        
        minimax_desc = tk.Label(minimax_frame, 
                               text="• Algoritmo determinístico\n• Estratégia sempre consistente\n• Boa para aprender padrões\n• Performance previsível",
                               font=STYLE_CONFIG['FONTS']['NORMAL'], 
                               justify="left", anchor="w")
        minimax_desc.pack(padx=10, pady=8)
        
        # Neural
        neural_frame = tk.LabelFrame(desc_frame, text="🧠 Rede Neural (Adaptativa)", 
                                    font=STYLE_CONFIG['FONTS']['SUBTITLE'])
        neural_frame.pack(fill="x", pady=5)
        
        neural_desc = tk.Label(neural_frame, 
                              text="• Aprende com cada partida\n• Estratégia evolui com o tempo\n• Pode surpreender o jogador\n• Melhora continuamente",
                              font=STYLE_CONFIG['FONTS']['NORMAL'], 
                              justify="left", anchor="w")
        neural_desc.pack(padx=10, pady=8)
        
        # Espaçador
        spacer = tk.Frame(ai_window, height=20)
        spacer.pack()
        
        # Botões de seleção
        button_frame = tk.Frame(ai_window)
        button_frame.pack(pady=15)
        
        minimax_btn = tk.Button(button_frame, text="🎯 Jogar vs Minimax", 
                               command=lambda: self.start_game_with_ai('MINIMAX', ai_window, simple),
                               font=STYLE_CONFIG['FONTS']['SUBTITLE'], 
                               width=18, height=2,
                               bg="lightblue", relief="raised")
        minimax_btn.pack(side="left", padx=10)
        
        neural_btn = tk.Button(button_frame, text="🧠 Jogar vs Neural", 
                              command=lambda: self.start_game_with_ai('NEURAL', ai_window, simple),
                              font=STYLE_CONFIG['FONTS']['SUBTITLE'], 
                              width=18, height=2,
                              bg="lightgreen", relief="raised")
        neural_btn.pack(side="left", padx=10)
        
        # Botão cancelar
        cancel_frame = tk.Frame(ai_window)
        cancel_frame.pack(pady=15)
        
        cancel_btn = tk.Button(cancel_frame, text="❌ Cancelar", 
                              command=ai_window.destroy,
                              font=STYLE_CONFIG['FONTS']['NORMAL'], 
                              width=12,
                              bg="lightcoral")
        cancel_btn.pack()
    
    def start_game_with_ai(self, ai_type, dialog_window, simple=True):
        """Inicia o jogo com o tipo de IA selecionado"""
        dialog_window.destroy()
        
        if simple:
            # Usa a GUI moderna
            from .enhanced_gui import ModernGameGUI
            game_window = tk.Toplevel(self.root)
            game = ModernGameGUI(game_window, ai_type=ai_type)
        else:
            # Para jogo avançado, usa a GUI moderna também
            self.create_advanced_game_with_ai(ai_type)
    
    def create_advanced_game_with_ai(self, ai_type):
        """Cria jogo avançado com IA específica"""
        # Usa a GUI moderna diretamente
        from .enhanced_gui import ModernGameGUI
        game_window = tk.Toplevel(self.root)
        game = ModernGameGUI(game_window, ai_type=ai_type)
    
    def create_ai_stats_tab(self, parent, ai_type, game_instance):
        """Cria aba de estatísticas específicas da IA"""
        title = tk.Label(parent, text=f"📊 Estatísticas da IA {ai_type}", 
                        font=STYLE_CONFIG['FONTS']['TITLE'])
        title.pack(pady=20)
        
        if ai_type == 'NEURAL' and hasattr(game_instance, 'neural_ai') and game_instance.neural_ai:
            # Estatísticas da IA Neural
            stats = game_instance.neural_ai.get_performance_stats()
            
            stats_text = f"""
Estatísticas da Rede Neural:

• Experiências Acumuladas: {stats['experience_count']}
• Épocas de Treinamento: {stats['training_epochs']}
• Último Erro: {stats['last_error']:.4f}
• Modelo Salvo: {'Sim' if stats['model_exists'] else 'Não'}

Configurações da Rede:
• Neurônios de Entrada: 6
• Neurônios Ocultos: 10  
• Neurônios de Saída: 3
• Taxa de Aprendizado: 0.1

A IA Neural aprende continuamente durante o jogo,
ajustando sua estratégia baseada nos resultados.
            """
            
            # Botão para retreinar
            retrain_btn = tk.Button(parent, text="🔄 Retreinar IA", 
                                   command=lambda: self.retrain_neural_ai(game_instance),
                                   bg="lightyellow", font=STYLE_CONFIG['FONTS']['NORMAL'])
            retrain_btn.pack(pady=10)
            
        else:
            # Estatísticas do Minimax
            stats_text = f"""
Estatísticas do Minimax:

• Profundidade de Busca: {GAME_CONFIG['MINIMAX_DEPTH']}
• Algoritmo: Minimax com Poda Alpha-Beta
• Função de Avaliação: Baseada em HP e vantagem
• Estratégia: Determinística

O Minimax analisa {GAME_CONFIG['MINIMAX_DEPTH']} jogadas à frente
para escolher a melhor ação possível.

Vantagens:
• Estratégia consistente
• Performance previsível
• Boa para iniciantes

Desvantagens:
• Não aprende com erros
• Pode ser previsível
            """
        
        stats_label = tk.Label(parent, text=stats_text, 
                              font=STYLE_CONFIG['FONTS']['NORMAL'], 
                              justify="left")
        stats_label.pack(pady=20, padx=20)
    
    def retrain_neural_ai(self, game_instance):
        """Retreina a IA neural"""
        if hasattr(game_instance, 'neural_ai') and game_instance.neural_ai:
            game_instance.neural_ai.retrain_network()
            messagebox.showinfo("Retreinamento", "IA Neural retreinada com sucesso!")
        else:
            messagebox.showerror("Erro", "IA Neural não encontrada!")
        
    def run(self):
        """Executa o gerenciador de janelas"""
        self.root.mainloop()


def run_window_manager():
    """Função para executar o gerenciador de janelas"""
    manager = WindowManager()
    manager.run()


if __name__ == "__main__":
    run_window_manager()