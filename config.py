# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background
PLAYER_COLOR = (60, 140, 255)  # Blue player
PLAYER_COLOR2 = (255, 140, 60)  # Orange player
PLAYER_SPEED = 6  # Speed of the player movement
PLAYER_MIN_SPEED = 2  # Reto 8: minimum speed
PLAYER_MAX_SPEED = 12  # Reto 8: maximum speed

SPAWN_OBSTACLE_DELAY = 500  # milliseconds
MIN_SPAWN_OBSTACLE_DELAY = 150  # Reto 7: minimum spawn interval (ms)
SPAWN_DELAY_STEP = 50  # Reto 7: ms removed every 10 points

OBSTACLE_MIN_SIZE = 20  # Reto 2
OBSTACLE_MAX_SIZE = 70  # Reto 2

PLAYER_LIVES = 3  # Reto 10: lives for each player
INVULNERABLE_TIME = 2000  # Reto 10: milliseconds of invulnerability after a hit

SCORES_FILE = "scores.txt"  # Reto 12: file where the scores are saved
TOP_SCORES = 5  # Reto 12: how many scores are shown
MAX_NAME_LENGTH = 12  # Reto 12: maximum length of the player's name
