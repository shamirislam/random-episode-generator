from flask import Flask, jsonify, render_template, request
import ast
import csv
import os
import random
import html

app = Flask(__name__)

# Pre-load episode data into memory during app initialization
episode_data = {}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Each show is announced in its own ident colour, the way a channel is
# "color" fills whole fields; "ink" is the darkened tint small text needs to
# clear 4.5:1 against the paper ground.
SHOWS = {
  "The Office": {
    "slug": "the_office", "channel": "01", "color": "#FF4B12", "ink": "#B23107"
  },
  "Friends": {
    "slug": "friends", "channel": "02", "color": "#8B5CF6", "ink": "#5B21B6"
  },
  "The Big Bang Theory": {
    "slug": "big_bang_theory", "channel": "03", "color": "#00C2D1", "ink": "#046070"
  },
}


def read_csv(show):
  file_path = os.path.join(BASE_DIR, f"{show}_episodes.csv")
  try:
    with open(file_path, "r", encoding="utf-8") as file:
      reader = csv.reader(file)
      return list(reader)[1:]  # Exclude header
  except FileNotFoundError:
    return None


def read_rating(value):
  # Ratings are stored as a "{'average': 8.1}" literal in the CSV files
  try:
    parsed = ast.literal_eval(value)
  except (ValueError, SyntaxError):
    return None
  if isinstance(parsed, dict):
    parsed = parsed.get("average")
  return parsed or None


for _show, _info in SHOWS.items():
  episode_data[_show] = read_csv(_info["slug"])

# Iconic quotes shown alongside the episode
quotes = {
  "The Office": [
    "That's what she said!",
    "I am Beyoncé, always.",
    "I'm not superstitious, but I am a little stitious.",
    "I'm an early bird and a night owl. So I'm wise and I have worms.",
    "I talk a lot, so I've learned to just tune myself out.",
    "I wish there was a way to know you're in the good old days before you've actually left them.",
    "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way.",
  ],
  "Friends": [
    "We were on a break!",
    "How you doin'?",
    "Pivot! PIVOT!",
    "Oh. My. God.",
    "It's like all my life everyone has always told me, 'You're a shoe!'",
    "Welcome to the real world. It sucks. You're gonna love it.",
    "I'm not great at the advice. Can I interest you in a sarcastic comment?",
  ],
  "The Big Bang Theory": [
    "Bazinga!",
    "Knock, knock, knock. Penny. Knock, knock, knock. Penny.",
    "That's my spot.",
    "I'm not crazy. My mother had me tested.",
    "Engineering! Where the noble, semi-skilled labourers execute the vision of those who think and dream.",
    "Oh gravity, thou art a heartless witch.",
    "One cries because one is sad. I cry because others are stupid, and that makes me sad.",
  ],
}


def draw_episode(exclude=None):
  """Pick one random episode from any show, as a flat dict for the template."""
  available = [name for name, rows in episode_data.items() if rows]
  if not available:
    return None

  chosen_show = random.choice(available)
  episodes = episode_data[chosen_show]

  episode = random.choice(episodes)
  # Avoid repeating the episode the visitor is already looking at
  if exclude and len(episodes) > 1:
    for _ in range(5):
      if f"{chosen_show}|{episode[1]}|{episode[2]}" != exclude:
        break
      episode = random.choice(episodes)

  info = SHOWS[chosen_show]
  return {
    "show": chosen_show,
    "channel": info["channel"],
    "color": info["color"],
    "ink": info["ink"],
    "title": html.unescape(episode[0]),
    "season": episode[1],
    "number": episode[2],
    "airdate": episode[3] if len(episode) > 3 else None,
    "runtime": episode[4] if len(episode) > 4 else None,
    "rating": read_rating(episode[5]) if len(episode) > 5 else None,
    "summary": html.unescape(episode[6]) if len(episode) > 6 else "",
    "image_url": episode[7] if len(episode) > 7 else None,
    "quote": random.choice(quotes.get(chosen_show, [""])),
    "id": f"{chosen_show}|{episode[1]}|{episode[2]}",
    "total": sum(len(rows) for rows in episode_data.values() if rows),
  }


OFF_AIR = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Off air - Random Episode Generator</title>
<style>
@font-face{font-family:'Archivo';src:url('/static/fonts/archivo-latin.woff2') format('woff2-variations');
font-weight:400 800;font-stretch:62% 125%;font-display:block}
html,body{height:100%;margin:0;background:#F1F3F5;color:#0B1219;
font-family:'Archivo',sans-serif;display:grid;place-items:center;text-align:center;padding:24px}
p{color:#59636F;max-width:44ch;line-height:1.5}
strong{display:block;font-size:1.5rem;font-stretch:118%;font-weight:800;letter-spacing:.06em;
text-transform:uppercase;margin-bottom:.75rem}
</style></head><body><div><strong>Off air</strong>
<p>No episode data loaded, so there is nothing to broadcast. The episode CSV files
are missing from the server.</p></div></body></html>"""


@app.route("/")
def home():
  episode = draw_episode()
  if not episode:
    return OFF_AIR, 500
  return render_template("home.html", ep=episode)


@app.route("/next")
def next_episode():
  """Draw for the client so the transition can play without a reload."""
  episode = draw_episode(exclude=request.args.get("from"))
  if not episode:
    return jsonify({"error": "no episodes loaded"}), 500
  return jsonify(episode)


if __name__ == '__main__':
    # The Werkzeug debugger allows arbitrary code execution, so keep it opt-in
    # via FLASK_DEBUG=1 rather than on by default.
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug)
