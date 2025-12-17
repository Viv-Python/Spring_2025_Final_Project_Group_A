# Hack-and-Slash Adventure Game

A 2D platformer hack-and-slash adventure game built with Python and Pygame, where players explore ancient ruins to find treasure while battling enemies and overcoming obstacles.

## Project Overview

The game features an explorer navigating through multiple levels of ancient ruins, fighting enemies, collecting treasure, and facing a final boss. The game emphasizes dynamic platforming mechanics, combat, and progression through procedurally-designed levels.

## Features

### Core Mechanics
- **Player Movement**: Walking, jumping, and attacking with sword combat
- **Collision Detection**: Responsive platform and obstacle collision system
- **Vertical Exploration**: 4 levels with 2400 pixel height enabling vertical scrolling
- **Dynamic Camera**: Smooth camera system with player tracking and deadzones

### Gameplay Elements
- **3 Regular Levels + 1 Boss Stage**: Progressive difficulty with varied level layouts
- **10+ Obstacle Types**:
  - Spikes, fire traps, slow traps, poison pools
  - Slippery surfaces, bouncy platforms, falling rocks
  - Electric hazards, healing plants, block obstacles
  - Spike rows, and more

- **Enemy System**: Multiple enemy types with:
  - Patrol and chase patterns
  - Melee and ranged attacks
  - Health and damage systems
  - Limited simultaneous attacks (max 2 enemies attacking at once)

- **Boss Fight**: Special boss stage with unique mechanics

- **Power-Up System**:
  - Armor Power-Ups (health boost)
  - Attack Power-Ups (damage increase)
  - Speed Power-Ups (movement speed boost)
  - Health Pickups for recovery

### Additional Features
- **Treasure Collection**: 10 sticker tracker for collectibles
- **Door Mechanics**: Vertical progression through level gates
- **Sword Combat**: Attack animations and hitbox detection
- **Health System**: Player health management with damage feedback
- **Asset Loading**: Dynamic sprite and animation loading system
- **Audio System**: Music integration for victory scenes

## Project Structure

```
├── src/                          # Main game source code
│   ├── main.py                  # Entry point for the game
│   ├── game.py                  # Core game engine and state management
│   ├── player.py                # Player class and attack mechanics
│   ├── enemies.py               # Enemy and projectile systems
│   ├── boss.py                  # Boss fight mechanics
│   ├── obstacles.py             # Obstacle types and behaviors
│   ├── platform.py              # Platform collision system
│   ├── door.py                  # Level progression doors
│   ├── treasure.py              # Treasure/collectible system
│   ├── health_pickup.py         # Health recovery items
│   ├── powerup.py               # Power-up implementations
│   ├── camera.py                # Camera system with smooth tracking
│   ├── asset_loader.py          # Asset and sprite loading
│   ├── settings.py              # Global game configuration
│   ├── utils.py                 # Utility functions (terrain/obstacle generation)
│   └── __pycache__/             # Python cache files
│
├── assets/                       # Game assets (sprites, animations, audio)
│   ├── animations/              # Character animation frames
│   ├── backgrounds/             # Level backgrounds
│   ├── dinosaurs/               # Enemy sprites (themed as animals)
│   ├── enemies/                 # Additional enemy assets
│   ├── obstacles/               # Obstacle and trap sprites
│   ├── player/                  # Player character sprites
│   └── tiles/                   # Tileset for platforms and terrain
│
├── generate_assets.py           # Asset generation script
├── generate_backgrounds.py      # Background generation utility
├── generate_bear.py             # Boss/bear sprite generation
├── generate_music.py            # Music generation utility
│
├── test_boss_bear.py            # Boss behavior tests
├── test_comprehensive_bear.py   # Comprehensive gameplay tests
├── test_game_run.py             # Game execution tests
├── test_script.py               # General script tests
├── test_visual_boss_bear.py     # Visual/rendering tests
│
├── video_game_proposal.txt      # Original project proposal
└── README.md                    # This file
```

## Game Settings

Key configuration values in `settings.py`:
- **Screen Resolution**: 800x600 pixels
- **Level Height**: 2400 pixels (for vertical exploration)
- **FPS**: 60 frames per second
- **Player Size**: 50x70 pixels
- **Enemy Size**: 40x40 pixels
- **Obstacle Size**: 40x40 pixels
- **Total Levels**: 4 (3 regular + 1 boss stage)
- **Camera Smoothing**: Enabled with lerp factor of 0.1

## Installation

### Prerequisites
- Python 3.7+
- Pygame library

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Viv-Python/Spring_2025_Final_Project_Group_A.git
cd Spring_2025_Final_Project_Group_A
```

2. Install dependencies:
```bash
pip install pygame
```

3. Generate or prepare game assets:
```bash
python generate_assets.py
python generate_backgrounds.py
```

## Running the Game

Start the game from the main entry point:

```bash
cd src
python main.py
```

The game will launch with Level 1 and can be progressed through by completing levels, defeating enemies, and collecting treasure.

## Game Controls

- **Movement**: Arrow keys or A/D keys
- **Jump**: Spacebar
- **Attack**: Left mouse button or designated attack key
- **Interact**: Enter doors to progress between levels

## Level Design

The game features 4 levels with increasing difficulty:

1. **Level 1**: Introduction to mechanics, basic enemies and obstacles
2. **Level 2**: More complex layouts, tougher enemies
3. **Level 3**: Advanced obstacle combinations, challenging enemy patterns
4. **Boss Level**: Final confrontation with the boss enemy

Each level is procedurally laid out with variations to increase replayability.

## Gameplay Mechanics

### Combat System
- Players attack with a sword, dealing damage to enemies within the attack hitbox
- Enemies have health and die when health reaches zero
- Both player and enemies have health bars displayed above them
- Attack animations provide visual feedback

### Platforming
- Navigate across platforms with proper jump timing
- Obstacles deal damage on contact or block movement
- Various obstacle types have unique effects:
  - Spike traps: instant damage
  - Fire: damage over time effect
  - Slippery surfaces: reduced traction
  - Slow traps: movement speed reduction
  - Bouncy platforms: enhanced jump height
  - Healing plants: restore health

### Progression
- Players must defeat enemies and collect treasure
- Doors serve as level checkpoints and progression gates
- Treasure collection tracked through sticker system (max 10)
- Reaching the boss stage completes regular level progression

## Asset System

The game includes a dynamic asset loader (`asset_loader.py`) that:
- Loads sprites from the `assets/` directory
- Supports animation frame sequences
- Provides fallback colored shapes if sprites are missing
- Enables easy expansion with new asset types

Sprite types currently supported:
- Player animations
- Sword attack animations (left and right)
- Enemy sprites (forest creatures)
- Obstacle sprites (various trap types)
- Background tilesets

## Testing

The project includes comprehensive test suites:

- `test_game_run.py`: Tests basic game execution and initialization
- `test_boss_bear.py`: Tests boss AI and combat mechanics
- `test_comprehensive_bear.py`: Full gameplay scenario testing
- `test_visual_boss_bear.py`: Visual rendering and animation tests
- `test_script.py`: General functionality and utility tests

Run tests with:
```bash
python test_game_run.py
python test_comprehensive_bear.py
```

## Audio

The game includes music support with:
- Victory music that plays when levels are completed
- Dynamic music loading from the `assets/` directory
- Audio initialization through Pygame mixer

## Performance Considerations

- **Collision Detection**: Optimized with spatial organization
- **Camera System**: Smooth scrolling with configurable deadzone and tracking
- **Sprite Management**: Efficient sprite group handling with culling
- **Enemy Limits**: Maximum 2 enemies attacking simultaneously to balance performance

## Future Enhancements

Potential features for future development:
- Additional animal enemy types (currently placeholder names)
- More visual art assets and animations
- Sound effects for attacks, damage, and pickups
- Difficulty settings and leaderboards
- Additional power-up types
- Procedural level generation algorithms
- Multiplayer or co-op modes

## Technologies Used

- **Engine**: Pygame 2.x
- **Language**: Python 3.7+
- **Art Tools**: Aseprite, GIMP
- **Level Design**: Custom Python-based generation
- **Version Control**: Git/GitHub

## Development Timeline

The project was developed in 3 phases over approximately 3 weeks:

1. **Phase 1**: Core mechanics (movement, jumping, attacks)
2. **Phase 2**: Enemies and obstacles
3. **Phase 3**: Levels, progression, and boss mechanics

## Project Proposal

For detailed project specifications, requirements, and initial design documentation, see [video_game_proposal.txt](video_game_proposal.txt).

## License

This project is part of the Spring 2025 Final Project for Group A.

## Author

Group A 

---

**Status**: Done

For issues, feature requests, or contributions, please refer to the project's GitHub repository.
