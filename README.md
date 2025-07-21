# 🎮 Combate por Turnos com IA

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![AI](https://img.shields.io/badge/AI-Minimax%20%7C%20Neural-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Um jogo estratégico de combate por turnos com sistema de IA avançado**

[🎯 Demo](#-demonstração) • [🚀 Instalação](#-instalação) • [📖 Como Usar](#-como-usar) • [🤖 Tecnologias](#-tecnologias-utilizadas) • [📊 Arquitetura](#-arquitetura)

</div>

---

## 🌟 Visão Geral

Este projeto implementa um **jogo de combate por turnos** com dois tipos distintos de inteligência artificial:

- **🎯 Minimax**: Algoritmo clássico determinístico
- **🧠 Rede Neural**: Sistema adaptativo que aprende com cada partida

### ✨ Características Principais

- 🎮 **Múltiplas Interfaces**: Console, GUI simples e GUI moderna
- 🤖 **IA Dupla**: Escolha entre Minimax tradicional ou Rede Neural adaptativa
- 📊 **Sistema de Aprendizado**: IA Neural evolui e melhora com o tempo
- 🎨 **Interface Moderna**: Design responsivo com animações e feedback visual
- 📈 **Estatísticas Detalhadas**: Acompanhe seu desempenho e evolução da IA
- ⚙️ **Configuração Flexível**: Ajuste dificuldade e parâmetros facilmente

---

## 🎯 Demonstração

### Comparação dos Algoritmos

| 🎯 **Minimax**            | 🧠 **Rede Neural**           |
| ------------------------- | ---------------------------- |
| ✅ Estratégia consistente | ✅ Aprende continuamente     |
| ✅ Performance previsível | ✅ Estratégia evolutiva      |
| ✅ Boa para iniciantes    | ✅ Pode surpreender          |
| ❌ Não aprende            | ❌ Imprevisível inicialmente |

### Funcionalidades Visuais

- **Interface Moderna**: Design clean com cores temáticas para cada IA
- **Animações**: Efeitos visuais para ataques, defesa e cura
- **Feedback em Tempo Real**: Log de combate colorido e informativo
- **Estatísticas**: Acompanhamento de performance e aprendizado da IA

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/rafajovaneli/turnbased-ai.git
cd turnbased-ai

# Instale dependências opcionais
pip install numpy pillow

# Execute o jogo
python run_window_manager.py
```

### Dependências

| Biblioteca | Versão   | Obrigatória | Descrição               |
| ---------- | -------- | ----------- | ----------------------- |
| `tkinter`  | Built-in | ✅          | Interface gráfica       |
| `numpy`    | 1.19+    | ✅          | Cálculos da rede neural |
| `Pillow`   | 8.0+     | ❌          | Suporte a imagens       |

---

## 📖 Como Usar

### 🎮 Modos de Jogo

#### 1. Interface Completa (Recomendado)

```bash
python run_window_manager.py
```

- Menu principal com seleção de IA
- Interface moderna e intuitiva
- Estatísticas em tempo real

#### 2. Console Clássico

```bash
python main.py
```

- Experiência tradicional no terminal
- Ideal para desenvolvimento e testes

#### 3. Demo da IA Neural

```bash
python demo_neural_ai.py
```

- Demonstração das capacidades da IA
- Visualização do processo de aprendizado

### ⚔️ Mecânicas de Combate

| Ação            | Efeito                     | Estratégia      |
| --------------- | -------------------------- | --------------- |
| **⚔️ Atacar**   | Causa 15-25 de dano        | Ofensiva direta |
| **🛡️ Defender** | Reduz dano recebido em 50% | Proteção tática |
| **💚 Curar**    | Restaura 5-20 HP           | Recuperação     |

### 🤖 Tipos de IA

#### 🎯 Minimax

- **Profundidade**: 6 níveis de análise
- **Estratégia**: Sempre escolhe a melhor jogada possível
- **Tempo de resposta**: ~1 segundo
- **Ideal para**: Aprender padrões e estratégias básicas

#### 🧠 Rede Neural

- **Arquitetura**: 6 → 10 → 3 neurônios
- **Aprendizado**: Contínuo durante o jogo
- **Adaptação**: Muda estratégia baseada em resultados
- **Ideal para**: Desafio crescente e gameplay dinâmico

---

## 🤖 Tecnologias Utilizadas

### Core

- **Python 3.7+**: Linguagem principal
- **Tkinter**: Interface gráfica nativa
- **NumPy**: Computação científica para IA

### Algoritmos de IA

- **Minimax**: Algoritmo clássico de teoria dos jogos
- **Backpropagation**: Treinamento da rede neural
- **Sigmoid**: Função de ativação

### Arquitetura

- **MVC Pattern**: Separação clara de responsabilidades
- **Observer Pattern**: Sistema de eventos
- **Strategy Pattern**: Intercâmbio de algoritmos de IA

---

## 📊 Arquitetura

### 🏗️ Estrutura do Projeto

```
📦 combate-turnos-ia/
├── 🎮 game/                    # Módulo principal do jogo
│   ├── 🧠 neural_ai.py         # Implementação da rede neural
│   ├── 🎯 minimax.py           # Algoritmo Minimax
│   ├── 👤 entities.py          # Classes de personagens
│   ├── 🎨 enhanced_gui.py      # Interface moderna
│   ├── 🖥️ game_gui.py          # Interface simples
│   ├── 🪟 window_manager.py    # Gerenciador de janelas
│   ├── ⚙️ config.py            # Configurações centralizadas
│   └── 🎲 engine.py            # Motor do jogo
├── 🧪 tests/                   # Testes automatizados
│   └── test_engine.py
├── 🚀 run_window_manager.py    # Launcher principal
├── 🎯 demo_neural_ai.py        # Demonstração da IA
└── 📚 README.md                # Esta documentação
```

### 🧠 Arquitetura da Rede Neural

```
Entrada (6 neurônios)     Oculta (10 neurônios)    Saída (3 neurônios)
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ HP Jogador      │────┐  │                 │────┐  │ Atacar          │
│ HP Inimigo      │────┤  │   Camada        │────┤  │ Defender        │
│ Defendendo?     │────┤  │   Oculta        │────┤  │ Curar           │
│ Turno Atual     │────┤  │   (Sigmoid)     │────┤  │                 │
│ Diferença HP    │────┤  │                 │────┤  │ (Softmax)       │
│ Status Anterior │────┘  │                 │────┘  │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## ⚙️ Configuração

### 🎛️ Parâmetros Principais

```python
# game/config.py
GAME_CONFIG = {
    'MAX_HP': 300,              # Vida máxima
    'PLAYER_ATTACK': 20,        # Ataque do jogador
    'AI_ATTACK': 25,            # Ataque da IA
    'MINIMAX_DEPTH': 6,         # Profundidade Minimax
    'NEURAL_LEARNING': True,    # Aprendizado ativo
}
```

### 🎨 Personalização Visual

```python
STYLE_CONFIG = {
    'COLORS': {
        'MINIMAX': '#3498DB',   # Azul para Minimax
        'NEURAL': '#9B59B6',    # Roxo para Neural
        'PLAYER': '#27AE60',    # Verde para jogador
        'ENEMY': '#E74C3C'      # Vermelho para inimigo
    }
}
```

---

## 🧪 Testes e Qualidade

### Executar Testes

```bash
# Todos os testes
python -m unittest discover tests/

# Teste específico
python -m unittest tests.test_engine

# Com verbose
python -m unittest tests.test_engine -v
```

### 📊 Cobertura de Testes

- ✅ **Entidades**: Criação, combate, cura
- ✅ **Minimax**: Estados terminais, avaliação
- ✅ **Rede Neural**: Treinamento, predição
- ✅ **Configurações**: Validação de parâmetros

---

## 📈 Roadmap

### 🎯 Versão Atual (2.0.0)

- ✅ Dois tipos de IA funcionais
- ✅ Interface moderna
- ✅ Sistema de aprendizado
- ✅ Documentação completa

### 🚀 Próximas Versões

#### v2.1.0 - Melhorias de UX

- [ ] 🎵 Sistema de som
- [ ] 🎨 Temas visuais
- [ ] 📱 Interface responsiva
- [ ] 🏆 Sistema de conquistas

#### v2.2.0 - Recursos Avançados

- [ ] 👥 Multiplayer local
- [ ] 💾 Salvamento de progresso
- [ ] 📊 Analytics detalhados
- [ ] 🌐 Leaderboards online

#### v3.0.0 - IA Avançada

- [ ] 🧠 Redes neurais convolucionais
- [ ] 🎮 Reinforcement Learning
- [ ] 🤖 Múltiplas personalidades de IA
- [ ] 📚 Sistema de memória de longo prazo

---

## 🎓 Conceitos Demonstrados

Este projeto demonstra conhecimento em:

### 🧠 Inteligência Artificial

- **Algoritmos Clássicos**: Implementação do Minimax
- **Machine Learning**: Rede neural com backpropagation
- **Aprendizado Adaptativo**: Sistema que evolui com experiência

### 💻 Desenvolvimento de Software

- **Arquitetura Limpa**: Separação de responsabilidades
- **Padrões de Design**: MVC, Strategy, Observer
- **Testes Automatizados**: Cobertura abrangente

### 🎨 Interface e UX

- **Design Responsivo**: Interface adaptável
- **Feedback Visual**: Animações e indicadores
- **Usabilidade**: Interface intuitiva e acessível

---

## 🤝 Contribuição

### Como Contribuir

1. 🍴 Fork o projeto
2. 🌿 Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. 💾 Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. 📤 Push para a branch (`git push origin feature/nova-funcionalidade`)
5. 🔄 Abra um Pull Request

### 📋 Guidelines

- Siga o padrão PEP 8
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Use commits semânticos

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Seu Nome**

- 💼 LinkedIn: [linkedin.com/in/rafaeljovaneli](www.linkedin.com/in/rafael-jovaneli-a495b420)
- 📧 Email: rafajovaneli@gmail.com
- 🐙 GitHub: [@rafajovaneli](https://github.com/rafajovaneli

---

## 🙏 Agradecimentos

- 🎯 **Minimax Algorithm**: Baseado na teoria clássica de jogos
- 🧠 **Neural Networks**: Inspirado em trabalhos de deep learning
- 🎨 **UI/UX**: Design inspirado em jogos modernos
- 📚 **Documentação**: Seguindo melhores práticas de open source

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

[![GitHub stars](https://img.shields.io/github/stars/seu-usuario/combate-turnos-ia.svg?style=social&label=Star)](https://github.com/seu-usuario/combate-turnos-ia)
[![GitHub forks](https://img.shields.io/github/forks/seu-usuario/combate-turnos-ia.svg?style=social&label=Fork)](https://github.com/seu-usuario/combate-turnos-ia/fork)

</div>
