# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

This recommender suggests the top 3 to 5 songs from a small catalog based on a user’s preferred genre, mood, and target energy. It is designed for classroom exploration, not real production use. It assumes users can describe their taste with a few simple preferences and that those preferences are stable during one session.

---

## 3. How the Model Works  

Each song has features like genre, mood, energy, tempo, valence, danceability, and acousticness. The user profile provides a target genre, mood, and energy (plus optional numeric preferences). The model gives points when genre or mood match and then adds similarity points based on how close the song is to the user’s target values. In my current experiment, energy has extra influence and genre has reduced influence, so songs with close energy can move up even if genre is not a perfect match.

---

## 4. Data  

The dataset is a small hand-built CSV catalog with 18 songs. It includes genres like pop, lofi, rock, ambient, jazz, synthwave, indie pop, blues, hip hop, reggae, folk, metal, latin, classical, and house, with a range of moods from happy and chill to intense and aggressive. I expanded the starter data by adding more songs to increase variety. Even with that expansion, this is still a tiny dataset and does not represent the full range of global music taste.

---

## 5. Strengths  

This system works well for users with clear preferences, like “happy pop” or “chill lofi.” The score explanations are easy to read, so it is transparent why a song ranked high or low. In testing, top results usually matched intuition when the requested mood and energy were present in the dataset. It is especially good for quickly showing how changing weights changes recommendation behavior.

---

## 6. Limitations and Bias 

One weakness I found is that the current scoring can create a small filter bubble around energy. After I doubled the energy weight, songs with very close energy values started outranking songs that matched genre better, even when the overall vibe felt less accurate. This means users with unusual or conflicting profiles (for example, very high energy plus a rare mood) can get recommendations that are mathematically close but emotionally off. The model is also sensitive to exact genre and mood labels, so users whose taste does not fit those labels can be underserved.

---

## 7. Evaluation  

I tested several profiles, including Happy Pop, Chill Lofi, Deep Intense Rock, and three edge-case profiles with conflicting preferences. I looked at the top 5 songs for each profile and checked whether the reasons matched what a listener would expect. One surprise was how often “Gym Hero” appeared for users who asked for Happy Pop. In plain terms, that happens because “Gym Hero” gets a strong boost for matching pop and also has an energy level very close to what those users requested, so it keeps beating songs that are happy but slightly farther from the energy target.

---

## 8. Future Work  

Next, I would add fuzzy matching for genre and mood so near-equivalent labels (like hip-hop vs hip hop) are treated as similar. I would also add a diversity step to avoid recommending songs that are too similar to each other in the top 5. Another improvement would be multi-preference profiles (for example, 70% pop and 30% rock) instead of one strict favorite genre. Finally, I would test with a larger and more balanced dataset.

---

## 9. Personal Reflection  

My biggest learning moment was realizing how sensitive recommendations are to small weight changes. When I shifted weight from genre to energy, the rankings changed immediately, which showed me that “accuracy” depends on what you decide to value. AI tools helped me move faster when drafting scoring ideas, edge-case tests, and documentation, but I still had to double-check outputs by running the program and reading actual recommendation reasons in the terminal. What surprised me most is that even a simple point-based system can still feel personal to a user, because it reacts to mood and energy in ways that seem intuitive. If I extended this project, I would add fuzzy matching for genre labels, a diversity rule to avoid repetitive top results, and a larger dataset so the system can represent more listening styles.
