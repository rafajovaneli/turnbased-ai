import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Combate por Turnos")

        self.max_hp = 100
        self.player_hp = self.max_hp
        self.enemy_hp = self.max_hp

        # Imagens
        self.hero_img = ImageTk.PhotoImage(Image.open("game/assets/hero.png").resize((64,64)))
        self.villain_img = ImageTk.PhotoImage(Image.open("game/assets/villain.png").resize((64,64)))

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        self.hero_label = tk.Label(frame, image=self.hero_img)
        self.hero_label.grid(row=0, column=0, padx=10)

        self.villain_label = tk.Label(frame, image=self.villain_img)
        self.villain_label.grid(row=0, column=2, padx=10)

        self.player_hp_bar = ttk.Progressbar(frame, length=200, maximum=self.max_hp, style="default.Horizontal.TProgressbar")
        self.player_hp_bar.grid(row=1, column=0)

        self.enemy_hp_bar = ttk.Progressbar(frame, length=200, maximum=self.max_hp, style="default.Horizontal.TProgressbar")
        self.enemy_hp_bar.grid(row=1, column=2)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.attack_btn = tk.Button(btn_frame, text="Atacar", command=self.attack)
        self.attack_btn.pack(side="left", padx=5)

        self.defend_btn = tk.Button(btn_frame, text="Defender", command=self.defend)
        self.defend_btn.pack(side="left", padx=5)

        self.heal_btn = tk.Button(btn_frame, text="Curar", command=self.heal)
        self.heal_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reiniciar", command=self.reset)
        self.reset_btn.pack(side="left", padx=5)

        self.log = tk.Text(self.root, height=10, width=60)
        self.log.pack()

        self.update_bars()

    def log_message(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def animate_bar(self, bar):
        bar.config(style="Red.Horizontal.TProgressbar")
        self.root.after(300, lambda: bar.config(style="default.Horizontal.TProgressbar"))

    def attack(self):
        damage = random.randint(5, 20)
        if random.random() < 0.15:
            damage *= 2
            self.log_message("⚡ Dano crítico!")
        self.enemy_hp = max(0, self.enemy_hp - damage)
        self.log_message(f"Você atacou causando {damage} de dano!")
        self.animate_bar(self.enemy_hp_bar)
        self.update_bars()
        self.check_end()
        if self.enemy_hp > 0:
            self.enemy_turn()

    def defend(self):
        self.log_message("Você se defendeu!")
        self.enemy_turn()

    def heal(self):
        healing = random.randint(5, 15)
        if random.random() < 0.3:
            healing += 30
            self.log.insert(tk.END, "💖 Super cura!\n")
        self.player_hp = min(self.max_hp, self.player_hp + healing)
        self.log.insert(tk.END, f"Você se curou em {healing} pontos!\n")
        self.animate_bar(self.player_hp_bar, "light green")
        self.enemy_turn()
        self.update_bars()

    def enemy_turn(self):
        damage = random.randint(10, 25)
        self.player_hp = max(0, self.player_hp - damage)
        self.log_message(f"O inimigo atacou causando {damage} de dano!")
        self.animate_bar(self.player_hp_bar)
        self.update_bars()
        self.check_end()

    def update_bars(self):
        self.player_hp_bar["value"] = self.player_hp
        self.enemy_hp_bar["value"] = self.enemy_hp

    def check_end(self):
        if self.player_hp <= 0:
            self.log_message("💀 Você perdeu!")
            self.disable_actions()
        elif self.enemy_hp <= 0:
            self.log_message("🎉 Você venceu!")
            self.disable_actions()

    def disable_actions(self):
        self.attack_btn.config(state="disabled")
        self.defend_btn.config(state="disabled")
        self.heal_btn.config(state="disabled")

    def enable_actions(self):
        self.attack_btn.config(state="normal")
        self.defend_btn.config(state="normal")
        self.heal_btn.config(state="normal")

    def reset(self):
        self.player_hp = self.max_hp
        self.enemy_hp = self.max_hp
        self.update_bars()
        self.log.delete(1.0, tk.END)
        self.enable_actions()

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    style.theme_use("default")
    style.configure("default.Horizontal.TProgressbar", troughcolor='white', background='green')
    style.configure("Red.Horizontal.TProgressbar", troughcolor='white', background='red')

    game = GameGUI(root)
    root.mainloop()
