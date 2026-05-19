### Project Title

Life Simulator

### One Sentence Pitch

My project is a text-based life simulation game where the player makes choices each year from childhood to adulthood, and those choices affect five core stats that determine one of multiple unique endings.

### Target User

Teenagers (ages 14–18) who enjoy story-based games and want to explore how different life choices can lead to different outcomes. Players who like games like BitLife or interactive fiction.

### Purpose

This project turns real-life decisions into a game, letting users explore different life paths in a fun and interactive way. It teaches cause-and-effect thinking — every choice has consequences on Health, Happiness, Intelligence, Wealth, and Social stats.

### MVP (Most Important Part)

A story-based game where the player progresses year-by-year from age 5 to 25, makes 2–3 choices at each stage, and reaches one of five unique endings based on their dominant stat.

**What is NOT in the MVP:**
- No login system or accounts
- No graphics or 3D models
- No sound or music
- No multiplayer

### Must-Have Features (3 only)

1. **Branching story system** — Each year presents a scenario with 2–3 choices. The player picks one, and the story continues.
2. **Stat system** — Five stats (Health, Happiness, Intelligence, Wealth, Social) start at 50 and change based on choices. Displayed as a visual bar (0–100).
3. **Multiple endings** — After the final year, the player's dominant stat determines their life ending (5 possible endings).

### Nice-to-Have Features (1 or 2)

1. Save/load game progress (JSON file) — already implemented
2. More story years and branching paths

### Stretch Feature (1 only)

Add more storyline — expand from 5 years to 15+ years covering more life stages (30s, 40s, retirement).

### Python Skills You Might Use

Check the boxes for skills your project will need:

- [x] Functions
- [x] Lists
- [x] Dictionaries
- [ ] APIs
- [x] File I/O (reading/writing files) — JSON save/load
- [x] Object-Oriented Programming (Classes) — Player class, Game class
- [x] Error Handling — input validation for choices

### Data Plan

1. **What data does my project need?**
   - Player data: name, age, and 5 stats (Health, Happiness, Intelligence, Wealth, Social)
   - Event data: a list of year events, each with a text description and 2–3 choices with stat effects
   - Save data: player state saved to a JSON file for loading later

2. **Where will the data come from?**
   - Player name: user input at game start
   - Choices: user picks from numbered options each year
   - Events/story: hardcoded list of dictionaries in the code (no external files needed)

3. **How will I store or organize the data?**
   - Events: list of dictionaries, each with `year`, `text`, and `choices` (list of dicts with `text` and `effects`)
   - Player stats: dictionary `{"Health": 50, "Happiness": 50, ...}`
   - Save file: JSON file (`save_data.json`) written after each year

### First Tiny Step

A Player class with 5 stats, a `__str__` method to display them as bars, and an `apply_effects` method to update stats with clamping (0–100). This was the first thing built and is now complete.

### Possible Risk

1. **Balancing the story** — Making sure choices feel meaningful and stats don't all converge to the same values. If every choice gives +5 to everything, there's no real strategy.
2. **Not enough content** — With only 5 sample years, the game feels short. Need more events to make it feel like a full life.
3. **Edge cases** — What if a player's stats hit 0? Should there be an early death mechanic, or just let it keep going?

## Part 3: Choose Your Project Lane

| Lane | Type | Examples |
|------|------|----------|
| **Lane 1: Data Tool** | Working with real-world information from APIs | Weather clothing recommender, country info explorer, movie search tool, sports stats viewer |
| **Lane 2: Personal Utility** | Practical tools you could actually use | Habit tracker, budget tracker, flashcard app, homework planner, grade calculator |
| **Lane 3: Game or Simulation** | Creative, story-driven, or competitive projects | Text adventure, battle simulator, quiz game, survival decision game, economy simulator |
| **Lane 4: Advanced Stretch** | Bigger ideas that need teacher approval | Dashboard, recommendation engine, AI-assisted study tool, data analysis project |

**Which lane did you choose?** Lane 3 — Game or Simulation

---
