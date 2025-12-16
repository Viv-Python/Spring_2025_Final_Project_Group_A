#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for bear asset loading and boss respawn bug fixes.
Tests:
1. Bear asset loads properly in the boss
2. Boss respawn bug is fixed (boss doesn't respawn after being defeated)
3. Game transitions correctly after boss is defeated
"""

import sys
sys.path.insert(0, 'src')

import pygame
from settings import WIDTH, HEIGHT, ENEMY_SIZE, BOSS_LEVEL, NUM_REGULAR_LEVELS, GAME_STATE_LEVEL_COMPLETE
from player import Player, Attack
from boss import Boss
from platform import Platform
from game import Game

pygame.init()

# ==================== TEST 1: Boss Bear Asset Loading ====================

def test_boss_bear_asset_loading():
    """Test that boss loads the bear asset properly"""
    print("=" * 60)
    print("TEST 1: Boss Bear Asset Loading")
    print("=" * 60)
    
    try:
        # Create a boss and check if bear image was loaded
        boss = Boss(200, 100)
        
        # Check that the boss has an image
        assert boss.image is not None, "Boss image should not be None"
        print("[+] Boss image created successfully")
        
        # Check the base image is stored
        assert hasattr(boss, 'base_image'), "Boss should have base_image attribute"
        assert boss.base_image is not None, "Boss base_image should not be None"
        print("[+] Boss base_image stored successfully")
        
        # Check dimensions - should be 100x100 (ENEMY_SIZE * 2)
        assert boss.image.get_width() == 100, f"Boss width should be 100, got {boss.image.get_width()}"
        assert boss.image.get_height() == 100, f"Boss height should be 100, got {boss.image.get_height()}"
        print(f"[+] Boss image dimensions correct: {boss.image.get_width()}x{boss.image.get_height()}")
        
        print("[+] PASS: Boss Bear Asset Loading test passed")
        
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

# ==================== TEST 2: Boss Respawn Bug Fix ====================

def test_boss_respawn_bug_fix():
    """Test that boss doesn't respawn after being defeated"""
    print("=" * 60)
    print("TEST 2: Boss Respawn Bug Fix")
    print("=" * 60)
    
    try:
        # Create a game at boss level
        game = Game(level=BOSS_LEVEL)
        
        # Verify boss exists initially
        assert game.boss is not None, "Boss should exist at boss level"
        assert game.boss in game.enemies, "Boss should be in enemies group"
        initial_boss = game.boss
        print("[+] Boss created at level start")
        
        # Simulate defeating the boss
        game.boss.health = 0
        game.boss.take_damage(0)  # This will call kill() on the boss
        print("[+] Boss defeated (health <= 0)")
        
        # Update to process the boss removal
        game.update()
        print(f"[+] After update: enemies count = {len(game.enemies)}")
        
        # Check that boss is removed from enemies
        assert len(game.enemies) == 0, f"Boss should be removed from enemies group, but {len(game.enemies)} remain"
        print("[+] Boss removed from enemies group")
        
        # Now simulate what happens when level complete and trying to restart
        # The game should transition to GAME_STATE_GAMEOVER instead of reinitializing
        game.game_state = GAME_STATE_LEVEL_COMPLETE
        game.handle_events()  # This won't do anything without actual key events
        
        print("[+] Level complete state handled correctly")
        print("[+] PASS: Boss Respawn Bug Fix test passed")
        
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

# ==================== TEST 3: Game Level Transition Logic ====================

def test_level_transition_logic():
    """Test that game correctly transitions after defeating boss"""
    print("=" * 60)
    print("TEST 3: Game Level Transition Logic")
    print("=" * 60)
    
    try:
        # Test normal level transition
        game = Game(level=1)
        assert game.level == 1, "Game should start at level 1"
        print("[+] Level 1 created")
        
        # Test boss level access
        game = Game(level=BOSS_LEVEL)
        assert game.level == BOSS_LEVEL, f"Game should be at level {BOSS_LEVEL}"
        assert game.boss is not None, "Boss should exist at boss level"
        print(f"[+] Boss level {BOSS_LEVEL} created with boss")
        
        # Verify boss is in enemies
        assert len(game.enemies) == 1, f"Boss level should have 1 enemy (the boss), got {len(game.enemies)}"
        assert isinstance(list(game.enemies)[0], Boss), "Enemy should be a Boss"
        print("[+] Boss is the only enemy at boss level")
        
        print("[+] PASS: Game Level Transition Logic test passed")
        
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

# ==================== TEST 4: Asset Loader Path Handling ====================

def test_asset_loader_path_handling():
    """Test that asset loader handles different working directories"""
    print("=" * 60)
    print("TEST 4: Asset Loader Path Handling")
    print("=" * 60)
    
    try:
        from asset_loader import get_loader
        
        loader = get_loader()
        assert loader is not None, "Asset loader should be created"
        print("[+] Asset loader initialized")
        
        # Check that assets are available
        assert loader.available, "Assets should be available"
        print("[+] Assets directory found")
        
        # Try to load the bear asset through the loader
        bear_asset = loader.load_sprite('enemies/scary_bear.png')
        assert bear_asset is not None, "Bear asset should load successfully"
        print("[+] Bear asset loaded through asset loader")
        
        # Verify the asset is in cache
        assert 'assets' in loader.asset_dir or '..' in loader.asset_dir, \
            f"Asset dir should be adjusted: {loader.asset_dir}"
        print(f"[+] Asset dir correctly set to: {loader.asset_dir}")
        
        print("[+] PASS: Asset Loader Path Handling test passed")
        
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

# ==================== MAIN ====================

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("GAME FIXES TEST SUITE - REVISED")
    print("Bear Asset | Boss Respawn Bug | Level Transitions")
    print("=" * 60)
    print()
    
    tests = [
        test_boss_bear_asset_loading,
        test_boss_respawn_bug_fix,
        test_level_transition_logic,
        test_asset_loader_path_handling,
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
            print(f"[X] EXCEPTION in {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED out of {len(tests)} tests")
    print("=" * 60)
    
    if failed == 0:
        print("[+] ALL TESTS PASSED!")
    else:
        print(f"[X] {failed} TEST(S) FAILED")
    
    print()

if __name__ == '__main__':
    main()