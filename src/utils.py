# Utility functions for terrain generation and game helpers
import random
from platform import Platform
from obstacles import spike, fire, slow_trap, slippery, block, falling_rock, poison_pool, electric, healing_plant, bouncy
from settings import WIDTH, HEIGHT, OBSTACLE_SIZE

def load_image(path):
    import pygame
    return pygame.image.load(path).convert_alpha()


def generate_terrain(seed=None, difficulty=1, is_boss=False):
    """
    Procedurally generate platforms for a level.
    Generates taller levels for vertical exploration within screen bounds.
    
    Args:
        seed: Random seed for reproducible generation
        difficulty: Affects platform spacing and complexity (1-3)
        is_boss: If True, generate a smaller arena for boss stage
    
    Returns:
        List of Platform objects
    """
    if seed is not None:
        random.seed(seed)
    
    platforms = []
    
    if is_boss:
        # Boss arena: smaller, symmetric design
        platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40))  # Ground
        platforms.append(Platform(100, HEIGHT - 200, 200, 20))  # Left platform
        platforms.append(Platform(500, HEIGHT - 200, 200, 20))  # Right platform
        platforms.append(Platform(250, HEIGHT - 350, 300, 20))  # Top platform
    else:
        # Regular level: tall, vertical exploration
        # Always add ground platform
        platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40))
        
        # Generate vertical platforms for tall levels
        # Use more platforms but with varied vertical spacing
        # Increased min_gap to prevent super jumps and ensure systematic spacing
        min_gap = 150 - (difficulty * 20)
        max_gap = 220 - (difficulty * 30)
        min_platform_width = 100 + (difficulty * 20)
        max_platform_width = 200 + (difficulty * 30)
        
        # Start the first platform closer to the ground to maintain consistent spacing
        y = HEIGHT - 40 - random.randint(min_gap, max_gap)
        x = random.randint(50, WIDTH - 150)
        
        # Generate platforms with consistent spacing all the way to near the top
        # Keep generating until we're close to the top (y < 100)
        while y > 100:
            platform_width = random.randint(min_platform_width, max_platform_width)
            x = max(50, min(x + random.randint(-80, 80), WIDTH - platform_width - 50))
            platforms.append(Platform(x, y, platform_width, 20))
            gap = random.randint(min_gap, max_gap)
            y -= gap
        
        # If there's still space, add a final platform at the top
        if y > 40:
            top_platform_width = random.randint(min_platform_width, max_platform_width)
            top_x = (WIDTH - top_platform_width) // 2
            platforms.append(Platform(top_x, y, top_platform_width, 20))
    
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
        y = random.randint(150, HEIGHT - OBSTACLE_SIZE - 100)
        
        # Avoid creating spike_row to keep obstacle count manageable
        # Single obstacles only to meet the 4-6 constraint
        obstacles.append(obstacle_type(x, y))
    
    return obstacles

