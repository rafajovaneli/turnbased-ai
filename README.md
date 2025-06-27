# 🕹️ Combate por Turnos com Minimax | Turn-Based Combat with Minimax

Este projeto é um **jogo de combate por turnos** desenvolvido em **Python**, com o objetivo de praticar e demonstrar o uso do **algoritmo Minimax** em um contexto de inteligência artificial para jogos.  

This project is a **turn-based combat game** developed in **Python**, aimed at practicing and demonstrating the use of the **Minimax algorithm** in a game AI context.

---

## 💡 Objetivos do projeto | Project goals

✅ Praticar a implementação do **algoritmo Minimax** em Python.  
✅ Aplicar o Minimax para tomada de decisão em um jogo simples de turnos.  
✅ Desenvolver uma interface gráfica com **Tkinter** para visualização do combate.  
✅ Adicionar elementos de sorte (dano crítico, cura acima da média) para tornar o jogo mais dinâmico.  
✅ Treinar boas práticas de organização de código em projetos Python.  

✅ Practice implementing the **Minimax algorithm** in Python.  
✅ Apply Minimax for decision-making in a simple turn-based game.  
✅ Develop a graphical interface with **Tkinter** to display the combat.  
✅ Add luck elements (critical damage, above-average healing) to make the game more dynamic.  
✅ Train good code organization practices in Python projects.

---

## 🚀 Como executar o projeto | How to run the project

1️⃣ Clone o repositório | Clone the repository:
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

2️⃣ Instale as dependências | Install dependencies:
```bash
pip install pillow
```

3️⃣ Execute o jogo com interface gráfica | Run the game with GUI:
```bash
python -m game.game_gui
```

![image](https://github.com/user-attachments/assets/b4f47591-a0f4-4dbc-8aa0-c4cca22a471d)

---

## 🎮 Como jogar | How to play

- **Atacar | Attack:** causa dano ao inimigo (chance de dano crítico). / deals damage to the enemy (chance of critical hit).  
- **Defender | Defend:** reduz o dano recebido no próximo ataque do inimigo. / reduces damage received on next enemy attack.  
- **Curar | Heal:** recupera pontos de vida (cura entre 5 e 15 pontos). / restores health points (heals between 5 and 15 points).  
- **Reiniciar | Restart:** reinicia a batalha após vitória ou derrota. / restarts the battle after a win or loss.  

💥 O inimigo é controlado pela IA e toma decisões com base no Minimax. / The enemy is AI-controlled and makes decisions using Minimax.  
⚡ A cada turno, tanto o herói quanto o inimigo realizam ações até que um seja derrotado. / Each turn, both hero and enemy perform actions until one is defeated.

---

## 🧠 Sobre o Minimax | About Minimax

O algoritmo **Minimax** foi utilizado para que a IA do inimigo escolha suas ações de forma a:
- Maximizar o seu próprio benefício.
- Minimizar as chances do jogador vencer.

The **Minimax algorithm** was used so the enemy AI selects its actions to:
- Maximize its own benefit.
- Minimize the player's chances of winning.

📌 A implementação considera profundidade limitada e estados simplificados do jogo para tomada de decisão em tempo real.  
📌 The implementation uses limited depth and simplified game states for real-time decision-making.

---

## ✨ Funcionalidades extras | Extra features

- Barra de vida animada (piscando ao sofrer dano). / Animated health bar (blinks when damaged).  
- Interface gráfica simples e clara com imagens de herói e monstro. / Simple and clear GUI with hero and monster images.  
- Elementos de sorte: dano crítico e cura acima da média. / Luck elements: critical hits and above-average healing.  
- Botões desabilitados automaticamente ao fim da partida. / Buttons automatically disabled at end of match.

---

## 🛠️ Tecnologias utilizadas | Technologies used

- Python 3  
- Tkinter (GUI)  
- Pillow (image handling)

---

## 👨‍💻 Autor | Author

Rafael Hernandes Jovaneli  

---

## 📌 Licença | License

Este projeto foi desenvolvido para fins educativos e de prática.  
This project was developed for educational and practice purposes.
