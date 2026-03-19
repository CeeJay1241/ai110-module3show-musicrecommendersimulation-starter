from typing import List, Dict, Tuple
from dataclasses import dataclass
import pandas as pd

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _score_song(song: Song, user: UserProfile) -> Tuple[float, str]:
        """Return total score and explanation for one song against a user profile."""
        score = 0.0
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match +2.00")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append("mood match +1.00")

        energy_similarity = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        energy_points = 1.0 * energy_similarity
        score += energy_points
        reasons.append(f"energy similarity +{energy_points:.2f}")

        if user.likes_acoustic:
            acoustic_similarity = song.acousticness
        else:
            acoustic_similarity = 1.0 - song.acousticness
        acoustic_points = 0.5 * acoustic_similarity
        score += acoustic_points
        reasons.append(f"acoustic fit +{acoustic_points:.2f}")

        return float(score), ", ".join(reasons)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda song: self._score_song(song, user)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song(song, user)
        return f"Score {score:.2f} based on {reasons}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    dataframe = pd.read_csv(csv_path)
    return dataframe.to_dict(orient="records")


def _get_song_score(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Compute a weighted score and reason string for a song dictionary."""
    score = 0.0
    reasons: List[str] = []

    genre_pref = user_prefs.get("favorite_genre") or user_prefs.get("genre")
    if genre_pref and str(song["genre"]).lower() == str(genre_pref).lower():
        score += 2.0
        reasons.append("genre match +2.00")

    mood_pref = user_prefs.get("favorite_mood") or user_prefs.get("mood")
    if mood_pref and str(song["mood"]).lower() == str(mood_pref).lower():
        score += 1.0
        reasons.append("mood match +1.00")

    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    if target_energy is not None:
        energy_similarity = max(0.0, 1.0 - abs(float(song["energy"]) - float(target_energy)))
        energy_points = 1.0 * energy_similarity
        score += energy_points
        reasons.append(f"energy similarity +{energy_points:.2f}")

    target_tempo = user_prefs.get("target_tempo_bpm")
    if target_tempo is not None:
        tempo_diff = abs(float(song["tempo_bpm"]) - float(target_tempo))
        tempo_similarity = max(0.0, 1.0 - (tempo_diff / 160.0))
        tempo_points = 0.5 * tempo_similarity
        score += tempo_points
        reasons.append(f"tempo similarity +{tempo_points:.2f}")

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        valence_similarity = max(0.0, 1.0 - abs(float(song["valence"]) - float(target_valence)))
        valence_points = 0.4 * valence_similarity
        score += valence_points
        reasons.append(f"valence similarity +{valence_points:.2f}")

    target_danceability = user_prefs.get("target_danceability")
    if target_danceability is not None:
        dance_similarity = max(0.0, 1.0 - abs(float(song["danceability"]) - float(target_danceability)))
        dance_points = 0.4 * dance_similarity
        score += dance_points
        reasons.append(f"danceability similarity +{dance_points:.2f}")

    target_acousticness = user_prefs.get("target_acousticness")
    if target_acousticness is not None:
        acoustic_similarity = max(0.0, 1.0 - abs(float(song["acousticness"]) - float(target_acousticness)))
        acoustic_points = 0.3 * acoustic_similarity
        score += acoustic_points
        reasons.append(f"acousticness similarity +{acoustic_points:.2f}")

    if not reasons:
        reasons.append("default similarity")

    return float(score), ", ".join(reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, explanation = _get_song_score(song, user_prefs)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
