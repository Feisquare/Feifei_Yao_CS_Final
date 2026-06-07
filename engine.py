

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
        from events_data import FAMILY_OPTIONS, APPEARANCE_OPTIONS, PERSONALITY_OPTIONS
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

    def meets_requires(self, requires):
        for stat, min_val in requires.items():
            if stat == "appearance_score":
                if self.stats.get("Social", 0) < min_val:
                    return False
            elif stat in self.stats:
                if self.stats[stat] < min_val:
                    return False
        return True

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


def get_ending(player):
    stats = player.stats
    dominant = max(stats, key=stats.get)
    endings = {
        "Health": "You lived to 100 and still did yoga every morning. Your secret? Probably the crayons. You outlived everyone who doubted you. Take that, haters.",
        "Happiness": "You found joy in everything — even the bad stuff. Your laughter was contagious. Your smile could cure Mondays. People wrote songs about your positivity.",
        "Intelligence": "You became a genius who changed the world. Your IQ was so high, calculators felt insecure. Students will study your work for centuries. Nerds rule.",
        "Wealth": "You built an empire worth more than some countries. Your bank account had so many zeros, it looked like a phone number. Money can't buy happiness, but it can buy a yacht. Close enough.",
        "Social": "You had more friends than Facebook. Your phone never stopped ringing. Your parties were legendary. People wrote your name on bathroom walls. In a good way.",
    }
    return endings[dominant]


def get_available_choices(choices, player):
    result = []
    for choice in choices:
        req = choice.get("requires", {})
        if req:
            available = player.meets_requires(req)
        else:
            available = True
        result.append((choice, available))
    return result