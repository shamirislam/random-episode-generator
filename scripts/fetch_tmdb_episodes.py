"""Fetch episode data for a TV show and write it to a CSV file.

Titles, summaries, air dates and still images come from TMDB. Audience ratings and
runtimes come from TVMaze, which is the source the existing show CSVs use, so every
show in the app is scored on the same scale.

The CSV schema matches the existing show data files used by main.py:
    name,season,number,airdate,runtime,rating,summary,image_url

Usage:
    TMDB_API_KEY=xxxx python scripts/fetch_tmdb_episodes.py 1418 big_bang_theory

Arguments:
    tmdb_id   TMDB television id (e.g. 1418 for The Big Bang Theory)
    slug      Output file prefix, written as <slug>_episodes.csv in the repo root
"""

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_ROOT = "https://api.themoviedb.org/3"
TVMAZE_ROOT = "https://api.tvmaze.com"
IMAGE_ROOT = "https://image.tmdb.org/t/p/original"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_json(path, api_key, retries=3):
    """Call a TMDB endpoint and return the decoded JSON payload."""
    url = f"{API_ROOT}{path}?{urllib.parse.urlencode({'api_key': api_key, 'language': 'en-US'})}"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError(f"Failed to fetch {path}")


def fetch_tvmaze_ratings(title):
    """Return {(season, number): {"rating": float, "runtime": int}} from TVMaze.

    TVMaze is the rating source behind the other show CSVs, so reusing it keeps the
    rating-based filters and collections comparable across shows.
    """
    query = urllib.parse.urlencode({"q": title, "embed": "episodes"})
    url = f"{TVMAZE_ROOT}/singlesearch/shows?{query}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            show = json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"  TVMaze lookup failed ({error}); falling back to TMDB ratings")
        return {}

    ratings = {}
    for episode in show.get("_embedded", {}).get("episodes", []):
        if not episode.get("season"):
            continue
        ratings[(episode["season"], episode["number"])] = {
            "rating": (episode.get("rating") or {}).get("average"),
            "runtime": episode.get("runtime") or show.get("averageRuntime"),
        }
    print(f"  TVMaze: matched show '{show.get('name')}' with {len(ratings)} rated episodes")
    return ratings


def format_airdate(air_date):
    """Convert TMDB's YYYY-MM-DD into the M/D/YYYY format used by the CSVs."""
    if not air_date:
        return "N/A"
    try:
        year, month, day = air_date.split("-")
        return f"{int(month)}/{int(day)}/{int(year)}"
    except ValueError:
        return "N/A"


def clean_text(text):
    """Collapse whitespace so multi-line overviews stay on a single CSV row."""
    return " ".join((text or "").split())


def fetch_show(tmdb_id, api_key):
    show = get_json(f"/tv/{tmdb_id}", api_key)
    fallback_image = f"{IMAGE_ROOT}{show['backdrop_path']}" if show.get("backdrop_path") else ""
    default_runtime = 30
    if show.get("episode_run_time"):
        default_runtime = show["episode_run_time"][0]

    tvmaze = fetch_tvmaze_ratings(show.get("name", ""))

    rows = []
    for season in show.get("seasons", []):
        season_number = season.get("season_number")
        # Season 0 holds specials, which the other shows in this app do not include.
        if not season_number:
            continue

        data = get_json(f"/tv/{tmdb_id}/season/{season_number}", api_key)
        for episode in data.get("episodes", []):
            still_path = episode.get("still_path")
            episode_number = episode.get("episode_number")
            external = tvmaze.get((season_number, episode_number), {})

            rating = external.get("rating")
            if rating is None:
                rating = round(float(episode.get("vote_average") or 0), 1)

            rows.append({
                "name": clean_text(episode.get("name")) or f"Episode {episode_number}",
                "season": season_number,
                "number": episode_number,
                "airdate": format_airdate(episode.get("air_date")),
                "runtime": external.get("runtime") or episode.get("runtime") or default_runtime,
                "rating": "{'average': %s}" % rating,
                "summary": clean_text(episode.get("overview")) or "No summary available.",
                "image_url": f"{IMAGE_ROOT}{still_path}" if still_path else fallback_image,
            })
        print(f"  season {season_number}: {len(data.get('episodes', []))} episodes")
        time.sleep(0.25)

    return show, rows


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1

    api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        print("TMDB_API_KEY environment variable is required.")
        return 1

    tmdb_id, slug = sys.argv[1], sys.argv[2]
    show, rows = fetch_show(tmdb_id, api_key)

    if not rows:
        print("No episodes returned.")
        return 1

    output_path = os.path.join(REPO_ROOT, f"{slug}_episodes.csv")
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["name", "season", "number", "airdate", "runtime", "rating", "summary", "image_url"],
        )
        writer.writeheader()
        writer.writerows(rows)

    missing_images = sum(1 for row in rows if not row["image_url"])
    print(f"{show.get('name')}: wrote {len(rows)} episodes to {output_path}")
    print(f"episodes without an image: {missing_images}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
