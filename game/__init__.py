"""
Jogo de Combate por Turnos

Um jogo estratégico com IA inteligente usando algoritmo Minimax.

Modos de Jogo:
- Console: run_game()
- GUI Simples: run_gui()  
- GUI com Janelas Múltiplas: run_window_manager()
"""

from .engine import run_game, run_game_with_neural_ai, run_game_with_minimax
from .game_gui import run_gui, GameGUI
from .enhanced_gui import ModernGameGUI, run_modern_gui
from .window_manager import run_window_manager, WindowManager
from .entities import Character
from .minimax import BattleState, minimax
from .neural_ai import NeuralAI, create_neural_ai
from .config import GAME_CONFIG, GUI_CONFIG, STYLE_CONFIG

__version__ = "2.0.0"
__author__ = "Desenvolvedor"

__all__ = [
    'run_game',
    'run_game_with_neural_ai',
    'run_game_with_minimax',
    'run_gui', 
    'run_modern_gui',
    'run_window_manager',
    'GameGUI',
    'ModernGameGUI',
    'WindowManager',
    'Character',
    'BattleState',
    'minimax',
    'NeuralAI',
    'create_neural_ai',
    'GAME_CONFIG',
    'GUI_CONFIG',
    'STYLE_CONFIG'
]