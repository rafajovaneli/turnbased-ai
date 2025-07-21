# Configurações do jogo
GAME_CONFIG = {
    # Configurações de combate
    'MAX_HP': 300,
    'PLAYER_ATTACK': 20,
    'PLAYER_DEFENSE': 5,
    'AI_ATTACK': 25,
    'AI_DEFENSE': 4,
    
    # Configurações de cura
    'HEAL_MIN': 5,
    'HEAL_MAX': 20,
    
    # Configurações de IA
    'MINIMAX_DEPTH': 6,
    'AI_TYPE': 'MINIMAX',  # 'MINIMAX' ou 'NEURAL'
    'NEURAL_LEARNING': True,  # Se a IA neural deve aprender durante o jogo
    
    # Configurações específicas por tipo de IA
    'MINIMAX_CONFIG': {
        'THINKING_TIME': 1.0,  # Tempo de "pensamento" em segundos
        'SHOW_ANALYSIS': True,  # Mostra análise das jogadas
        'CONSISTENCY': 1.0,  # 100% consistente
        'AGGRESSION': 0.7  # Nível de agressividade
    },
    
    'NEURAL_CONFIG': {
        'THINKING_TIME': 1.5,  # Tempo de "pensamento" em segundos
        'SHOW_LEARNING': True,  # Mostra processo de aprendizado
        'EXPLORATION_RATE': 0.15,  # Taxa de exploração (ações aleatórias)
        'ADAPTATION_SPEED': 0.1,  # Velocidade de adaptação
        'PERSONALITY_SHIFT': True  # Muda personalidade com o tempo
    },
    
    # Configurações visuais do console
    'HP_BAR_LENGTH': 20,
    
    # Configurações de dificuldade
    'DIFFICULTY_LEVELS': {
        'FACIL': {'AI_ATTACK': 20, 'MINIMAX_DEPTH': 3},
        'NORMAL': {'AI_ATTACK': 25, 'MINIMAX_DEPTH': 6},
        'DIFICIL': {'AI_ATTACK': 30, 'MINIMAX_DEPTH': 8}
    }
}

# Configurações da GUI
GUI_CONFIG = {
    'WINDOW_TITLE': 'Combate por Turnos',
    'IMAGE_SIZE': (64, 64),
    'HP_BAR_LENGTH': 200,
    'WINDOW_WIDTH': 600,
    'WINDOW_HEIGHT': 400,
    'MENU_WIDTH': 400,
    'MENU_HEIGHT': 300,
    'ADVANCED_WIDTH': 900,
    'ADVANCED_HEIGHT': 700
}

# Configurações de estilo
STYLE_CONFIG = {
    'COLORS': {
        'PRIMARY': '#2C3E50',
        'SECONDARY': '#34495E', 
        'SUCCESS': '#27AE60',
        'DANGER': '#E74C3C',
        'WARNING': '#F39C12',
        'INFO': '#3498DB',
        'LIGHT': '#ECF0F1',
        'DARK': '#2C3E50',
        'MINIMAX': '#3498DB',  # Azul para Minimax
        'NEURAL': '#9B59B6',   # Roxo para Neural
        'PLAYER': '#27AE60',   # Verde para jogador
        'ENEMY': '#E74C3C'     # Vermelho para inimigo
    },
    'FONTS': {
        'TITLE': ('Segoe UI', 18, 'bold'),
        'SUBTITLE': ('Segoe UI', 14, 'bold'),
        'NORMAL': ('Segoe UI', 11),
        'SMALL': ('Segoe UI', 9),
        'MONO': ('Consolas', 10)
    },
    'GRADIENTS': {
        'MINIMAX': ['#3498DB', '#2980B9'],
        'NEURAL': ['#9B59B6', '#8E44AD'],
        'PLAYER': ['#27AE60', '#229954'],
        'ENEMY': ['#E74C3C', '#C0392B']
    }
}