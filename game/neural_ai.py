import numpy as np
import random
import json
import os
from typing import List, Tuple
from .config import GAME_CONFIG

class SimpleNeuralNetwork:
    """Rede neural simples para IA do jogo"""
    
    def __init__(self, input_size: int = 6, hidden_size: int = 10, output_size: int = 3):
        """
        Inicializa a rede neural
        
        Args:
            input_size: Tamanho da entrada (estado do jogo)
            hidden_size: Neurônios na camada oculta
            output_size: Tamanho da saída (3 ações: attack, defend, heal)
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Inicializa pesos aleatoriamente
        self.weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))
        
        # Bias
        self.bias_hidden = np.random.uniform(-1, 1, hidden_size)
        self.bias_output = np.random.uniform(-1, 1, output_size)
        
        # Taxa de aprendizado
        self.learning_rate = 0.1
        
        # Histórico de treinamento
        self.training_data = []
        self.performance_history = []
        
    def sigmoid(self, x):
        """Função de ativação sigmoid"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip para evitar overflow
    
    def sigmoid_derivative(self, x):
        """Derivada da função sigmoid"""
        return x * (1 - x)
    
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """Propagação para frente"""
        # Camada oculta
        self.hidden_input = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        self.hidden_output = self.sigmoid(self.hidden_input)
        
        # Camada de saída
        self.output_input = np.dot(self.hidden_output, self.weights_hidden_output) + self.bias_output
        self.output = self.sigmoid(self.output_input)
        
        return self.output
    
    def backward(self, inputs: np.ndarray, expected_output: np.ndarray):
        """Propagação para trás (backpropagation)"""
        # Erro na saída
        output_error = expected_output - self.output
        output_delta = output_error * self.sigmoid_derivative(self.output)
        
        # Erro na camada oculta
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden_output)
        
        # Atualiza pesos e bias
        self.weights_hidden_output += self.hidden_output.reshape(-1, 1).dot(output_delta.reshape(1, -1)) * self.learning_rate
        self.bias_output += output_delta * self.learning_rate
        
        self.weights_input_hidden += inputs.reshape(-1, 1).dot(hidden_delta.reshape(1, -1)) * self.learning_rate
        self.bias_hidden += hidden_delta * self.learning_rate
    
    def train(self, training_data: List[Tuple[np.ndarray, np.ndarray]], epochs: int = 1000):
        """Treina a rede neural"""
        for epoch in range(epochs):
            total_error = 0
            for inputs, expected_output in training_data:
                # Forward pass
                predicted = self.forward(inputs)
                
                # Calcula erro
                error = np.mean((expected_output - predicted) ** 2)
                total_error += error
                
                # Backward pass
                self.backward(inputs, expected_output)
            
            # Registra performance a cada 100 épocas
            if epoch % 100 == 0:
                avg_error = total_error / len(training_data)
                self.performance_history.append(avg_error)
                print(f"Época {epoch}: Erro médio = {avg_error:.4f}")
    
    def predict(self, inputs: np.ndarray) -> str:
        """Faz predição e retorna ação"""
        output = self.forward(inputs)
        action_index = np.argmax(output)
        
        actions = ['attack', 'defend', 'heal']
        return actions[action_index]
    
    def save_model(self, filepath: str):
        """Salva o modelo treinado"""
        model_data = {
            'weights_input_hidden': self.weights_input_hidden.tolist(),
            'weights_hidden_output': self.weights_hidden_output.tolist(),
            'bias_hidden': self.bias_hidden.tolist(),
            'bias_output': self.bias_output.tolist(),
            'performance_history': self.performance_history,
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'output_size': self.output_size
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f)
    
    def load_model(self, filepath: str):
        """Carrega modelo salvo"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                model_data = json.load(f)
            
            self.weights_input_hidden = np.array(model_data['weights_input_hidden'])
            self.weights_hidden_output = np.array(model_data['weights_hidden_output'])
            self.bias_hidden = np.array(model_data['bias_hidden'])
            self.bias_output = np.array(model_data['bias_output'])
            self.performance_history = model_data.get('performance_history', [])
            
            return True
        return False


class NeuralAI:
    """IA baseada em rede neural para o jogo"""
    
    def __init__(self):
        self.network = SimpleNeuralNetwork()
        self.model_path = "neural_ai_model.json"
        self.experience_buffer = []
        self.max_buffer_size = 1000
        
        # Tenta carregar modelo existente
        if self.network.load_model(self.model_path):
            print("Modelo neural carregado com sucesso!")
        else:
            print("Novo modelo neural criado.")
            self.train_initial_model()
    
    def game_state_to_input(self, player_hp: int, enemy_hp: int, 
                           player_defending: bool = False, 
                           enemy_defending: bool = False,
                           turn_count: int = 1) -> np.ndarray:
        """Converte estado do jogo para entrada da rede neural"""
        max_hp = GAME_CONFIG['MAX_HP']
        
        # Normaliza valores para [0, 1]
        inputs = np.array([
            player_hp / max_hp,           # HP do jogador normalizado
            enemy_hp / max_hp,            # HP do inimigo normalizado
            1.0 if player_defending else 0.0,  # Status de defesa do jogador
            1.0 if enemy_defending else 0.0,   # Status de defesa do inimigo
            min(turn_count / 20.0, 1.0),       # Turno normalizado (máx 20)
            (enemy_hp - player_hp) / max_hp     # Diferença de HP normalizada
        ])
        
        return inputs
    
    def action_to_output(self, action: str) -> np.ndarray:
        """Converte ação para saída esperada da rede"""
        action_map = {'attack': 0, 'defend': 1, 'heal': 2}
        output = np.zeros(3)
        if action in action_map:
            output[action_map[action]] = 1.0
        return output
    
    def decide_action(self, player_hp: int, enemy_hp: int, 
                     player_defending: bool = False, 
                     enemy_defending: bool = False,
                     turn_count: int = 1) -> str:
        """Decide ação baseada no estado atual"""
        inputs = self.game_state_to_input(player_hp, enemy_hp, 
                                        player_defending, enemy_defending, 
                                        turn_count)
        
        # Adiciona um pouco de aleatoriedade para exploração
        if random.random() < 0.1:  # 10% de chance de ação aleatória
            return random.choice(['attack', 'defend', 'heal'])
        
        return self.network.predict(inputs)
    
    def learn_from_experience(self, player_hp: int, enemy_hp: int,
                            action_taken: str, result_score: float,
                            player_defending: bool = False,
                            enemy_defending: bool = False,
                            turn_count: int = 1):
        """Aprende com a experiência do jogo"""
        inputs = self.game_state_to_input(player_hp, enemy_hp, 
                                        player_defending, enemy_defending, 
                                        turn_count)
        
        # Cria saída baseada no resultado
        expected_output = self.action_to_output(action_taken)
        
        # Ajusta baseado no resultado (recompensa/punição)
        if result_score > 0:  # Boa ação
            expected_output *= 1.2  # Reforça a ação
        elif result_score < 0:  # Má ação
            expected_output *= 0.8  # Diminui a probabilidade
        
        # Normaliza para manter entre 0 e 1
        expected_output = np.clip(expected_output, 0, 1)
        
        # Adiciona ao buffer de experiência
        self.experience_buffer.append((inputs, expected_output))
        
        # Mantém buffer limitado
        if len(self.experience_buffer) > self.max_buffer_size:
            self.experience_buffer.pop(0)
        
        # Treina periodicamente
        if len(self.experience_buffer) % 50 == 0:
            self.retrain_network()
    
    def retrain_network(self):
        """Retreina a rede com experiências recentes"""
        if len(self.experience_buffer) < 10:
            return
        
        # Usa as últimas experiências para treinar
        recent_experiences = self.experience_buffer[-50:]
        self.network.train(recent_experiences, epochs=100)
        
        # Salva modelo atualizado
        self.network.save_model(self.model_path)
    
    def train_initial_model(self):
        """Treina modelo inicial com estratégias básicas"""
        print("Treinando modelo inicial...")
        
        training_data = []
        max_hp = GAME_CONFIG['MAX_HP']
        
        # Gera dados de treinamento baseados em estratégias básicas
        for _ in range(500):
            player_hp = random.randint(50, max_hp)
            enemy_hp = random.randint(50, max_hp)
            player_defending = random.choice([True, False])
            enemy_defending = random.choice([True, False])
            turn_count = random.randint(1, 15)
            
            inputs = self.game_state_to_input(player_hp, enemy_hp, 
                                            player_defending, enemy_defending, 
                                            turn_count)
            
            # Estratégia básica para gerar dados de treinamento
            if player_hp < max_hp * 0.3:  # HP baixo
                action = 'heal'
            elif enemy_hp < max_hp * 0.3:  # Inimigo com HP baixo
                action = 'attack'
            elif enemy_hp > player_hp * 1.5:  # Inimigo muito mais forte
                action = 'defend'
            else:
                action = 'attack'
            
            expected_output = self.action_to_output(action)
            training_data.append((inputs, expected_output))
        
        # Treina a rede
        self.network.train(training_data, epochs=1000)
        
        # Salva modelo inicial
        self.network.save_model(self.model_path)
        print("Modelo inicial treinado e salvo!")
    
    def get_performance_stats(self) -> dict:
        """Retorna estatísticas de performance da IA"""
        return {
            'training_epochs': len(self.network.performance_history),
            'experience_count': len(self.experience_buffer),
            'last_error': self.network.performance_history[-1] if self.network.performance_history else 0,
            'model_exists': os.path.exists(self.model_path)
        }


# Função de conveniência para usar a IA neural
def create_neural_ai() -> NeuralAI:
    """Cria e retorna uma instância da IA neural"""
    return NeuralAI()


if __name__ == "__main__":
    # Teste da rede neural
    print("Testando rede neural...")
    
    ai = NeuralAI()
    
    # Simula algumas decisões
    for i in range(5):
        player_hp = random.randint(100, 300)
        enemy_hp = random.randint(100, 300)
        
        action = ai.decide_action(player_hp, enemy_hp, turn_count=i+1)
        print(f"Estado: Player HP={player_hp}, Enemy HP={enemy_hp}")
        print(f"Ação escolhida: {action}")
        
        # Simula aprendizado
        result_score = random.uniform(-1, 1)
        ai.learn_from_experience(player_hp, enemy_hp, action, result_score, turn_count=i+1)
        print(f"Resultado: {result_score:.2f}")
        print("-" * 30)
    
    print("Estatísticas da IA:", ai.get_performance_stats())