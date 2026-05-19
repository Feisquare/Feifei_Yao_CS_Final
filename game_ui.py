import tkinter as tk
from tkinter import messagebox
import json
import os

from main import Player, SAMPLE_EVENTS, get_ending, SAVE_FILE

STAT_COLORS = {
    "Health": "#4CAF50",
    "Happiness": "#FFC107",
    "Intelligence": "#2196F3",
    "Wealth": "#FF9800",
    "Social": "#9C27B0",
}

BG = "#1a1a2e"
FG = "#e0e0e0"
ACCENT = "#e94560"
BTN_BG = "#16213e"
BTN_ACTIVE = "#0f3460"


class LifeSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Simulator")
        self.root.geometry("700x650")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.player = None
        self.events = SAMPLE_EVENTS
        self.current_event = 0
        self.stat_bars = {}

        self.show_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.stat_bars = {}

    # ── START SCREEN ──────────────────────────────────────────────

    def show_start_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(
            frame, text="LIFE SIMULATOR", font=("Helvetica", 36, "bold"),
            bg=BG, fg=ACCENT
        ).pack(pady=(0, 10))

        tk.Label(
            frame, text="Every choice shapes your future",
            font=("Helvetica", 14), bg=BG, fg=FG
        ).pack(pady=(0, 40))

        tk.Label(
            frame, text="Enter your name:", font=("Helvetica", 14),
            bg=BG, fg=FG
        ).pack()

        self.name_entry = tk.Entry(
            frame, font=("Helvetica", 16), width=20,
            bg=BTN_BG, fg=FG, insertbackground=FG,
            relief="flat", justify="center"
        )
        self.name_entry.pack(pady=10)
        self.name_entry.focus()

        btn_frame = tk.Frame(frame, bg=BG)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame, text="New Game", font=("Helvetica", 14, "bold"),
            bg=ACCENT, fg="white", activebackground=BTN_ACTIVE,
            relief="flat", padx=20, pady=8, command=self.start_game
        ).pack(side="left", padx=10)

        if os.path.exists(SAVE_FILE):
            tk.Button(
                btn_frame, text="Load Game", font=("Helvetica", 14),
                bg=BTN_BG, fg=FG, activebackground=BTN_ACTIVE,
                relief="flat", padx=20, pady=8, command=self.load_game
            ).pack(side="left", padx=10)

        self.name_entry.bind("<Return>", lambda e: self.start_game())

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name Required", "Please enter your name.")
            return
        self.player = Player(name)
        self.current_event = 0
        self.show_game_screen()

    def load_game(self):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            self.player = Player.from_dict(data)
            # Find the next event based on player age
            self.current_event = 0
            for i, event in enumerate(self.events):
                if event["year"] > self.player.age:
                    self.current_event = i
                    break
            else:
                self.current_event = len(self.events)
            if self.current_event >= len(self.events):
                self.show_ending_screen()
            else:
                self.show_game_screen()
        except (json.JSONDecodeError, KeyError):
            messagebox.showerror("Error", "Save file is corrupted. Starting new game.")

    # ── GAME SCREEN ───────────────────────────────────────────────

    def show_game_screen(self):
        self.clear_screen()

        event = self.events[self.current_event]
        self.player.age = event["year"]

        # Top bar — age and name
        top = tk.Frame(self.root, bg=BTN_BG, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top, text=f"  {self.player.name}", font=("Helvetica", 16, "bold"),
            bg=BTN_BG, fg=FG
        ).pack(side="left", padx=10)

        tk.Label(
            top, text=f"Age {event['year']}  ", font=("Helvetica", 16),
            bg=BTN_BG, fg=ACCENT
        ).pack(side="right", padx=10)

        # Progress indicator
        progress_text = f"Year {self.current_event + 1} of {len(self.events)}"
        tk.Label(
            top, text=progress_text, font=("Helvetica", 11),
            bg=BTN_BG, fg="#888"
        ).pack(side="right", padx=10)

        # Main content area
        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Story text
        story_frame = tk.Frame(content, bg="#16213e", bd=0, highlightthickness=1,
                               highlightbackground="#333")
        story_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            story_frame, text=event["text"], font=("Helvetica", 14),
            bg="#16213e", fg=FG, wraplength=600, justify="left", padx=15, pady=15
        ).pack()

        # Choices
        tk.Label(
            content, text="What will you do?", font=("Helvetica", 13, "bold"),
            bg=BG, fg=ACCENT
        ).pack(anchor="w", pady=(0, 8))

        for i, choice in enumerate(event["choices"], 1):
            btn = tk.Button(
                content, text=f"  {i}.  {choice['text']}",
                font=("Helvetica", 12), bg=BTN_BG, fg=FG,
                activebackground=BTN_ACTIVE, activeforeground="white",
                relief="flat", anchor="w", padx=15, pady=10,
                command=lambda c=choice: self.make_choice(c)
            )
            btn.pack(fill="x", pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=BTN_ACTIVE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BTN_BG))

        # Stats panel at bottom
        self.show_stats_panel()

    def show_stats_panel(self):
        stats_frame = tk.Frame(self.root, bg=BTN_BG, height=130)
        stats_frame.pack(fill="x", side="bottom")
        stats_frame.pack_propagate(False)

        tk.Label(
            stats_frame, text="Stats", font=("Helvetica", 11, "bold"),
            bg=BTN_BG, fg="#888"
        ).pack(anchor="w", padx=15, pady=(8, 2))

        for stat, value in self.player.stats.items():
            row = tk.Frame(stats_frame, bg=BTN_BG)
            row.pack(fill="x", padx=15, pady=2)

            tk.Label(
                row, text=f"{stat}:", font=("Helvetica", 10),
                bg=BTN_BG, fg=FG, width=12, anchor="w"
            ).pack(side="left")

            bar_bg = tk.Frame(row, bg="#333", height=14, width=300)
            bar_bg.pack(side="left", padx=(5, 10))
            bar_bg.pack_propagate(False)

            bar_fill = tk.Frame(bar_bg, bg=STAT_COLORS[stat], height=14)
            bar_fill.place(x=0, y=0, width=int(value * 3), height=14)

            tk.Label(
                row, text=str(value), font=("Helvetica", 10, "bold"),
                bg=BTN_BG, fg=STAT_COLORS[stat], width=4
            ).pack(side="left")

            self.stat_bars[stat] = (bar_bg, bar_fill)

    def make_choice(self, choice):
        self.player.apply_effects(choice["effects"])
        self.save_game()
        self.current_event += 1

        if self.current_event >= len(self.events):
            self.show_ending_screen()
        else:
            self.show_game_screen()

    # ── ENDING SCREEN ─────────────────────────────────────────────

    def show_ending_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(
            frame, text="Your Life Story", font=("Helvetica", 30, "bold"),
            bg=BG, fg=ACCENT
        ).pack(pady=(0, 5))

        tk.Label(
            frame, text=f"{self.player.name}'s Journey is Complete",
            font=("Helvetica", 14), bg=BG, fg=FG
        ).pack(pady=(0, 25))

        # Final stats
        stats_frame = tk.Frame(frame, bg="#16213e", padx=20, pady=15)
        stats_frame.pack(pady=(0, 20))

        for stat, value in self.player.stats.items():
            row = tk.Frame(stats_frame, bg="#16213e")
            row.pack(fill="x", pady=2)

            tk.Label(
                row, text=f"{stat}:", font=("Helvetica", 12),
                bg="#16213e", fg=FG, width=14, anchor="w"
            ).pack(side="left")

            bar_bg = tk.Frame(row, bg="#333", height=16, width=250)
            bar_bg.pack(side="left", padx=(5, 10))
            bar_bg.pack_propagate(False)

            bar_fill = tk.Frame(bar_bg, bg=STAT_COLORS[stat], height=16)
            bar_fill.place(x=0, y=0, width=int(value * 2.5), height=16)

            tk.Label(
                row, text=str(value), font=("Helvetica", 12, "bold"),
                bg="#16213e", fg=STAT_COLORS[stat], width=4
            ).pack(side="left")

        # Ending text
        dominant = max(self.player.stats, key=self.player.stats.get)
        ending = get_ending(self.player.stats)

        tk.Label(
            frame, text=f"Your dominant trait: {dominant}",
            font=("Helvetica", 13, "bold"), bg=BG, fg=STAT_COLORS[dominant]
        ).pack(pady=(0, 10))

        ending_frame = tk.Frame(frame, bg="#16213e", padx=20, pady=15)
        ending_frame.pack(pady=(0, 25))

        tk.Label(
            ending_frame, text=ending, font=("Helvetica", 13),
            bg="#16213e", fg=FG, wraplength=550, justify="center"
        ).pack()

        # Buttons
        btn_frame = tk.Frame(frame, bg=BG)
        btn_frame.pack()

        tk.Button(
            btn_frame, text="Play Again", font=("Helvetica", 13, "bold"),
            bg=ACCENT, fg="white", activebackground=BTN_ACTIVE,
            relief="flat", padx=20, pady=8, command=self.show_start_screen
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="Quit", font=("Helvetica", 13),
            bg=BTN_BG, fg=FG, activebackground=BTN_ACTIVE,
            relief="flat", padx=20, pady=8, command=self.root.quit
        ).pack(side="left", padx=10)

    # ── SAVE/LOAD ─────────────────────────────────────────────────

    def save_game(self):
        data = self.player.to_dict()
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = LifeSimulatorApp(root)
    root.mainloop()
