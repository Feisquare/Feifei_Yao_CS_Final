import json
import os

SAVE_FILE = "save_data.json"

STAT_NAMES = ["Health", "Happiness", "Intelligence", "Wealth", "Social"]

# ── CHARACTER OPTIONS ────────────────────────────────────────────

GENDER_OPTIONS = [
    {"id": "male", "text": "Male"},
    {"id": "female", "text": "Female"},
]

FAMILY_OPTIONS = [
    {
        "id": "wealthy",
        "text": "Extremely wealthy family",
        "desc": "You grew up in luxury. Money was never a problem.",
        "effects": {"Wealth": 30, "Happiness": 10},
    },
    {
        "id": "middle",
        "text": "Middle-class family",
        "desc": "A normal, stable upbringing. Nothing fancy, nothing lacking.",
        "effects": {},
    },
    {
        "id": "poor",
        "text": "Poor household",
        "desc": "Life was a struggle. But hardship builds character.",
        "effects": {"Wealth": -30, "Intelligence": 10, "Health": 5},
    },
    {
        "id": "orphan",
        "text": "Orphan",
        "desc": "You grew up without parents. The world was your teacher.",
        "effects": {"Wealth": -20, "Happiness": -20, "Intelligence": 10, "Social": -10},
    },
]

APPEARANCE_OPTIONS = [
    {
        "id": "attractive",
        "text": "Very attractive",
        "desc": "People are naturally drawn to you.",
        "effects": {"Social": 15, "Happiness": 5},
    },
    {
        "id": "average",
        "text": "Average-looking",
        "desc": "Nothing stands out, but nothing holds you back.",
        "effects": {},
    },
    {
        "id": "below_avg",
        "text": "Below average",
        "desc": "Looks aren't everything. You learned to rely on other strengths.",
        "effects": {"Social": -10, "Intelligence": 5, "Happiness": -5},
    },
]

PERSONALITY_OPTIONS = [
    {
        "id": "outgoing",
        "text": "Outgoing",
        "desc": "You love being around people. Life of the party.",
        "effects": {"Social": 10, "Happiness": 5},
    },
    {
        "id": "introvert",
        "text": "Introvert",
        "desc": "You prefer solitude and deep thinking.",
        "effects": {"Intelligence": 10, "Social": -5},
    },
    {
        "id": "ambitious",
        "text": "Ambitious",
        "desc": "You always want more. Success drives you.",
        "effects": {"Intelligence": 10, "Wealth": 5},
    },
    {
        "id": "laidback",
        "text": "Laid-back",
        "desc": "You go with the flow. Stress is for other people.",
        "effects": {"Happiness": 10, "Intelligence": -5},
    },
]


# ── PLAYER CLASS ─────────────────────────────────────────────────

class Player:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.gender = ""
        self.family = ""
        self.appearance = ""
        self.personality = ""
        self.history = []
        self.stats = {
            "Health": 50,
            "Happiness": 50,
            "Intelligence": 50,
            "Wealth": 50,
            "Social": 50,
        }

    def __str__(self):
        lines = [f"--- {self.name}, Age {self.age} ---"]
        for stat, value in self.stats.items():
            bar = "█" * (value // 5) + "░" * (20 - value // 5)
            lines.append(f"  {stat:13s} [{bar}] {value}")
        return "\n".join(lines)

    def apply_effects(self, effects):
        for stat, change in effects.items():
            if stat in self.stats:
                self.stats[stat] = max(0, min(100, self.stats[stat] + change))

    def apply_background(self):
        for opt in FAMILY_OPTIONS:
            if opt["id"] == self.family:
                self.apply_effects(opt["effects"])
        for opt in APPEARANCE_OPTIONS:
            if opt["id"] == self.appearance:
                self.apply_effects(opt["effects"])
        for opt in PERSONALITY_OPTIONS:
            if opt["id"] == self.personality:
                self.apply_effects(opt["effects"])

    def has_history(self, tag):
        return tag in self.history

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "family": self.family,
            "appearance": self.appearance,
            "personality": self.personality,
            "history": self.history,
            "stats": self.stats,
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])
        player.age = data["age"]
        player.gender = data.get("gender", "")
        player.family = data.get("family", "")
        player.appearance = data.get("appearance", "")
        player.personality = data.get("personality", "")
        player.history = data.get("history", [])
        player.stats = data["stats"]
        return player


# ── EVENTS ───────────────────────────────────────────────────────

def build_events(player):
    """Build event list based on player traits and history."""
    events = [
        # ── CHILDHOOD ──
        {
            "year": 3,
            "text": "It's your first day of preschool. The classroom is full of toys and other kids. A teacher asks you to join the group.",
            "choices": [
                {"text": "Run to the toy corner and start playing with others", "effects": {"Social": 8, "Happiness": 5}, "tag": "preschool_play"},
                {"text": "Cling to the teacher and refuse to let go", "effects": {"Happiness": -5, "Social": -3}, "tag": "preschool_cling"},
                {"text": "Sit in the corner and quietly observe", "effects": {"Intelligence": 5}, "tag": "preschool_observe"},
            ],
        },
        {
            "year": 6,
            "text": "You're in elementary school. An older kid starts picking on your classmate at recess.",
            "choices": [
                {"text": "Stand up to the bully and defend your classmate", "effects": {"Social": 10, "Happiness": 5, "Health": -5}, "tag": "stand_up_bully"},
                {"text": "Run to get a teacher immediately", "effects": {"Intelligence": 5}, "tag": "get_teacher"},
                {"text": "Walk away — it's not your problem", "effects": {"Happiness": -5, "Social": -5}, "tag": "ignore_bully"},
            ],
        },
        {
            "year": 10,
            "text": "Your school is holding a talent show. Your friends dare you to sign up.",
            "choices": [
                {"text": "Sign up and perform in front of the whole school", "effects": {"Social": 10, "Happiness": 5, "Intelligence": 5}, "tag": "talent_show"},
                {"text": "Decline — you don't want to embarrass yourself", "effects": {"Happiness": -5}, "tag": "no_talent_show"},
            ],
        },

        # ── TEEN YEARS ──
        {
            "year": 13,
            "text": "You're in middle school. A group of kids behind the gym asks you to skip class and try smoking with them.",
            "choices": [
                {"text": "Join them — you want to fit in", "effects": {"Social": 10, "Health": -15, "Happiness": 5}, "tag": "smoking"},
                {"text": "Refuse and walk away", "effects": {"Health": 5, "Intelligence": 5}, "tag": "refuse_smoking"},
                {"text": "Tell a teacher what's happening", "effects": {"Intelligence": 5, "Social": -10}, "tag": "snitch_smoking"},
            ],
        },
        {
            "year": 15,
            "text": "You notice a classmate you find really attractive. Your heart races every time you see them. A friend says they think the feeling is mutual.",
            "choices": [
                {"text": "Confess your feelings and start dating", "effects": {"Happiness": 15, "Social": 10, "Intelligence": -5}, "tag": "early_romance"},
                {"text": "Keep it to yourself — focus on studies for now", "effects": {"Intelligence": 10, "Happiness": -5}, "tag": "no_romance"},
                {"text": "Just be friends and see what happens", "effects": {"Social": 5, "Happiness": 5}, "tag": "just_friends"},
            ],
        },
        {
            "year": 16,
            "text": "Your friend offers to help you get a part-time job at a local shop. You could use the money.",
            "choices": [
                {"text": "Take the job and start earning money", "effects": {"Wealth": 15, "Happiness": -5, "Intelligence": 5}, "tag": "part_time_job"},
                {"text": "Focus on school and extracurriculars instead", "effects": {"Intelligence": 10, "Happiness": 5, "Social": 5}, "tag": "focus_school"},
                {"text": "Spend the summer playing video games", "effects": {"Happiness": 10, "Health": -5, "Wealth": -5}, "tag": "video_games"},
            ],
        },
    ]

    # ── CONSEQUENCE: ROMANCE AT 15 ──
    if player.has_history("early_romance"):
        events.append({
            "year": 17,
            "text": "Your teacher found out about your relationship. They call your parents and give you a serious talk about focusing on academics. The whole school knows now.",
            "choices": [
                {"text": "Accept the criticism and cool things off", "effects": {"Intelligence": 10, "Happiness": -10, "Social": -5}, "tag": "accept_scolding"},
                {"text": "Ignore them — love is more important", "effects": {"Happiness": 5, "Intelligence": -10, "Social": 5}, "tag": "ignore_scolding"},
                {"text": "Break up to avoid more trouble", "effects": {"Happiness": -15, "Intelligence": 5, "Social": -5}, "tag": "break_up"},
            ],
        })
    else:
        events.append({
            "year": 17,
            "text": "It's junior year. You see couples around school and wonder what you're missing. Your friends talk about prom plans.",
            "choices": [
                {"text": "Ask someone to prom", "effects": {"Social": 10, "Happiness": 10}, "tag": "prom_ask"},
                {"text": "Go with a group of friends instead", "effects": {"Social": 5, "Happiness": 5}, "tag": "prom_friends"},
                {"text": "Skip prom entirely — not your thing", "effects": {"Intelligence": 5, "Happiness": -5}, "tag": "no_prom"},
            ],
        })

    # ── CONSEQUENCE: SMOKING AT 13 ──
    if player.has_history("smoking"):
        events.append({
            "year": 17,
            "text": "You've been sneaking cigarettes for a while now. You're getting winded going up stairs. Your coach notices you can't keep up in gym class.",
            "choices": [
                {"text": "Quit smoking and start exercising", "effects": {"Health": 15, "Happiness": -5}, "tag": "quit_smoking"},
                {"text": "Keep smoking — you can quit anytime", "effects": {"Health": -15, "Happiness": 5}, "tag": "keep_smoking"},
            ],
        })

    # ── CONTINUE EVENTS ──
    events.extend([
        {
            "year": 18,
            "text": "High school is over. What's your next step?",
            "choices": [
                {"text": "Go to a four-year university", "effects": {"Intelligence": 20, "Wealth": -15, "Social": 10}, "tag": "university"},
                {"text": "Go to community college", "effects": {"Intelligence": 10, "Wealth": -5, "Happiness": 5}, "tag": "community_college"},
                {"text": "Start working full-time right away", "effects": {"Wealth": 20, "Intelligence": -5, "Happiness": 5}, "tag": "work_immediately"},
            ],
        },
        {
            "year": 20,
            "text": "You're in your early twenties. It's Friday night. Your roommates are heading to a huge party.",
            "choices": [
                {"text": "Go to the party and stay out all night", "effects": {"Social": 15, "Happiness": 10, "Health": -5, "Intelligence": -5}, "tag": "party_hard"},
                {"text": "Stay in and study for Monday's exam", "effects": {"Intelligence": 15, "Happiness": -5}, "tag": "study_hard"},
                {"text": "Go for a bit, then come home early", "effects": {"Social": 5, "Happiness": 5}, "tag": "party_moderate"},
            ],
        },
        {
            "year": 22,
            "text": "You've graduated. Two job offers are on the table.",
            "choices": [
                {"text": "Join a risky startup — high reward, high stress", "effects": {"Wealth": 15, "Happiness": -10, "Intelligence": 10}, "tag": "startup"},
                {"text": "Take the stable corporate job", "effects": {"Wealth": 10, "Happiness": 5, "Health": 5}, "tag": "corporate"},
                {"text": "Travel the world before settling down", "effects": {"Happiness": 15, "Wealth": -15, "Social": 10}, "tag": "travel"},
            ],
        },
        {
            "year": 25,
            "text": "You've been dating someone special for two years. They bring up the idea of moving in together.",
            "choices": [
                {"text": "Move in together — it feels right", "effects": {"Happiness": 15, "Social": 10, "Wealth": -5}, "tag": "move_in"},
                {"text": "You're not ready yet — keep dating", "effects": {"Happiness": -5, "Wealth": 5}, "tag": "not_ready"},
                {"text": "Break up — you want to be single", "effects": {"Happiness": -10, "Social": -5, "Intelligence": 5}, "tag": "break_up_25"},
            ],
        },
        {
            "year": 30,
            "text": "Your boss offers you a big promotion. More money, but double the hours. You'd barely see your family.",
            "choices": [
                {"text": "Take the promotion — financial security matters", "effects": {"Wealth": 20, "Happiness": -10, "Health": -5}, "tag": "promotion"},
                {"text": "Decline — work-life balance is more important", "effects": {"Happiness": 10, "Health": 5}, "tag": "decline_promotion"},
                {"text": "Negotiate for fewer hours with a smaller raise", "effects": {"Wealth": 10, "Happiness": 5, "Intelligence": 5}, "tag": "negotiate"},
            ],
        },
        {
            "year": 40,
            "text": "You're turning 40. Life feels routine. You see an ad for a completely different career path — something you always dreamed about.",
            "choices": [
                {"text": "Quit your job and chase the dream", "effects": {"Happiness": 15, "Wealth": -20, "Intelligence": 10}, "tag": "career_change"},
                {"text": "Stay where you are — stability is comfortable", "effects": {"Wealth": 10, "Happiness": -5}, "tag": "stay_stable"},
                {"text": "Start it as a side project while keeping your job", "effects": {"Happiness": 10, "Wealth": -5, "Intelligence": 5, "Health": -5}, "tag": "side_project"},
            ],
        },
        {
            "year": 50,
            "text": "Your doctor tells you your health numbers aren't great. High blood pressure, high cholesterol. Time to make a change.",
            "choices": [
                {"text": "Overhaul your lifestyle — diet, exercise, sleep", "effects": {"Health": 20, "Happiness": 5}, "tag": "health_overhaul"},
                {"text": "Cut back a little but don't obsess over it", "effects": {"Health": 5, "Happiness": 5}, "tag": "health_moderate"},
                {"text": "Ignore it — you've lived this long", "effects": {"Health": -15, "Happiness": 5}, "tag": "ignore_health"},
            ],
        },
        {
            "year": 60,
            "text": "You're retiring. How do you want to spend your retirement?",
            "choices": [
                {"text": "Travel the world with your partner", "effects": {"Happiness": 15, "Social": 10, "Wealth": -10}, "tag": "retire_travel"},
                {"text": "Volunteer and give back to the community", "effects": {"Happiness": 10, "Social": 15}, "tag": "retire_volunteer"},
                {"text": "Relax at home — you've earned it", "effects": {"Happiness": 10, "Health": 5}, "tag": "retire_relax"},
                {"text": "Start a small business you always wanted", "effects": {"Wealth": 10, "Intelligence": 5, "Happiness": 5}, "tag": "retire_business"},
            ],
        },
        {
            "year": 70,
            "text": "Your children have kids of their own. You're a grandparent now. How do you want to be remembered?",
            "choices": [
                {"text": "Be the fun grandparent — spoil them rotten", "effects": {"Happiness": 15, "Social": 10}, "tag": "fun_grandparent"},
                {"text": "Teach them life lessons and values", "effects": {"Intelligence": 10, "Happiness": 10}, "tag": "wise_grandparent"},
                {"text": "Stay distant — let the parents handle it", "effects": {"Happiness": -5, "Social": -10}, "tag": "distant_grandparent"},
            ],
        },
        {
            "year": 80,
            "text": "You're reflecting on your life. An old friend visits and asks: 'If you could do it all over again, what would you change?'",
            "choices": [
                {"text": "Nothing — every mistake made me who I am", "effects": {"Happiness": 15, "Intelligence": 5}, "tag": "no_regrets"},
                {"text": "I'd take more risks when I was young", "effects": {"Happiness": -5, "Intelligence": 5}, "tag": "more_risks"},
                {"text": "I'd spend more time with the people I love", "effects": {"Happiness": 10, "Social": 10}, "tag": "more_love"},
            ],
        },
        {
            "year": 90,
            "text": "You're in your nineties. Your body is slowing down, but your mind is still sharp. A young journalist wants to write your life story.",
            "choices": [
                {"text": "Share everything — your story could inspire others", "effects": {"Social": 15, "Happiness": 10}, "tag": "share_story"},
                {"text": "Keep your life private — some things are personal", "effects": {"Happiness": 5}, "tag": "keep_private"},
                {"text": "Write your own memoir instead", "effects": {"Intelligence": 10, "Happiness": 10}, "tag": "write_memoir"},
            ],
        },
        {
            "year": 100,
            "text": "You've lived a full century. Your family gathers around you. The room is filled with love. You close your eyes one last time.",
            "choices": [
                {"text": "Smile — it was a good life", "effects": {"Happiness": 20}, "tag": "good_life"},
                {"text": "Whisper your final words of wisdom", "effects": {"Intelligence": 10, "Social": 10}, "tag": "final_wisdom"},
            ],
        },
    ])

    # ── TRAIT-BASED EXTRA CHOICES ──
    for event in events:
        if event["year"] == 16 and player.family == "wealthy":
            event["choices"].append({
                "text": "Why work? Ask your parents for money instead",
                "effects": {"Wealth": 10, "Intelligence": -5}, "tag": "ask_parents_money"
            })
        if event["year"] == 22 and player.appearance == "attractive":
            event["choices"].append({
                "text": "Use your looks to get into modeling or entertainment",
                "effects": {"Wealth": 15, "Social": 10, "Intelligence": -5}, "tag": "modeling"}
            )
        if event["year"] == 25 and player.personality == "introvert":
            event["choices"].append({
                "text": "You prefer being alone — end the relationship",
                "effects": {"Happiness": 10, "Social": -10}, "tag": "prefer_alone"
            })

    return events


# ── ENDING ───────────────────────────────────────────────────────

def get_ending(player):
    stats = player.stats
    dominant = max(stats, key=stats.get)
    endings = {
        "Health": "You lived a long, healthy life. You spent your days hiking, gardening, and enjoying nature. People admired your vitality and wondered what your secret was.",
        "Happiness": "You found true joy in the simple things. Your warm smile and positive energy made everyone around you happier. Your laughter echoed through generations.",
        "Intelligence": "You became a brilliant mind in your field. Your discoveries changed the way people understand the world. Students will study your work for decades.",
        "Wealth": "You built an empire from nothing. Money wasn't everything, but it gave you freedom and security. Your legacy funded opportunities for others.",
        "Social": "You were surrounded by people who loved you. Your friendships and relationships were the greatest treasure of your life. No one was ever alone when you were around.",
    }
    return endings[dominant]


# ── GAME CLASS ───────────────────────────────────────────────────

class Game:
    def __init__(self):
        self.player = None
        self.events = []

    def run(self):
        print("=" * 40)
        print("     LIFE SIMULATOR")
        print("=" * 40)

        # Check for saved game
        if os.path.exists(SAVE_FILE):
            choice = input("Save file found. Load it? (y/n): ").strip().lower()
            if choice == "y":
                self.load()
                self.events = build_events(self.player)
                self.run_events()
                return

        # Character creation
        self.create_character()
        self.events = build_events(self.player)
        self.run_events()

    def create_character(self):
        print("\n--- CHARACTER CREATION ---\n")
        name = input("Enter your name: ").strip()
        self.player = Player(name)

        # Gender
        print("\nWhat is your gender?")
        for i, opt in enumerate(GENDER_OPTIONS, 1):
            print(f"  {i}. {opt['text']}")
        self.player.gender = self._pick_option(GENDER_OPTIONS)["id"]

        # Family
        print("\nWhat is your family background?")
        for i, opt in enumerate(FAMILY_OPTIONS, 1):
            print(f"  {i}. {opt['text']}")
            print(f"     {opt['desc']}")
        self.player.family = self._pick_option(FAMILY_OPTIONS)["id"]

        # Appearance
        print("\nWhat do you look like?")
        for i, opt in enumerate(APPEARANCE_OPTIONS, 1):
            print(f"  {i}. {opt['text']}")
            print(f"     {opt['desc']}")
        self.player.appearance = self._pick_option(APPEARANCE_OPTIONS)["id"]

        # Personality
        print("\nWhat is your personality?")
        for i, opt in enumerate(PERSONALITY_OPTIONS, 1):
            print(f"  {i}. {opt['text']}")
            print(f"     {opt['desc']}")
        self.player.personality = self._pick_option(PERSONALITY_OPTIONS)["id"]

        self.player.apply_background()

        print(f"\nWelcome, {self.player.name}! Your life begins now.\n")
        print(self.player)
        print()

    def _pick_option(self, options):
        while True:
            try:
                pick = int(input("Your choice: "))
                if 1 <= pick <= len(options):
                    return options[pick - 1]
                print(f"Pick a number between 1 and {len(options)}.")
            except ValueError:
                print("Please enter a number.")

    def run_events(self):
        for event in self.events:
            self.player.age = event["year"]
            print(f"--- Age {event['year']} ---")
            print(event["text"])
            print()

            chosen = self.get_choice(event["choices"])
            self.player.apply_effects(chosen["effects"])
            if "tag" in chosen:
                self.player.history.append(chosen["tag"])

            print(f"\nYou chose: {chosen['text']}")
            print(self.player)
            print()

            self.save()

        # Game over
        print("=" * 40)
        print("Your life story has come to an end.")
        print("=" * 40)
        print(self.player)
        print()
        print(get_ending(self.player))

    def get_choice(self, choices):
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice['text']}")
        print()

        while True:
            try:
                pick = int(input("Your choice: "))
                if 1 <= pick <= len(choices):
                    return choices[pick - 1]
                print(f"Pick a number between 1 and {len(choices)}.")
            except ValueError:
                print("Please enter a number.")

    def save(self):
        data = self.player.to_dict()
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        self.player = Player.from_dict(data)
        print(f"Loaded save: {self.player.name}, age {self.player.age}")


if __name__ == "__main__":
    game = Game()
    game.run()
