from flask import Flask, render_template
import ast
import csv
import os
import random
import html

app = Flask(__name__)

# Pre-load episode data into memory during app initialization
episode_data = {}


def read_csv(show):
  file_path = f"./{show}_episodes.csv"
  try:
    with open(file_path, "r") as file:
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


episode_data["The Office"] = read_csv("the_office")
episode_data["Friends"] = read_csv("friends")
episode_data["The Big Bang Theory"] = read_csv("big_bang_theory")

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


@app.route("/")
def home():
  # Randomly choose one of the available shows
  chosen_show = random.choice(["The Office", "Friends", "The Big Bang Theory"])
  episodes = episode_data.get(chosen_show, [])

  if not episodes:
    return "Files not loaded properly", 500

  episode = random.choice(episodes)
  episode[6] = html.unescape(episode[6])  # Unescape HTML entities

  # Check if image_url exists in the episode data
  image_url = episode[7] if len(episode) > 7 else None

  quote = random.choice(quotes.get(chosen_show, [""]))
  airdate = episode[3] if len(episode) > 3 else None
  rating = read_rating(episode[5]) if len(episode) > 5 else None

  # Render the chosen episode
  return render_template(
    "home.html",
    episode=episode,
    show=chosen_show.capitalize(),
    image_url=image_url,
    quote=quote,
    airdate=airdate,
    rating=rating,
  )


if __name__ == '__main__':
    # The Werkzeug debugger allows arbitrary code execution, so keep it opt-in
    # via FLASK_DEBUG=1 rather than on by default.
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug)
