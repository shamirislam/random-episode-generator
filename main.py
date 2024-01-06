from flask import Flask, render_template, url_for
import csv
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


episode_data["The Office"] = read_csv("the_office")
episode_data["Friends"] = read_csv("friends")


@app.route("/")
def home():
  # Randomly choose between 'The Office' and 'Friends'
  chosen_show = random.choice(["The Office", "Friends"])
  episodes = episode_data.get(chosen_show, [])

  if not episodes:
    return "Files not loaded properly", 500

  episode = random.choice(episodes)
  episode[6] = html.unescape(episode[6])  # Unescape HTML entities

  # Check if image_url exists in the episode data
  image_url = episode[7] if len(episode) > 7 else None

  # Add streaming links
  streaming_links = {
    "The Office": {
      "link":
      "https://www.primevideo.com/detail/The-Office/0H7JFOPK2QO9WVZ8D9D0J5ZRQN",
      "logo": url_for("static", filename="prime_logo.png"),
      "name": "Prime Video"
    },
    "Friends": {
      "link": "https://www.netflix.com/title/70274077",
      "logo": url_for("static", filename="netflix_logo.png"),
      "name": "Netflix"
    },
  }

  streaming_info = streaming_links.get(chosen_show)

  # Render the chosen episode
  return render_template(
    "home.html",
    episode=episode,
    show=chosen_show.capitalize(),
    image_url=image_url,
    streaming_link=streaming_info["link"],
    streaming_logo=streaming_info["logo"],
    streaming_service_name=streaming_info["name"],  # new line
  )


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
