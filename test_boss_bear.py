#!/usr/bin/env python3
"""
Test script to verify the boss bear sprite loads and displays correctly.
"""

import sys
sys.path.insert(0, 'src')

import pygame
from game import Game
from settings import BOSS_LEVEL

def test_boss_bear():
    """Test boss bear sprite loading and display"""
    print("\n" + "=" * 60)
    print("BOSS BEAR SPRITE TEST")
    print("=" * 60)
    print("\nInitializing boss level...")
    
    try:
        # Create game at boss level
        game = Game(level=BOSS_LEVEL, seed=42)
        
        print(f"Game initialized at level {BOSS_LEVEL}")
        
        # Check if boss was created
        if game.boss:
            print(f"[+] Boss created: {game.boss}")
            print(f"[+] Boss position: ({game.boss.rect.x}, {game.boss.rect.y})")
            print(f"[+] Boss image size: {game.boss.image.get_size()}")
            print(f"[+] Boss rect size: ({game.boss.rect.width}, {game.boss.rect.height})")
            
            # Check if bear asset was loaded
            if hasattr(game.boss, 'base_image'):
                print(f"[+] Base image size: {game.boss.base_image.get_size()}")
        else:
            print("[-] Boss not created!")
            return False
        
        # Run game for 60 frames to test
        print("\nRunning boss level for 60 frames...")
        frame_count = 0
        max_frames = 60
        clock = pygame.time.Clock()
        
        running = True
        while running and frame_count < max_frames:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if frame_count % 20 == 0:
                print(f"Frame {frame_count}: Boss at ({game.boss.rect.x}, {game.boss.rect.y}), health={game.boss.health}")
            
            # Update game
            game.update()
            game.draw_game()
            pygame.display.flip()
            
            frame_count += 1
            clock.tick(60)
        
        print(f"\n[+] Boss bear test completed! Final health: {game.boss.health}")
        print(f"[+] Boss image final size: {game.boss.image.get_size()}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[-] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_boss_bear()
    print("\n" + "=" * 60)
    if success:
        print("[+] BOSS BEAR TEST PASSED!")
    else:
        print("[-] BOSS BEAR TEST FAILED!")
    print("=" * 60 + "\n")
    sys.exit(0 if success else 1)
