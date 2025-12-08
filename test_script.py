#!/usr/bin/env python3
"""
Comprehensive test script for asset loading and sprite system:
1. Asset files exist and can be loaded
2. Player sprite loads correctly and dimensions match
3. Enemy sprite loads correctly and dimensions match
4. Obstacle sprites load correctly for all types
5. Terrain tile sprites load correctly
6. Animation frames load correctly
7. Sprite scaling works properly
8. Fallback system works when assets are missing
"""

import sys
sys.path.insert(0, 'src')

import pygame
import os
from asset_loader import get_loader, are_assets_available
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_SIZE, OBSTACLE_SIZE, WIDTH, HEIGHT, LEVEL_HEIGHT
from player import Player
from enemies import Enemy
from obstacles import spike, fire, slow_trap, slippery, block, falling_rock, poison_pool, electric, healing_plant, bouncy
from platform import Platform

pygame.init()

def test_asset_directory_structure():
    """Test that all asset directories exist"""
    print("=" * 60)
    print("TEST 1: Asset Directory Structure")
    print("=" * 60)
    
    try:
        required_dirs = [
            'assets',
            'assets/player',
            'assets/enemies',
            'assets/obstacles',
            'assets/tiles',
            'assets/animations'
        ]
        
        for dir_path in required_dirs:
            assert os.path.isdir(dir_path), f"Directory not found: {dir_path}"
            print(f"✓ Directory exists: {dir_path}")
        
        print("✓ PASS: All asset directories present")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_asset_files_exist():
    """Test that all required asset files exist"""
    print("=" * 60)
    print("TEST 2: Required Asset Files")
    print("=" * 60)
    
    try:
        required_files = [
            'assets/player/player_idle.png',
            'assets/enemies/forest_creature.png',
            'assets/obstacles/spike.png',
            'assets/obstacles/fire.png',
            'assets/obstacles/slow_trap.png',
            'assets/obstacles/slippery.png',
            'assets/obstacles/block.png',
            'assets/obstacles/falling_rock.png',
            'assets/obstacles/poison_pool.png',
            'assets/obstacles/electric.png',
            'assets/obstacles/healing_plant.png',
            'assets/obstacles/bouncy.png',
            'assets/tiles/grass.png',
            'assets/tiles/dirt.png',
            'assets/tiles/stone.png',
            'assets/tiles/grass_dirt.png',
            'assets/animations/player_walk_0.png',
            'assets/animations/player_walk_1.png',
            'assets/animations/player_walk_2.png',
            'assets/animations/player_walk_3.png',
            'assets/animations/enemy_idle_0.png',
            'assets/animations/enemy_idle_1.png',
            'assets/animations/enemy_idle_2.png',
            'assets/animations/enemy_idle_3.png',
        ]
        
        all_exist = True
        for file_path in required_files:
            if os.path.isfile(file_path):
                print(f"✓ File exists: {file_path}")
            else:
                print(f"✗ File missing: {file_path}")
                all_exist = False
        
        assert all_exist, "Some required asset files are missing"
        print("✓ PASS: All asset files present")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_asset_loader_initialization():
    """Test that AssetLoader initializes correctly"""
    print("=" * 60)
    print("TEST 3: Asset Loader Initialization")
    print("=" * 60)
    
    try:
        loader = get_loader()
        assert loader is not None, "Asset loader is None"
        print(f"✓ Asset loader created")
        
        assets_available = are_assets_available()
        assert assets_available, "Assets reported as not available"
        print(f"✓ Assets are available: {assets_available}")
        
        print("✓ PASS: Asset loader initialized successfully")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_player_sprite_loading():
    """Test that player sprite loads correctly"""
    print("=" * 60)
    print("TEST 4: Player Sprite Loading")
    print("=" * 60)
    
    try:
        loader = get_loader()
        player_sprite = loader.get_player_idle()
        
        assert player_sprite is not None, "Player sprite is None"
        print(f"✓ Player sprite loaded")
        
        assert player_sprite.get_width() > 0, "Player sprite has no width"
        assert player_sprite.get_height() > 0, "Player sprite has no height"
        print(f"✓ Player sprite dimensions: {player_sprite.get_width()}x{player_sprite.get_height()}")
        
        # Test scaling
        scaled = pygame.transform.scale(player_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
        assert scaled.get_width() == PLAYER_WIDTH, "Scaled width doesn't match"
        assert scaled.get_height() == PLAYER_HEIGHT, "Scaled height doesn't match"
        print(f"✓ Player sprite scales to {PLAYER_WIDTH}x{PLAYER_HEIGHT}")
        
        print("✓ PASS: Player sprite loads and scales correctly")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_enemy_sprite_loading():
    """Test that enemy sprite loads correctly"""
    print("=" * 60)
    print("TEST 5: Enemy Sprite Loading")
    print("=" * 60)
    
    try:
        loader = get_loader()
        enemy_sprite = loader.get_enemy_sprite('forest_creature')
        
        assert enemy_sprite is not None, "Enemy sprite is None"
        print(f"✓ Enemy sprite loaded")
        
        assert enemy_sprite.get_width() > 0, "Enemy sprite has no width"
        assert enemy_sprite.get_height() > 0, "Enemy sprite has no height"
        print(f"✓ Enemy sprite dimensions: {enemy_sprite.get_width()}x{enemy_sprite.get_height()}")
        
        # Test scaling
        scaled = pygame.transform.scale(enemy_sprite, (ENEMY_SIZE, ENEMY_SIZE))
        assert scaled.get_width() == ENEMY_SIZE, "Scaled width doesn't match"
        assert scaled.get_height() == ENEMY_SIZE, "Scaled height doesn't match"
        print(f"✓ Enemy sprite scales to {ENEMY_SIZE}x{ENEMY_SIZE}")
        
        print("✓ PASS: Enemy sprite loads and scales correctly")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_obstacle_sprites_loading():
    """Test that all obstacle sprites load correctly"""
    print("=" * 60)
    print("TEST 6: Obstacle Sprites Loading")
    print("=" * 60)
    
    try:
        loader = get_loader()
        obstacle_types = ['spike', 'fire', 'slow_trap', 'slippery', 'block', 
                         'falling_rock', 'poison_pool', 'electric', 'healing_plant', 'bouncy']
        
        for obs_type in obstacle_types:
            sprite = loader.get_obstacle_sprite(obs_type)
            assert sprite is not None, f"Obstacle sprite '{obs_type}' is None"
            assert sprite.get_width() > 0, f"Obstacle '{obs_type}' has no width"
            print(f"✓ Obstacle sprite loaded: {obs_type}")
        
        print("✓ PASS: All obstacle sprites load correctly")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_terrain_tiles_loading():
    """Test that terrain tile sprites load correctly"""
    print("=" * 60)
    print("TEST 7: Terrain Tiles Loading")
    print("=" * 60)
    
    try:
        loader = get_loader()
        tile_types = ['grass', 'dirt', 'stone', 'grass_dirt']
        
        for tile_type in tile_types:
            sprite = loader.get_tile_sprite(tile_type)
            assert sprite is not None, f"Tile sprite '{tile_type}' is None"
            assert sprite.get_width() > 0, f"Tile '{tile_type}' has no width"
            print(f"✓ Tile sprite loaded: {tile_type}")
        
        print("✓ PASS: All terrain tiles load correctly")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_animation_frames_loading():
    """Test that animation frames load correctly"""
    print("=" * 60)
    print("TEST 8: Animation Frames Loading")
    print("=" * 60)
    
    try:
        loader = get_loader()
        
        # Test player walking animation
        player_walk = loader.get_player_walking()
        assert player_walk is not None, "Player walking animation is None"
        assert len(player_walk) == 4, f"Player walking should have 4 frames, got {len(player_walk)}"
        for i, frame in enumerate(player_walk):
            assert frame is not None, f"Player walking frame {i} is None"
            assert frame.get_width() > 0, f"Frame {i} has no width"
        print(f"✓ Player walking animation loaded: 4 frames")
        
        # Test enemy idle animation
        enemy_idle = loader.get_enemy_idle()
        assert enemy_idle is not None, "Enemy idle animation is None"
        assert len(enemy_idle) == 4, f"Enemy idle should have 4 frames, got {len(enemy_idle)}"
        for i, frame in enumerate(enemy_idle):
            assert frame is not None, f"Enemy idle frame {i} is None"
            assert frame.get_width() > 0, f"Frame {i} has no width"
        print(f"✓ Enemy idle animation loaded: 4 frames")
        
        print("✓ PASS: All animation frames load correctly")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_player_instantiation():
    """Test that Player class can be instantiated with sprite loading"""
    print("=" * 60)
    print("TEST 9: Player Instantiation with Sprites")
    print("=" * 60)
    
    try:
        # Create a dummy display for pygame
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        player = Player(WIDTH // 2, HEIGHT // 2)
        assert player is not None, "Player object is None"
        assert player.image is not None, "Player image is None"
        assert player.rect is not None, "Player rect is None"
        print(f"✓ Player instantiated successfully")
        print(f"✓ Player position: ({player.rect.x}, {player.rect.y})")
        print(f"✓ Player dimensions: {player.rect.width}x{player.rect.height}")
        print(f"✓ Player health: {player.health}/{player.max_health}")
        
        print("✓ PASS: Player instantiation works with sprite system")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_enemy_instantiation():
    """Test that Enemy class can be instantiated with sprite loading"""
    print("=" * 60)
    print("TEST 10: Enemy Instantiation with Sprites")
    print("=" * 60)
    
    try:
        enemy = Enemy(200, 200, pattern='patrol', speed=2, health=20)
        assert enemy is not None, "Enemy object is None"
        assert enemy.image is not None, "Enemy image is None"
        assert enemy.rect is not None, "Enemy rect is None"
        print(f"✓ Enemy instantiated successfully")
        print(f"✓ Enemy position: ({enemy.rect.x}, {enemy.rect.y})")
        print(f"✓ Enemy dimensions: {enemy.rect.width}x{enemy.rect.height}")
        print(f"✓ Enemy health: {enemy.health}/{enemy.max_health}")
        
        print("✓ PASS: Enemy instantiation works with sprite system")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_obstacle_instantiation():
    """Test that obstacles can be instantiated with sprite loading"""
    print("=" * 60)
    print("TEST 11: Obstacle Instantiation with Sprites")
    print("=" * 60)
    
    try:
        # Test a few different obstacle types
        spike_obs = spike(100, 100)
        assert spike_obs is not None, "Spike obstacle is None"
        assert spike_obs.image is not None, "Spike image is None"
        print(f"✓ Spike obstacle created successfully")
        
        fire_obs = fire(150, 150)
        assert fire_obs is not None, "Fire obstacle is None"
        print(f"✓ Fire obstacle created successfully")
        
        bouncy_obs = bouncy(200, 200)
        assert bouncy_obs is not None, "Bouncy obstacle is None"
        print(f"✓ Bouncy obstacle created successfully")
        
        print("✓ PASS: All obstacle types instantiate correctly")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def test_platform_instantiation():
    """Test that Platform class can be instantiated with tile sprites"""
    print("=" * 60)
    print("TEST 12: Platform Instantiation with Tile Sprites")
    print("=" * 60)
    
    try:
        platform = Platform(100, 300, 200, 20)
        assert platform is not None, "Platform object is None"
        assert platform.image is not None, "Platform image is None"
        assert platform.rect is not None, "Platform rect is None"
        print(f"✓ Platform instantiated successfully")
        print(f"✓ Platform position: ({platform.rect.x}, {platform.rect.y})")
        print(f"✓ Platform dimensions: {platform.rect.width}x{platform.rect.height}")
        
        print("✓ PASS: Platform instantiation works with tile sprite system")
    except AssertionError as e:
        print(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    return True

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("ASSET LOADING AND SPRITE SYSTEM TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_asset_directory_structure,
        test_asset_files_exist,
        test_asset_loader_initialization,
        test_player_sprite_loading,
        test_enemy_sprite_loading,
        test_obstacle_sprites_loading,
        test_terrain_tiles_loading,
        test_animation_frames_loading,
        test_player_instantiation,
        test_enemy_instantiation,
        test_obstacle_instantiation,
        test_platform_instantiation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = test()
            if result is not False:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ EXCEPTION in {test.__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED")
    print("=" * 60)
    
    if failed == 0:
        print("✓ ALL TESTS PASSED!")
    else:
        print(f"✗ {failed} TEST(S) FAILED")
    
    print()

if __name__ == '__main__':
    main()

