# Global settings
WIDTH, HEIGHT = 800, 600  # Taller for vertical exploration
LEVEL_HEIGHT = 2400  # Total level height for vertical scrolling
FPS = 60
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = (50, 200, 50)
RED = (220, 50, 50)
YELLOW = (240, 200, 40)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
CYAN = (0, 200, 200)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (200, 0, 200)
GRAVITY = 0.8
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 70
ENEMY_SIZE = 40
OBSTACLE_SIZE = 40

# Game state constants
GAME_STATE_PLAYING = 0
GAME_STATE_GAMEOVER = 1
GAME_STATE_LEVEL_COMPLETE = 2
GAME_STATE_BOSS_STAGE = 3

# Level progression
NUM_REGULAR_LEVELS = 3
BOSS_LEVEL = 4
TOTAL_LEVELS = NUM_REGULAR_LEVELS + 1

# Enemy variations
ENEMY_COLORS = [RED, CYAN, MAGENTA, ORANGE, PURPLE, YELLOW, (200, 100, 50)]

# Treasure sticker tracker
MAX_STICKERS = 10

# Camera settings
CAMERA_SMOOTH_ENABLED = True     # Enable smooth scrolling
CAMERA_SMOOTH_FACTOR = 0.1       # Lerp factor (lower = smoother)
CAMERA_PLAYER_OFFSET = 0.3       # Player at 30% from top (0.0 = top, 1.0 = bottom)
CAMERA_DEADZONE = 100             # Pixels before camera starts moving
