"""
Asset generation script to create all 2D pixel art sprites for the game.
Generates player, enemies, obstacles, tiles, and animations.
Uses PIL to create pixel art style graphics with transparent backgrounds.
"""

from PIL import Image, ImageDraw
import os
import math

# Define asset directory
ASSET_DIR = 'assets'
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(f'{ASSET_DIR}/player', exist_ok=True)
os.makedirs(f'{ASSET_DIR}/enemies', exist_ok=True)
os.makedirs(f'{ASSET_DIR}/obstacles', exist_ok=True)
os.makedirs(f'{ASSET_DIR}/tiles', exist_ok=True)
os.makedirs(f'{ASSET_DIR}/animations', exist_ok=True)

# Base resolution
SPRITE_SIZE = 64
ANIMATION_FRAMES = 4

def create_player_sprite():
    """Create a top-down 2D sprite for the player with vibrant colors"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Player body (vibrant blue-purple)
    body_color = (100, 150, 255)
    # Head
    draw.ellipse([(16, 8), (48, 24)], fill=body_color, outline=(50, 100, 200), width=2)
    # Body
    draw.rectangle([(20, 24), (44, 48)], fill=body_color, outline=(50, 100, 200), width=2)
    # Legs (vibrant orange-red)
    legs_color = (255, 120, 50)
    draw.rectangle([(22, 48), (32, 64)], fill=legs_color, outline=(200, 80, 20), width=1)
    draw.rectangle([(32, 48), (42, 64)], fill=legs_color, outline=(200, 80, 20), width=1)
    # Arms (light skin color)
    arms_color = (255, 200, 150)
    draw.rectangle([(12, 28), (18, 44)], fill=arms_color, outline=(200, 150, 100), width=1)
    draw.rectangle([(46, 28), (52, 44)], fill=arms_color, outline=(200, 150, 100), width=1)
    # Eyes (bright)
    draw.ellipse([(22, 12), (28, 18)], fill=(0, 0, 0))
    draw.ellipse([(36, 12), (42, 18)], fill=(0, 0, 0))
    # Eyes highlights
    draw.ellipse([(23, 13), (26, 15)], fill=(255, 255, 255))
    draw.ellipse([(37, 13), (40, 15)], fill=(255, 255, 255))
    
    img.save(f'{ASSET_DIR}/player/player_idle.png')
    print(f"✓ Player sprite created: {ASSET_DIR}/player/player_idle.png")
    return img

def create_enemy_sprite():
    """Create a dark forest creature enemy sprite with menacing look"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark body (menacing dark green)
    body_color = (40, 80, 30)
    # Main body
    draw.ellipse([(12, 16), (52, 52)], fill=body_color, outline=(20, 40, 15), width=2)
    # Head (pointy, menacing)
    draw.polygon([(28, 8), (36, 8), (44, 20), (32, 24), (20, 20)], 
                 fill=(30, 60, 20), outline=(15, 30, 10), width=2)
    # Eyes (evil red glow)
    draw.ellipse([(22, 14), (28, 20)], fill=(200, 0, 0))
    draw.ellipse([(36, 14), (42, 20)], fill=(200, 0, 0))
    # Eye highlights (menacing)
    draw.ellipse([(24, 15), (26, 17)], fill=(255, 100, 100))
    draw.ellipse([(38, 15), (40, 17)], fill=(255, 100, 100))
    # Spikes/spines (dark purple)
    spike_color = (100, 20, 100)
    draw.polygon([(14, 20), (12, 12), (16, 18)], fill=spike_color, outline=(60, 10, 60))
    draw.polygon([(50, 20), (52, 12), (48, 18)], fill=spike_color, outline=(60, 10, 60))
    draw.polygon([(28, 10), (26, 2), (30, 8)], fill=spike_color, outline=(60, 10, 60))
    draw.polygon([(36, 10), (38, 2), (34, 8)], fill=spike_color, outline=(60, 10, 60))
    # Claws (dark gray)
    claw_color = (80, 80, 80)
    draw.polygon([(10, 40), (6, 45), (8, 40)], fill=claw_color)
    draw.polygon([(54, 40), (58, 45), (56, 40)], fill=claw_color)
    
    img.save(f'{ASSET_DIR}/enemies/forest_creature.png')
    print(f"✓ Enemy sprite created: {ASSET_DIR}/enemies/forest_creature.png")
    return img

def create_terrain_tiles():
    """Create a set of 2D pixel art tiles for forest terrain"""
    tiles = {
        'grass': (34, 139, 34),
        'dirt': (139, 90, 43),
        'stone': (128, 128, 128),
        'grass_dirt': (80, 120, 60),
    }
    
    for tile_name, base_color in tiles.items():
        img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw base tile
        draw.rectangle([(0, 0), (SPRITE_SIZE-1, SPRITE_SIZE-1)], 
                       fill=base_color, outline=(0, 0, 0), width=1)
        
        # Add texture pattern for seamless effect
        if tile_name == 'grass':
            # Add grass tufts
            for i in range(8):
                x = (i * 8) % SPRITE_SIZE
                y = (i * 7) % SPRITE_SIZE
                draw.polygon([(x, y+8), (x+3, y), (x+6, y+8)], 
                           fill=(50, 180, 50))
        elif tile_name == 'dirt':
            # Add dirt speckles
            for i in range(10):
                x = (i * 13) % SPRITE_SIZE
                y = (i * 11) % SPRITE_SIZE
                draw.ellipse([(x, y), (x+2, y+2)], fill=(200, 150, 100))
        elif tile_name == 'stone':
            # Add stone cracks
            for i in range(3):
                x = (i * 20) % SPRITE_SIZE
                y = (i * 20) % SPRITE_SIZE
                draw.line([(x, y), (x+15, y+10)], fill=(64, 64, 64), width=1)
        
        img.save(f'{ASSET_DIR}/tiles/{tile_name}.png')
    
    print(f"✓ Terrain tiles created: grass, dirt, stone, grass_dirt")

def create_obstacle_sprites():
    """Create pixel art sprites for all obstacles"""
    obstacles = {
        'spike': (220, 50, 50),
        'fire': (255, 120, 0),
        'slow_trap': (150, 150, 255),
        'slippery': (200, 200, 255),
        'block': (100, 100, 100),
        'falling_rock': (80, 50, 30),
        'poison_pool': (50, 200, 50),
        'electric': (255, 255, 0),
        'healing_plant': (100, 200, 100),
        'bouncy': (255, 100, 200),
    }
    
    for obs_name, color in obstacles.items():
        img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if obs_name == 'spike':
            # Triangle spike
            draw.polygon([(20, 2), (38, 38), (2, 38)], fill=color, outline=(150, 20, 20), width=1)
        elif obs_name == 'fire':
            # Flame shape
            draw.polygon([(10, 30), (20, 5), (30, 30), (25, 35), (15, 35)], 
                        fill=color, outline=(200, 80, 0), width=1)
        elif obs_name == 'slow_trap':
            # Ice/frost pattern
            draw.rectangle([(2, 2), (38, 38)], fill=color, outline=(100, 100, 200), width=1)
            draw.line([(2, 2), (38, 38)], fill=(100, 100, 200), width=1)
            draw.line([(38, 2), (2, 38)], fill=(100, 100, 200), width=1)
        elif obs_name == 'slippery':
            # Smooth waves
            for i in range(4):
                y = 10 + i * 7
                draw.arc([(5, y-3), (35, y+3)], 0, 180, fill=(100, 100, 200), width=1)
        elif obs_name == 'block':
            # Simple block
            draw.rectangle([(2, 2), (38, 38)], fill=color, outline=(50, 50, 50), width=2)
        elif obs_name == 'falling_rock':
            # Round rock
            draw.ellipse([(4, 4), (36, 36)], fill=color, outline=(40, 25, 15), width=2)
        elif obs_name == 'poison_pool':
            # Liquid pool
            draw.ellipse([(5, 10), (35, 38)], fill=color, outline=(30, 150, 30), width=1)
            draw.ellipse([(8, 15), (18, 25)], fill=(100, 255, 100))
        elif obs_name == 'electric':
            # Bolt/electric
            draw.polygon([(14, 2), (18, 14), (12, 18), (20, 38), (16, 22), (22, 18), (14, 2)], 
                        fill=color, outline=(200, 200, 0), width=1)
        elif obs_name == 'healing_plant':
            # Plant/flower
            draw.ellipse([(14, 20), (26, 36)], fill=(50, 100, 50))  # Stem
            draw.ellipse([(10, 8), (16, 16)], fill=color)  # Petal
            draw.ellipse([(24, 8), (30, 16)], fill=color)  # Petal
            draw.ellipse([(12, 2), (28, 10)], fill=color)  # Petal
        elif obs_name == 'bouncy':
            # Spring/bouncy
            for i in range(3):
                draw.rectangle([(6, 8+i*8), (34, 10+i*8)], fill=color, outline=(200, 50, 150), width=1)
        
        img.save(f'{ASSET_DIR}/obstacles/{obs_name}.png')
    
    print(f"✓ Obstacle sprites created: {len(obstacles)} types")

def create_player_walking_animation():
    """Create 4-frame walking animation for player (side view)"""
    for frame in range(ANIMATION_FRAMES):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Player body (consistent colors)
        body_color = (100, 150, 255)
        arms_color = (255, 200, 150)
        legs_color = (255, 120, 50)
        
        # Calculate leg and arm offset based on frame
        leg_offset = int(8 * math.sin(frame * math.pi / 2))
        arm_offset = -leg_offset
        
        # Head (fixed)
        draw.ellipse([(24, 8), (40, 20)], fill=body_color, outline=(50, 100, 200), width=1)
        # Eyes
        draw.ellipse([(26, 10), (29, 13)], fill=(0, 0, 0))
        draw.ellipse([(35, 10), (38, 13)], fill=(0, 0, 0))
        
        # Body
        draw.rectangle([(24, 20), (40, 36)], fill=body_color, outline=(50, 100, 200), width=1)
        
        # Left arm (raised/lowered)
        draw.rectangle([(18, 22 + arm_offset), (22, 34 + arm_offset)], 
                      fill=arms_color, outline=(200, 150, 100), width=1)
        # Right arm (opposite)
        draw.rectangle([(42, 22 - arm_offset), (46, 34 - arm_offset)], 
                      fill=arms_color, outline=(200, 150, 100), width=1)
        
        # Left leg (forward/back)
        draw.rectangle([(26, 36), (30, 50 + leg_offset)], 
                      fill=legs_color, outline=(200, 80, 20), width=1)
        # Right leg (opposite)
        draw.rectangle([(34, 36), (38, 50 - leg_offset)], 
                      fill=legs_color, outline=(200, 80, 20), width=1)
        
        img.save(f'{ASSET_DIR}/animations/player_walk_{frame}.png')
    
    print(f"✓ Player walking animation created: {ANIMATION_FRAMES} frames")

def create_enemy_idle_animation():
    """Create 4-frame idle animation for enemies (side view)"""
    for frame in range(ANIMATION_FRAMES):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        body_color = (40, 80, 30)
        
        # Breathing effect - slight scale change
        scale = 1.0 + 0.1 * math.sin(frame * math.pi / 2)
        
        # Body (breathing)
        offset = int(5 * (1 - scale))
        draw.ellipse([(12 + offset, 16 + offset), (52 - offset, 52 - offset)], 
                    fill=body_color, outline=(20, 40, 15), width=2)
        
        # Head (menacing)
        head_offset = int(2 * math.sin(frame * math.pi / 2))
        draw.polygon([(28, 8 + head_offset), (36, 8 + head_offset), 
                     (44, 20 + head_offset), (32, 24 + head_offset), 
                     (20, 20 + head_offset)], 
                    fill=(30, 60, 20), outline=(15, 30, 10), width=2)
        
        # Eyes (glowing)
        draw.ellipse([(22, 14 + head_offset), (28, 20 + head_offset)], fill=(200, 0, 0))
        draw.ellipse([(36, 14 + head_offset), (42, 20 + head_offset)], fill=(200, 0, 0))
        # Highlights pulse
        highlight_color = (255, 100 + int(100 * abs(math.sin(frame * math.pi / 2))), 100)
        draw.ellipse([(24, 15 + head_offset), (26, 17 + head_offset)], fill=highlight_color)
        draw.ellipse([(38, 15 + head_offset), (40, 17 + head_offset)], fill=highlight_color)
        
        img.save(f'{ASSET_DIR}/animations/enemy_idle_{frame}.png')
    
    print(f"✓ Enemy idle animation created: {ANIMATION_FRAMES} frames")

def main():
    """Generate all assets"""
    print("=" * 60)
    print("GENERATING PIXEL ART ASSETS")
    print("=" * 60)
    print()
    
    print("PHASE 1: Core Sprites")
    print("-" * 60)
    create_player_sprite()
    create_enemy_sprite()
    print()
    
    print("PHASE 2: Environment")
    print("-" * 60)
    create_terrain_tiles()
    create_obstacle_sprites()
    print()
    
    print("PHASE 4: Animations")
    print("-" * 60)
    create_player_walking_animation()
    create_enemy_idle_animation()
    print()
    
    print("=" * 60)
    print("✓ ALL ASSETS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Asset directory structure:")
    print(f"  {ASSET_DIR}/")
    print(f"    ├── player/")
    print(f"    ├── enemies/")
    print(f"    ├── obstacles/")
    print(f"    ├── tiles/")
    print(f"    └── animations/")

if __name__ == '__main__':
    main()
