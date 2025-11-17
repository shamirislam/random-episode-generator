from flask import Flask, render_template, jsonify, request
import csv
import random
import html
import os
from datetime import datetime

app = Flask(__name__)

# Pre-load episode data into memory during app initialization
episode_data = {}
show_metadata = {}

def read_csv(show_key, display_name):
    """Read episode data from CSV file"""
    file_path = f"./{show_key}_episodes.csv"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            episodes = []
            for row in reader:
                # Parse rating if it exists
                try:
                    rating_str = row.get('rating', '0')
                    if rating_str and 'average' in rating_str:
                        rating = eval(rating_str).get('average', 0)
                    else:
                        rating = 0
                except:
                    rating = 0

                episodes.append({
                    'name': html.unescape(row['name']),
                    'season': int(row['season']),
                    'episode': int(row['number']),
                    'airdate': row.get('airdate', 'N/A'),
                    'runtime': row.get('runtime', 'N/A'),
                    'rating': rating,
                    'summary': html.unescape(row.get('summary', 'No summary available.')),
                    'image_url': row.get('image_url', '')
                })
            return episodes
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Load show data
show_configs = {
    'the_office': {
        'display_name': 'The Office',
        'streaming': {
            'link': 'https://www.primevideo.com/detail/The-Office/0H7JFOPK2QO9WVZ8D9D0J5ZRQN',
            'logo': '/static/prime_logo.png',
            'name': 'Prime Video'
        },
        'color': '#FF6B35',  # Coral orange
        'emoji': '📄'
    },
    'friends': {
        'display_name': 'Friends',
        'streaming': {
            'link': 'https://www.netflix.com/title/70274077',
            'logo': '/static/netflix_logo.png',
            'name': 'Netflix'
        },
        'color': '#F7931E',  # Orange
        'emoji': '☕'
    }
}

# Load all shows
for show_key, config in show_configs.items():
    episodes = read_csv(show_key, config['display_name'])
    if episodes:
        episode_data[show_key] = episodes
        show_metadata[show_key] = {
            'display_name': config['display_name'],
            'streaming': config['streaming'],
            'color': config['color'],
            'emoji': config['emoji'],
            'total_episodes': len(episodes),
            'seasons': max([ep['season'] for ep in episodes]),
            'avg_rating': round(sum([ep['rating'] for ep in episodes]) / len(episodes), 2) if episodes else 0
        }

@app.route("/")
def home():
    """Serve the main application page"""
    return render_template("index.html")

@app.route("/api/shows", methods=["GET"])
def get_shows():
    """Get list of all available shows with metadata"""
    return jsonify({
        'success': True,
        'shows': show_metadata
    })

@app.route("/api/random-episode", methods=["GET"])
def get_random_episode():
    """Get a random episode from any show or a specific show"""
    show_key = request.args.get('show', None)
    min_rating = float(request.args.get('min_rating', 0))
    season = request.args.get('season', None)

    # Determine which shows to pick from
    if show_key and show_key in episode_data:
        available_shows = [show_key]
    else:
        available_shows = list(episode_data.keys())

    if not available_shows:
        return jsonify({
            'success': False,
            'error': 'No shows available'
        }), 404

    # Pick a random show
    chosen_show = random.choice(available_shows)
    episodes = episode_data[chosen_show]

    # Apply filters
    filtered_episodes = episodes

    if min_rating > 0:
        filtered_episodes = [ep for ep in filtered_episodes if ep['rating'] >= min_rating]

    if season:
        try:
            season_num = int(season)
            filtered_episodes = [ep for ep in filtered_episodes if ep['season'] == season_num]
        except ValueError:
            pass

    if not filtered_episodes:
        return jsonify({
            'success': False,
            'error': 'No episodes match the specified filters'
        }), 404

    # Pick random episode
    episode = random.choice(filtered_episodes)

    # Add show metadata
    episode_data_response = {
        'success': True,
        'episode': episode,
        'show': {
            'key': chosen_show,
            'display_name': show_metadata[chosen_show]['display_name'],
            'color': show_metadata[chosen_show]['color'],
            'emoji': show_metadata[chosen_show]['emoji'],
            'streaming': show_metadata[chosen_show]['streaming']
        }
    }

    return jsonify(episode_data_response)

@app.route("/api/show/<show_key>/episodes", methods=["GET"])
def get_show_episodes(show_key):
    """Get all episodes for a specific show"""
    if show_key not in episode_data:
        return jsonify({
            'success': False,
            'error': 'Show not found'
        }), 404

    return jsonify({
        'success': True,
        'show': show_metadata[show_key],
        'episodes': episode_data[show_key]
    })

@app.route("/api/show/<show_key>/seasons", methods=["GET"])
def get_show_seasons(show_key):
    """Get season information for a specific show"""
    if show_key not in episode_data:
        return jsonify({
            'success': False,
            'error': 'Show not found'
        }), 404

    episodes = episode_data[show_key]
    seasons = {}

    for episode in episodes:
        season_num = episode['season']
        if season_num not in seasons:
            seasons[season_num] = {
                'season': season_num,
                'episode_count': 0,
                'episodes': []
            }
        seasons[season_num]['episode_count'] += 1
        seasons[season_num]['episodes'].append(episode)

    return jsonify({
        'success': True,
        'show': show_metadata[show_key],
        'seasons': list(seasons.values())
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
