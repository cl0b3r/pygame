from config import *

# Reto 12: read and write the scores in scores.txt
# Each line of the file is:  name;score


def load_top_scores():
    """Read the file and return the best scores, from highest to lowest"""
    scores = []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if ";" not in line:
                    continue
                name, points = line.rsplit(";", 1)
                if points.isdigit():
                    scores.append((name, int(points)))
    except FileNotFoundError:
        pass  # No scores saved yet

    scores.sort(key=lambda item: item[1], reverse=True)
    return scores[:TOP_SCORES]


def save_score(name, points):
    """Add a new score at the end of the file"""
    with open(SCORES_FILE, "a", encoding="utf-8") as file:
        file.write(f"{name};{points}\n")
