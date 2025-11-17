from flask import Flask, render_template, jsonify, request
import csv
import random
import html
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Pre-load episode data into memory during app initialization
episode_data = {}
show_metadata = {}

# Episode quotes and trivia database
episode_extras = {
    'the_office': {
        'quotes': [
            "That's what she said!",
            "I am Beyoncé, always.",
            "I'm not superstitious, but I am a little stitious.",
            "Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me.",
            "I'm an early bird and a night owl. So I'm wise and I have worms.",
            "I talk a lot, so I've learned to just tune myself out.",
            "I wish there was a way to know you're in the good old days before you've actually left them.",
            "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way."
        ],
        'trivia': [
            "The show was filmed in a real office building in Van Nuys, California.",
            "John Krasinski wore a wig in season 3 because he had shaved his head for a movie role.",
            "The show's creators wanted to keep the documentary style authentic, so they avoided using a laugh track.",
            "Many of the pranks Jim plays on Dwight were improvised by the actors.",
            "The painting in Michael's office is one he painted himself (created by the props department)."
        ]
    },
    'friends': {
        'quotes': [
            "We were on a break!",
            "How you doin'?",
            "Could I BE any more...?",
            "Oh. My. God.",
            "Pivot! PIVOT!",
            "It's like all my life everyone has always told me, 'You're a shoe!'",
            "Welcome to the real world. It sucks. You're gonna love it.",
            "I'm not great at the advice. Can I interest you in a sarcastic comment?"
        ],
        'trivia': [
            "The fountain in the opening credits is located at Warner Bros. Ranch in California.",
            "The cast negotiated together to ensure they all made the same salary per episode.",
            "Central Perk was inspired by a real coffee shop called Insomnia Cafe in New York.",
            "The show was originally titled 'Insomnia Cafe' before becoming 'Friends Like Us' and finally 'Friends'.",
            "Marcel the monkey was played by two monkeys named Katie and Monkey."
        ]
    }
}

def read_csv(show_key, display_name):
    """Read episode data from CSV file with enhanced metadata"""
    file_path = f"./{show_key}_episodes.csv"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            episodes = []
            for idx, row in enumerate(reader):
                # Parse rating if it exists
                try:
                    rating_str = row.get('rating', '0')
                    if rating_str and 'average' in rating_str:
                        rating = eval(rating_str).get('average', 0)
                    else:
                        rating = 0
                except:
                    rating = 0

                # Add episode with enhanced data
                episode = {
                    'id': f"{show_key}_s{row['season']}_e{row['number']}",
                    'name': html.unescape(row['name']),
                    'season': int(row['season']),
                    'episode': int(row['number']),
                    'airdate': row.get('airdate', 'N/A'),
                    'runtime': row.get('runtime', 'N/A'),
                    'rating': rating,
                    'summary': html.unescape(row.get('summary', 'No summary available.')),
                    'image_url': row.get('image_url', ''),
                    # Add mood tags based on rating and season
                    'mood': get_episode_mood(rating, int(row['season'])),
                    # Add random quote and trivia
                    'quote': random.choice(episode_extras.get(show_key, {}).get('quotes', [''])),
                    'trivia': random.choice(episode_extras.get(show_key, {}).get('trivia', ['']))
                }
                episodes.append(episode)
            return episodes
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def get_episode_mood(rating, season):
    """Determine episode mood based on rating and other factors"""
    moods = []
    if rating >= 9.0:
        moods.append('legendary')
    if rating >= 8.5:
        moods.append('hilarious')
    if rating >= 8.0:
        moods.append('feel-good')
    if rating < 7.5:
        moods.append('chill')
    if season <= 3:
        moods.append('classic')
    if season >= 7:
        moods.append('nostalgic')

    # Add some random moods for variety
    other_moods = ['heartwarming', 'dramatic', 'romantic', 'wild', 'emotional']
    moods.append(random.choice(other_moods))

    return moods

# Load show data with enhanced metadata
show_configs = {
    'the_office': {
        'display_name': 'The Office',
        'streaming': {
            'link': 'https://www.primevideo.com/detail/The-Office/0H7JFOPK2QO9WVZ8D9D0J5ZRQN',
            'logo': '/static/prime_logo.png',
            'name': 'Prime Video'
        },
        'color': '#FF6B35',
        'emoji': '📄',
        'description': 'A mockumentary about the daily lives of office employees',
        'tags': ['comedy', 'workplace', 'mockumentary', 'sitcom']
    },
    'friends': {
        'display_name': 'Friends',
        'streaming': {
            'link': 'https://www.netflix.com/title/70274077',
            'logo': '/static/netflix_logo.png',
            'name': 'Netflix'
        },
        'color': '#F7931E',
        'emoji': '☕',
        'description': 'Six friends navigate life and love in New York City',
        'tags': ['comedy', 'friendship', 'romance', 'sitcom']
    }
}

# Load all shows
for show_key, config in show_configs.items():
    episodes = read_csv(show_key, config['display_name'])
    if episodes:
        episode_data[show_key] = episodes

        # Calculate enhanced metadata
        ratings = [ep['rating'] for ep in episodes if ep['rating'] > 0]

        show_metadata[show_key] = {
            'display_name': config['display_name'],
            'streaming': config['streaming'],
            'color': config['color'],
            'emoji': config['emoji'],
            'description': config['description'],
            'tags': config['tags'],
            'total_episodes': len(episodes),
            'seasons': max([ep['season'] for ep in episodes]),
            'avg_rating': round(sum(ratings) / len(ratings), 2) if ratings else 0,
            'top_rating': max(ratings) if ratings else 0,
            'quotes': episode_extras.get(show_key, {}).get('quotes', []),
            'trivia': episode_extras.get(show_key, {}).get('trivia', [])
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
    """Get a random episode from any show or a specific show with advanced filtering"""
    show_key = request.args.get('show', None)
    min_rating = float(request.args.get('min_rating', 0))
    season = request.args.get('season', None)
    mood = request.args.get('mood', None)

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

    if mood:
        filtered_episodes = [ep for ep in filtered_episodes if mood in ep.get('mood', [])]

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
            'streaming': show_metadata[chosen_show]['streaming'],
            'description': show_metadata[chosen_show]['description']
        }
    }

    return jsonify(episode_data_response)

@app.route("/api/search", methods=["GET"])
def search_episodes():
    """Search episodes by title, summary, or other criteria"""
    query = request.args.get('q', '').lower()
    show_key = request.args.get('show', None)

    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter required'
        }), 400

    # Determine which shows to search
    if show_key and show_key in episode_data:
        shows_to_search = [show_key]
    else:
        shows_to_search = list(episode_data.keys())

    results = []
    for show in shows_to_search:
        for episode in episode_data[show]:
            # Search in title and summary
            if (query in episode['name'].lower() or
                query in episode['summary'].lower()):
                results.append({
                    'episode': episode,
                    'show': {
                        'key': show,
                        'display_name': show_metadata[show]['display_name'],
                        'color': show_metadata[show]['color'],
                        'emoji': show_metadata[show]['emoji']
                    }
                })

    return jsonify({
        'success': True,
        'query': query,
        'count': len(results),
        'results': results[:50]  # Limit to 50 results
    })

@app.route("/api/collections", methods=["GET"])
def get_collections():
    """Get curated collections of episodes"""
    collections = {}

    for show_key, episodes in episode_data.items():
        show_info = show_metadata[show_key]

        # Top Rated
        top_rated = sorted([ep for ep in episodes if ep['rating'] > 0],
                          key=lambda x: x['rating'], reverse=True)[:10]

        # Hidden Gems (high rated but later seasons)
        hidden_gems = sorted([ep for ep in episodes if ep['rating'] >= 8.5 and ep['season'] >= 5],
                            key=lambda x: x['rating'], reverse=True)[:5]

        # Fan Favorites (ratings 9+)
        fan_favorites = [ep for ep in episodes if ep['rating'] >= 9.0]

        # Quick Watch (runtime-based if available)
        quick_watch = [ep for ep in episodes if ep.get('runtime', '30') == '30'][:10]

        collections[show_key] = {
            'show': {
                'key': show_key,
                'display_name': show_info['display_name'],
                'color': show_info['color'],
                'emoji': show_info['emoji']
            },
            'top_rated': top_rated,
            'hidden_gems': hidden_gems,
            'fan_favorites': fan_favorites,
            'quick_watch': random.sample(quick_watch, min(10, len(quick_watch)))
        }

    # All-time best across all shows
    all_episodes = []
    for show_key, episodes in episode_data.items():
        for ep in episodes:
            all_episodes.append({
                'episode': ep,
                'show': {
                    'key': show_key,
                    'display_name': show_metadata[show_key]['display_name'],
                    'color': show_metadata[show_key]['color'],
                    'emoji': show_metadata[show_key]['emoji']
                }
            })

    collections['all_shows'] = {
        'show': {
            'key': 'all',
            'display_name': 'All Shows',
            'color': '#FF6B6B',
            'emoji': '🎬'
        },
        'top_rated': sorted(all_episodes, key=lambda x: x['episode']['rating'], reverse=True)[:20],
        'legendary': [ep for ep in all_episodes if ep['episode']['rating'] >= 9.5][:10]
    }

    return jsonify({
        'success': True,
        'collections': collections
    })

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
                'episodes': [],
                'avg_rating': 0,
                'total_runtime': 0
            }
        seasons[season_num]['episode_count'] += 1
        seasons[season_num]['episodes'].append(episode)
        if episode['runtime'] != 'N/A':
            try:
                seasons[season_num]['total_runtime'] += int(episode['runtime'])
            except:
                pass

    # Calculate averages
    for season_data in seasons.values():
        ratings = [ep['rating'] for ep in season_data['episodes'] if ep['rating'] > 0]
        season_data['avg_rating'] = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return jsonify({
        'success': True,
        'show': show_metadata[show_key],
        'seasons': sorted(seasons.values(), key=lambda x: x['season'])
    })

@app.route("/api/stats", methods=["GET"])
def get_global_stats():
    """Get global statistics across all shows"""
    total_episodes = sum(len(episodes) for episodes in episode_data.values())
    all_ratings = []

    for episodes in episode_data.values():
        all_ratings.extend([ep['rating'] for ep in episodes if ep['rating'] > 0])

    return jsonify({
        'success': True,
        'stats': {
            'total_shows': len(episode_data),
            'total_episodes': total_episodes,
            'avg_rating': round(sum(all_ratings) / len(all_ratings), 2) if all_ratings else 0,
            'highest_rated': max(all_ratings) if all_ratings else 0,
            'total_seasons': sum(show['seasons'] for show in show_metadata.values())
        }
    })

@app.route("/api/achievements", methods=["POST"])
def check_achievements():
    """Check user achievements based on their history"""
    data = request.json
    history = data.get('history', [])
    favorites = data.get('favorites', [])

    achievements = []

    # First Episode
    if len(history) >= 1:
        achievements.append({
            'id': 'first_episode',
            'name': 'First Watch',
            'description': 'Generated your first episode',
            'icon': '🎬',
            'unlocked': True
        })

    # Binge Watcher
    if len(history) >= 10:
        achievements.append({
            'id': 'binge_watcher',
            'name': 'Binge Watcher',
            'description': 'Generated 10 episodes',
            'icon': '📺',
            'unlocked': True
        })

    # Super Fan
    if len(history) >= 50:
        achievements.append({
            'id': 'super_fan',
            'name': 'Super Fan',
            'description': 'Generated 50 episodes',
            'icon': '🌟',
            'unlocked': True
        })

    # Collector
    if len(favorites) >= 5:
        achievements.append({
            'id': 'collector',
            'name': 'Collector',
            'description': 'Favorited 5 episodes',
            'icon': '💖',
            'unlocked': True
        })

    # Quality Seeker
    high_rated = sum(1 for h in history if h.get('episode', {}).get('rating', 0) >= 9.0)
    if high_rated >= 5:
        achievements.append({
            'id': 'quality_seeker',
            'name': 'Quality Seeker',
            'description': 'Watched 5 episodes rated 9+',
            'icon': '⭐',
            'unlocked': True
        })

    # Show Explorer
    unique_shows = set(h.get('show', {}).get('key') for h in history)
    if len(unique_shows) >= len(episode_data):
        achievements.append({
            'id': 'show_explorer',
            'name': 'Show Explorer',
            'description': 'Watched episodes from all shows',
            'icon': '🗺️',
            'unlocked': True
        })

    return jsonify({
        'success': True,
        'achievements': achievements,
        'total_unlocked': len(achievements)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
