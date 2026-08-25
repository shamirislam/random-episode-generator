# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Someone who already loves The Office, Friends, or The Big Bang Theory and wants a comfort episode chosen for them. They open it on a laptop, usually while doing something else — working, cooking, eating — and they are not in a hurry. The decision is low-stakes and the point is to stop deciding.

## Product Purpose

Removes the choosing. One visit returns exactly one episode, drawn at random from 717 episodes across three sitcoms, with enough detail — title, season and episode number, still image, air date, audience rating, summary — to accept it and start watching. Success is the visitor stopping at the first or second episode shown.

## Positioning

It picks; it does not browse. There is no catalogue, no search, no grid of options, no account. A streaming service's own shuffle is buried inside a library that keeps selling you the alternatives — this surface shows one episode and nothing to compare it against.

## Operating Context

Single page, single action. The visitor lands, an episode is already chosen, and one button draws another. A channel selector in the station bug tunes the draw to one show or back to all three; it is the only control besides the draw. There is no history, no favourites, no queue; a refresh is a new episode. Typical session is a handful of draws at most.

## Capabilities and Constraints

- Flask application, one route (`/`), one Jinja template (`templates/home.html`), deployed on Vercel.
- Episode data lives in three CSVs: `the_office_episodes.csv` (202 episodes, 9 seasons), `friends_episodes.csv` (236, 10 seasons), `big_bang_theory_episodes.csv` (279, 12 seasons). Columns: name, season, number, airdate, runtime, rating, summary, image_url.
- Every episode carries a verified TMDB still image; ratings and air dates come from TVMaze. All 717 image URLs resolve.
- Per-show iconic quotes are hardcoded in `main.py`, chosen at random alongside the episode.
- Scope is one click plus one choice: the station bug picks a channel (one show, or all three). No season narrowing, no rating filters, no search.
- Every draw samples one flat pool of all 717 episodes, so each episode is equally likely; choosing a show first would have made an episode of the shortest run 38% likelier than one of the longest.
- Stack for this redesign: delegated. The user is open to a bigger rebuild; staying on Flask with server-rendered Jinja and no build step is the working assumption unless the design requires otherwise.

## Brand Commitments

Name: Random Episode Generator. Author: Shamir Islam. No logo, wordmark, or palette is committed — the previous look carries no authority.

## Evidence on Hand

Real and verified: all episode titles, numbers, air dates, audience ratings, summaries, and still images for the three shows; per-show quotes attributed to real characters. Nothing else exists — no usage numbers, no testimonials, no streaming partnerships, no user accounts. None of these may be invented.

## Product Principles

1. One episode, never a list. The moment the surface offers a comparison it has failed at its only job. Choosing a channel narrows what is drawn; it never shows two episodes at once.
2. The still image is the product. It is the fastest way a visitor recognises an episode they love.
3. Trust comes from specifics — real title, real season and episode, real air date, real rating.
4. Drawing again must cost nothing: one obvious control, always reachable.
5. Three shows, one surface. Which show came up should be instantly legible without fragmenting the design into three themes.

## Accessibility & Inclusion

No product-specific requirement established beyond ordinary web accessibility: legible contrast, keyboard-reachable controls, meaningful alt text on episode stills.
