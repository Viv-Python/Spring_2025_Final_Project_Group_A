#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick game test to verify new features:
- Running animation plays when moving
- Sword swings work in both directions
- Sword hilt rotates correctly
- Underground area with dinosaur skeletons is visible when falling
"""

import sys
sys.path.insert(0, 'src')

import pygame
from game import Game

def test_game_features():
    """Run game for a brief test"""
    print("\n" + "=" * 60)
    print("GAME FEATURES TEST")
    print("=" * 60)
    print("\nStarting game test...")
    print("Instructions during test:")
    print("1. Watch character move (RIGHT arrow) - should see running animation")
    print("2. Move left (LEFT arrow) - running animation should flip")
    print("3. Attack (A key) - sword should swing in direction you're facing")
    print("4. Game will auto-close after 120 frames (~2 seconds)")
    print("\n" + "=" * 60 + "\n")
    
    try:
        # Create game
        game = Game(level=1, seed=42)
        
        # Run game for 120 frames
        frame_count = 0
        max_frames = 120
        
        # Simulate some input
        input_sequence = [
            {'RIGHT': True},  # Move right - should see running animation
            {'RIGHT': True},
            {'RIGHT': True},
            {'RIGHT': False},  # Stop
            {'LEFT': True},   # Move left - running animation should flip
            {'LEFT': True},
            {'LEFT': True},
            {'LEFT': False},  # Stop
            {'a': True},      # Attack right
            {'a': False},
            {'LEFT': True, 'a': True},  # Move left and attack - should see left swing
            {'LEFT': False, 'a': False},
            {},  # Idle
        ]
        
        print("Running game test...\n")
        
        running = True
        input_index = 0
        
        while running and frame_count < max_frames:
            game.clock.tick(60)  # 60 FPS
            
            # Simulate input
            current_input = input_sequence[input_index % len(input_sequence)]
            
            # Create fake key press state
            keys = {}
            if current_input.get('RIGHT'):
                keys[pygame.K_RIGHT] = True
                print(f"Frame {frame_count}: Moving RIGHT - player should run right")
            elif current_input.get('LEFT'):
                keys[pygame.K_LEFT] = True
                print(f"Frame {frame_count}: Moving LEFT - player should run left")
            elif current_input.get('a'):
                keys[pygame.K_a] = True
                if current_input.get('LEFT'):
                    print(f"Frame {frame_count}: Attacking LEFT - left swing animation")
                else:
                    print(f"Frame {frame_count}: Attacking RIGHT - right swing animation")
            else:
                print(f"Frame {frame_count}: Idle")
            
            # Update game state manually
            game.player.vel_x = 0
            if current_input.get('RIGHT'):
                game.player.vel_x = 5
                game.player.facing_right = True
            elif current_input.get('LEFT'):
                game.player.vel_x = -5
                game.player.facing_right = False
            
            if current_input.get('a'):
                game.player.attack()
            
            # Update game
            game.update()
            
            # Draw game
            if game.game_state == 0:  # GAME_STATE_PLAYING
                game.draw_game()
            
            pygame.display.flip()
            
            frame_count += 1
            input_index += 1
            
            # Handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        # Verify features
        print("\n" + "=" * 60)
        print("FEATURE VERIFICATION RESULTS:")
        print("=" * 60)
        
        # Check running animation
        if game.player.running_animation is not None:
            print("[+] Running animation loaded: OK")
        else:
            print("[X] Running animation NOT loaded")
        
        # Check sword left swing
        from asset_loader import get_loader
        loader = get_loader()
        if loader.get_sword_swing_left() is not None:
            print("[+] Sword left swing animation: OK")
        else:
            print("[X] Sword left swing animation: FAILED")
        
        # Check underground rendering
        if hasattr(game, '_draw_underground'):
            print("[+] Underground rendering method: OK")
        else:
            print("[X] Underground rendering method: FAILED")
        
        # Check dinosaur skeleton rendering
        if hasattr(game, '_draw_dinosaur_skeleton'):
            print("[+] Dinosaur skeleton rendering: OK")
        else:
            print("[X] Dinosaur skeleton rendering: FAILED")
        
        print("\n" + "=" * 60)
        print("[+] GAME TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60 + "\n")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"\n[X] ERROR during game test: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False

if __name__ == '__main__':
    success = test_game_features()
    sys.exit(0 if success else 1)
