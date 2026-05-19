from flask import Flask, render_template, request, session, redirect, url_for
from main import Player, SAMPLE_EVENTS, get_ending
import json

app = Flask(__name__)
app.secret_key = "life-simulator-secret-key"

STAT_COLORS = {
    "Health": "#4CAF50",
    "Happiness": "#FFC107",
    "Intelligence": "#2196F3",
    "Wealth": "#FF9800",
    "Social": "#9C27B0",
}


@app.route("/")
def index():
    return render_template("game.html", screen="start", player=None, events=None)


@app.route("/start", methods=["POST"])
def start():
    name = request.form.get("name", "").strip()
    if not name:
        return render_template("game.html", screen="start", error="Please enter your name.", player=None, events=None)
    player = Player(name)
    session["player"] = player.to_dict()
    session["current_event"] = 0
    return redirect(url_for("play"))


@app.route("/play")
def play():
    player_data = session.get("player")
    current = session.get("current_event", 0)

    if not player_data:
        return redirect(url_for("index"))

    player = Player.from_dict(player_data)

    if current >= len(SAMPLE_EVENTS):
        return redirect(url_for("ending"))

    event = SAMPLE_EVENTS[current]
    player.age = event["year"]

    return render_template(
        "game.html", screen="game", player=player,
        event=event, current=current + 1, total=len(SAMPLE_EVENTS),
        stat_colors=STAT_COLORS
    )


@app.route("/choose", methods=["POST"])
def choose():
    player_data = session.get("player")
    current = session.get("current_event", 0)

    if not player_data:
        return redirect(url_for("index"))

    choice_idx = int(request.form.get("choice", 0))
    event = SAMPLE_EVENTS[current]
    choice = event["choices"][choice_idx]

    player = Player.from_dict(player_data)
    player.apply_effects(choice["effects"])

    session["player"] = player.to_dict()
    session["current_event"] = current + 1

    return redirect(url_for("play"))


@app.route("/ending")
def ending():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Player.from_dict(player_data)
    ending_text = get_ending(player.stats)
    dominant = max(player.stats, key=player.stats.get)

    return render_template(
        "game.html", screen="ending", player=player,
        ending_text=ending_text, dominant=dominant,
        stat_colors=STAT_COLORS
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
