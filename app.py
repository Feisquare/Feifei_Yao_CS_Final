from flask import Flask, render_template, request, session, redirect, url_for
from main import (
    Player, build_events, get_ending, get_available_choices,
    GENDER_OPTIONS, FAMILY_OPTIONS, APPEARANCE_OPTIONS, PERSONALITY_OPTIONS,
)

app = Flask(__name__)
app.secret_key = "life-simulator-secret-key"

# Server-side event storage (session cookies are too small for full event lists)
_game_events = {}

STAT_COLORS = {
    "Health": "#4CAF50",
    "Happiness": "#FFC107",
    "Intelligence": "#2196F3",
    "Wealth": "#FF9800",
    "Social": "#9C27B0",
}


def get_player():
    data = session.get("player")
    if not data:
        return None
    return Player.from_dict(data)


def save_player(player):
    session["player"] = player.to_dict()


# ── START ────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("game.html", screen="start", player=None, error=None)


@app.route("/start", methods=["POST"])
def start():
    name = request.form.get("name", "").strip()
    if not name:
        return render_template("game.html", screen="start", error="Please enter your name.", player=None)
    player = Player(name)
    save_player(player)
    return redirect(url_for("gender"))


# ── CHARACTER CREATION ───────────────────────────────────────────

@app.route("/gender", methods=["GET", "POST"])
def gender():
    if request.method == "POST":
        player = get_player()
        player.gender = request.form.get("gender", "male")
        save_player(player)
        return redirect(url_for("family"))
    return render_template("game.html", screen="gender", player=get_player(), options=GENDER_OPTIONS)


@app.route("/family", methods=["GET", "POST"])
def family():
    if request.method == "POST":
        player = get_player()
        player.family = request.form.get("family", "middle")
        save_player(player)
        return redirect(url_for("appearance"))
    return render_template("game.html", screen="family", player=get_player(), options=FAMILY_OPTIONS)


@app.route("/appearance", methods=["GET", "POST"])
def appearance():
    if request.method == "POST":
        player = get_player()
        player.appearance = request.form.get("appearance", "average")
        save_player(player)
        return redirect(url_for("personality"))
    return render_template("game.html", screen="appearance", player=get_player(), options=APPEARANCE_OPTIONS)


@app.route("/personality", methods=["GET", "POST"])
def personality():
    if request.method == "POST":
        player = get_player()
        player.personality = request.form.get("personality", "outgoing")
        player.apply_background()
        save_player(player)
        session["current_year"] = 0
        _game_events[player.name] = build_events(player)
        session["game_key"] = player.name
        return redirect(url_for("play"))
    return render_template("game.html", screen="personality", player=get_player(), options=PERSONALITY_OPTIONS)


# ── GAME ─────────────────────────────────────────────────────────

@app.route("/play")
def play():
    player = get_player()
    game_key = session.get("game_key", "")

    if not player:
        return redirect(url_for("index"))

    # Always rebuild events to pick up consequence events based on history
    events = build_events(player)
    _game_events[game_key] = events

    current_year = session.get("current_year", 0)

    # Find the next event after the current year
    next_event = None
    next_idx = 0
    for i, event in enumerate(events):
        if event["year"] > current_year:
            next_event = event
            next_idx = i
            break

    if not next_event:
        return redirect(url_for("ending"))

    player.age = next_event["year"]
    save_player(player)

    # Get available choices (some may be locked by stat requirements)
    choices_with_status = get_available_choices(next_event["choices"], player)

    return render_template(
        "game.html", screen="game", player=player,
        event=next_event, current=next_idx + 1, total=len(events),
        stat_colors=STAT_COLORS, choices_with_status=choices_with_status,
    )


@app.route("/choose", methods=["POST"])
def choose():
    player = get_player()
    game_key = session.get("game_key", "")

    if not player:
        return redirect(url_for("index"))

    # Rebuild events with current history
    events = build_events(player)

    current_year = session.get("current_year", 0)

    # Find the event for the current year
    current_event = None
    for event in events:
        if event["year"] > current_year:
            current_event = event
            break

    if not current_event:
        return redirect(url_for("ending"))

    choice_idx = int(request.form.get("choice", 0))

    # Validate that the choice is available to the player
    choices_with_status = get_available_choices(current_event["choices"], player)
    if choice_idx >= len(choices_with_status) or not choices_with_status[choice_idx][1]:
        return redirect(url_for("play"))

    choice = current_event["choices"][choice_idx]

    player.apply_effects(choice["effects"])
    if "tag" in choice:
        player.history.append(choice["tag"])

    # Save the new year and player state
    session["current_year"] = current_event["year"]
    save_player(player)

    # Rebuild events for next play (consequence events may have changed)
    _game_events[game_key] = build_events(player)

    return redirect(url_for("play"))


# ── ENDING ───────────────────────────────────────────────────────

@app.route("/ending")
def ending():
    player = get_player()
    if not player:
        return redirect(url_for("index"))

    ending_text = get_ending(player)
    dominant = max(player.stats, key=player.stats.get)

    return render_template(
        "game.html", screen="ending", player=player,
        ending_text=ending_text, dominant=dominant,
        stat_colors=STAT_COLORS,
    )


# ── RESET ────────────────────────────────────────────────────────

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
