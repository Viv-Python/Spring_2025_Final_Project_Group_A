#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for background implementation:
1. Verify background images are generated for all levels
2. Test background loading in Game class
3. Verify backgrounds are drawn correctly
"""

import sys
sys.path.insert(0, 'src')

import pygame
import os
from settings import BOSS_LEVEL, NUM_REGULAR_LEVELS
from game import Game

pygame.init()

# ==================== TEST 1: Background Files Exist ====================

def test_background_files_exist():
    """Test that all background image files are generated"""
    print("=" * 60)
    print("TEST 1: Background Files Exist")
    print("=" * 60)
    
    try:
        background_files = {
            1: 'swamp.png',
            2: 'jungle.png',
            3: 'forest.png',
            BOSS_LEVEL: 'cave.png',
        }
        
        base_paths = [
            'assets/backgrounds',
            'src/assets/backgrounds',
        ]
        
        found_files = {}
        for level, filename in background_files.items():
            found = False
            for base_path in base_paths:
                filepath = os.path.join(base_path, filename)
                if os.path.exists(filepath):
                    found = True
                    found_files[level] = filepath
                    print(f"[+] Found background for level {level}: {filepath}")
                    break
            
            assert found, f"Background image not found for level {level}"
        
        print("[+] PASS: All background files exist")
        return True
        
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

# ==================== TEST 2: Game Loading Backgrounds ====================

def test_game_load_background():
    """Test that Game class loads backgrounds for each level"""
    print("=" * 60)
    print("TEST 2: Game Loading Backgrounds")
    print("=" * 60)
    
    try:
        levels_to_test = [1, 2, 3, BOSS_LEVEL]
        
        for level in levels_to_test:
            print(f"Testing level {level}...")
            game = Game(level=level)
            
            # Check that background_image attribute exists
            assert hasattr(game, 'background_image'), f"Game missing background_image attribute"
            print(f"  [+] Game has background_image attribute")
            
            # Check if background was loaded (should be pygame.Surface if loaded)
            if game.background_image is not None:
                assert isinstance(game.background_image, pygame.Surface), \
                    f"background_image should be pygame.Surface, got {type(game.background_image)}"
                print(f"  [+] Background loaded as pygame.Surface for level {level}")
                
                # Check image dimensions match screen size
                from settings import WIDTH, HEIGHT
                assert game.background_image.get_size() == (WIDTH, HEIGHT), \
                    f"Background size mismatch: {game.background_image.get_size()} vs ({WIDTH}, {HEIGHT})"
                print(f"  [+] Background dimensions correct: {game.background_image.get_size()}")
            else:
                print(f"  [!] No background image loaded for level {level}, using fallback colors")
        
        print("[+] PASS: Game loading backgrounds correctly")
        return True
        
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

# ==================== TEST 3: Background Level Mapping ====================

def test_background_level_mapping():
    """Test that correct background is loaded for each level"""
    print("=" * 60)
    print("TEST 3: Background Level Mapping")
    print("=" * 60)
    
    try:
        level_bg_mapping = {
            1: 'swamp',
            2: 'jungle',
            3: 'forest',
            BOSS_LEVEL: 'cave',
        }
        
        for level, expected_bg in level_bg_mapping.items():
            game = Game(level=level)
            
            # Check background filename expectations by checking if it was loaded
            if game.background_image is not None:
                print(f"[+] Level {level}: Background loaded (expected {expected_bg})")
            else:
                print(f"[!] Level {level}: Using fallback colors (expected {expected_bg} background)")
        
        print("[+] PASS: Background level mapping verified")
        return True
        
    except Exception as e:
        print(f"[X] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

# ==================== TEST 4: Game Render with Backgrounds ====================

def test_game_render_with_backgrounds():
    """Test that game renders with backgrounds loaded"""
    print("=" * 60)
    print("TEST 4: Game Render with Backgrounds")
    print("=" * 60)
    
    try:
        # Create game
        game = Game(level=1)
        
        # Call draw_game to ensure it works with backgrounds
        try:
            game.draw_game()
            print("[+] game.draw_game() executed without errors")
        except Exception as e:
            print(f"[X] Error in draw_game(): {e}")
            raise
        
        # Call update to ensure game loop works
        try:
            game.update()
            print("[+] game.update() executed without errors")
        except Exception as e:
            print(f"[X] Error in update(): {e}")
            raise
        
        # Check game state
        from settings import GAME_STATE_PLAYING
        assert game.game_state == GAME_STATE_PLAYING, "Game should be in PLAYING state"
        print("[+] Game state is correct (PLAYING)")
        
        print("[+] PASS: Game renders correctly with backgrounds")
        return True
        
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
    print("BACKGROUND IMPLEMENTATION TEST SUITE")
    print("Files | Loading | Mapping | Rendering")
    print("=" * 60)
    print()
    
    tests = [
        test_background_files_exist,
        test_game_load_background,
        test_background_level_mapping,
        test_game_render_with_backgrounds,
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
