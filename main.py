import json
import os

SAVE_FILE = "save_data.json"

STAT_NAMES = ["Health", "Happiness", "Intelligence", "Wealth", "Social"]


class Player:
    def __init__(self, name):
        self.name = name
        self.age = 0
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

    def to_dict(self):
        return {"name": self.name, "age": self.age, "stats": self.stats}

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])
        player.age = data["age"]
        player.stats = data["stats"]
        return player


SAMPLE_EVENTS = [
    {
        "year": 5,
        "text": "You're starting kindergarten. The other kids are playing tag on the playground.",
        "choices": [
            {
                "text": "Join the game and run around",
                "effects": {"Health": 5, "Social": 10, "Happiness": 5},
            },
            {
                "text": "Sit alone and read a picture book",
                "effects": {"Intelligence": 10, "Happiness": 5, "Social": -5},
            },
            {
                "text": "Cry and ask to go home",
                "effects": {"Happiness": -10, "Social": -5},
            },
        ],
    },
    {
        "year": 12,
        "text": "You're in middle school. A group of popular kids invites you to sit with them at lunch.",
        "choices": [
            {
                "text": "Sit with them and try to fit in",
                "effects": {"Social": 15, "Happiness": 5, "Intelligence": -5},
            },
            {
                "text": "Decline and sit with your quieter friends",
                "effects": {"Happiness": 10, "Social": 5, "Intelligence": 5},
            },
            {
                "text": "Eat lunch alone in the library",
                "effects": {"Intelligence": 10, "Social": -10, "Happiness": -5},
            },
        ],
    },
    {
        "year": 16,
        "text": "You're old enough to get a part-time job. Your friend offers to help you apply at a local shop.",
        "choices": [
            {
                "text": "Take the job and start earning money",
                "effects": {"Wealth": 15, "Happiness": -5, "Intelligence": 5},
            },
            {
                "text": "Focus on school and extracurriculars instead",
                "effects": {"Intelligence": 10, "Happiness": 5, "Social": 5},
            },
            {
                "text": "Spend the summer playing video games",
                "effects": {"Happiness": 10, "Health": -5, "Wealth": -5},
            },
        ],
    },
    {
        "year": 18,
        "text": "High school is over. What's your next step?",
        "choices": [
            {
                "text": "Go to a four-year university",
                "effects": {"Intelligence": 20, "Wealth": -15, "Social": 10},
            },
            {
                "text": "Go to community college",
                "effects": {"Intelligence": 10, "Wealth": -5, "Happiness": 5},
            },
            {
                "text": "Start working full-time right away",
                "effects": {"Wealth": 20, "Intelligence": -5, "Happiness": 5},
            },
        ],
    },
    {
        "year": 25,
        "text": "You're in your mid-twenties. A close friend invites you on a cross-country road trip.",
        "choices": [
            {
                "text": "Go on the adventure",
                "effects": {"Happiness": 15, "Social": 10, "Wealth": -10},
            },
            {
                "text": "Stay and save money for the future",
                "effects": {"Wealth": 15, "Happiness": -5, "Health": 5},
            },
            {
                "text": "Compromise — take a shorter trip",
                "effects": {"Happiness": 5, "Social": 5, "Wealth": -5},
            },
        ],
    },
]


def get_ending(stats):
    dominant = max(stats, key=stats.get)
    endings = {
        "Health": "You lived a long, healthy life. You spent your days hiking, gardening, and enjoying nature. People admired your vitality.",
        "Happiness": "You found true joy in the simple things. Your warm smile and positive energy made everyone around you happier.",
        "Intelligence": "You became a brilliant mind in your field. Your discoveries changed the way people understand the world.",
        "Wealth": "You built an empire from nothing. Money wasn't everything, but it gave you freedom and security.",
        "Social": "You were surrounded by people who loved you. Your friendships and relationships were the greatest treasure of your life.",
    }
    return endings[dominant]


class Game:
    def __init__(self, events=None):
        self.events = events or SAMPLE_EVENTS
        self.player = None

    def run(self):
        print("=" * 40)
        print("     LIFE SIMULATOR")
        print("=" * 40)

        # Check for saved game
        if os.path.exists(SAVE_FILE):
            choice = input("Save file found. Load it? (y/n): ").strip().lower()
            if choice == "y":
                self.load()
            else:
                name = input("Enter your name: ").strip()
                self.player = Player(name)
        else:
            name = input("Enter your name: ").strip()
            self.player = Player(name)

        print(f"\nWelcome, {self.player.name}! Your life begins now.\n")

        for event in self.events:
            self.player.age = event["year"]
            print(f"--- Age {event['year']} ---")
            print(event["text"])
            print()

            chosen = self.get_choice(event["choices"])
            self.player.apply_effects(chosen["effects"])

            print(f"\nYou chose: {chosen['text']}")
            print(self.player)
            print()

            # Save after each year
            self.save()

        # Game over — show ending
        print("=" * 40)
        print("Your life story has come to an end.")
        print("=" * 40)
        print(self.player)
        print()
        print(get_ending(self.player.stats))

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
