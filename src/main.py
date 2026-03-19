"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the music recommender from the command line.")
    parser.add_argument("--genre", default="pop", help="Favorite genre (default: pop)")
    parser.add_argument("--mood", default="happy", help="Favorite mood (default: happy)")
    parser.add_argument(
        "--energy",
        type=float,
        default=0.80,
        help="Target energy from 0.0 to 1.0 (default: 0.80)",
    )
    parser.add_argument("--k", type=int, default=5, help="Number of recommendations to return (default: 5)")
    args = parser.parse_args()

    if not 0.0 <= args.energy <= 1.0:
        parser.error("--energy must be between 0.0 and 1.0")

    if args.k <= 0:
        parser.error("--k must be a positive integer")

    return args


def main() -> None:
    args = parse_args()
    songs = load_songs("data/songs.csv")

    # Default profile for quick sanity-check runs
    taste_profile = {
        "favorite_genre": args.genre,
        "favorite_mood": args.mood,
        "target_energy": args.energy,
    }

    recommendations = recommend_songs(taste_profile, songs, k=args.k)

    print("\n" + "=" * 72)
    print("TOP RECOMMENDATIONS")
    print("=" * 72)
    for index, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{index}. {song['title']} — {song['artist']}")
        print(f"   Final score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print("-" * 72)


if __name__ == "__main__":
    main()
