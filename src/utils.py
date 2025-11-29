# Utility functions for terrain generation and game helpers
import random
from platform import Platform
from obstacles import spike, fire, slow_trap, slippery, block, falling_rock, poison_pool, electric, healing_plant, bouncy
from settings import WIDTH, HEIGHT, OBSTACLE_SIZE

def load_image(path):
    import pygame
    return pygame.image.load(path).convert_alpha()


def generate_terrain(seed=None, difficulty=1):
    """
    Procedurally generate platforms for a level.
    
    Args:
        seed: Random seed for reproducible generation
        difficulty: Affects platform spacing and complexity (1-3)
    
    Returns:
        List of Platform objects
    """
    if seed is not None:
        random.seed(seed)
    
    platforms = []
    
    # Always add ground platform
    platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40))
    
    # Generate platforms based on difficulty
    min_gap = 80 - (difficulty * 20)  # Smaller gaps = harder
    max_gap = 150 - (difficulty * 30)
    min_platform_width = 100 + (difficulty * 20)
    max_platform_width = 200 + (difficulty * 30)
    
    y = HEIGHT - 150
    x = random.randint(50, WIDTH - 150)
    
    while y > 100:
        platform_width = random.randint(min_platform_width, max_platform_width)
        x = max(0, min(x + random.randint(-100, 100), WIDTH - platform_width))
        platforms.append(Platform(x, y, platform_width, 20))
        y -= random.randint(min_gap, max_gap)
    
    return platforms


def generate_obstacles(seed=None, count=10, difficulty=1):
    """
    Procedurally generate obstacles for a level.
    
    Args:
        seed: Random seed for reproducible generation
        count: Number of obstacles to generate (up to 10)
        difficulty: Affects obstacle types and damages (1-3)
    
    Returns:
        List of Obstacle objects
    """
    if seed is not None:
        random.seed(seed)
    
    count = min(count, 10)
    obstacles = []
    
    # List of obstacle generators
    obstacle_types = [spike, fire, slow_trap, slippery, block, falling_rock, 
                     poison_pool, electric, healing_plant, bouncy]
    
    for _ in range(count):
        obstacle_type = random.choice(obstacle_types)
        x = random.randint(0, WIDTH - OBSTACLE_SIZE)
        y = random.randint(100, HEIGHT - OBSTACLE_SIZE - 80)
        
        # Sometimes create spike_row instead of single obstacle
        if obstacle_type == spike and random.random() < 0.3:
            from obstacles import spike_row
            count_spikes = random.randint(2, 4)
            for s in spike_row(x, y, count=count_spikes):
                obstacles.append(s)
        else:
            obstacles.append(obstacle_type(x, y))
    
    return obstacles
