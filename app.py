from flask import Flask, render_template, request, session, redirect, url_for
from main import (
    Player, build_events, get_ending,
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
        session["current_event"] = 0
        _game_events[player.name] = build_events(player)
        session["game_key"] = player.name
        return redirect(url_for("play"))
    return render_template("game.html", screen="personality", player=get_player(), options=PERSONALITY_OPTIONS)


# ── GAME ─────────────────────────────────────────────────────────

@app.route("/play")
def play():
    player = get_player()
    game_key = session.get("game_key", "")
    events = _game_events.get(game_key, [])
    current = session.get("current_event", 0)

    if not player:
        return redirect(url_for("index"))

    if not events:
        # Rebuild events if missing (e.g. after server restart)
        events = build_events(player)
        _game_events[game_key] = events

    if current >= len(events):
        return redirect(url_for("ending"))

    event = events[current]
    player.age = event["year"]
    save_player(player)

    return render_template(
        "game.html", screen="game", player=player,
        event=event, current=current + 1, total=len(events),
        stat_colors=STAT_COLORS,
    )


@app.route("/choose", methods=["POST"])
def choose():
    player = get_player()
    game_key = session.get("game_key", "")
    events = _game_events.get(game_key, [])
    current = session.get("current_event", 0)

    if not player:
        return redirect(url_for("index"))

    if not events:
        events = build_events(player)
        _game_events[game_key] = events

    choice_idx = int(request.form.get("choice", 0))
    event = events[current]
    choice = event["choices"][choice_idx]

    player.apply_effects(choice["effects"])
    if "tag" in choice:
        player.history.append(choice["tag"])

    save_player(player)
    session["current_event"] = current + 1

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
