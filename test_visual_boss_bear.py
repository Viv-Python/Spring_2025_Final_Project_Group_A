#!/usr/bin/env python3
"""
Visual test to display the boss bear sprite on screen for inspection.
Run this to see the scary_bear.png rendered as the boss in the game.
"""

import sys
sys.path.insert(0, 'src')

import pygame
from game import Game
from settings import BOSS_LEVEL, WIDTH, HEIGHT

def visual_test_boss_bear():
    """Visually test boss bear sprite - displays for 8 seconds (480 frames)"""
    print("\n" + "=" * 60)
    print("BOSS BEAR VISUAL TEST")
    print("=" * 60)
    print("\nInitializing boss level for visual inspection...")
    print("A window should appear showing the boss bear sprite.")
    print("The bear will move around the screen for 8 seconds.\n")
    
    try:
        # Create game at boss level
        game = Game(level=BOSS_LEVEL, seed=42)
        
        if game.boss:
            print(f"[+] Boss created with scary_bear.png")
            print(f"[+] Boss image size: {game.boss.image.get_size()}")
            print(f"[+] Boss initial position: ({game.boss.rect.x}, {game.boss.rect.y})\n")
        
        # Run for 8 seconds (480 frames at 60 FPS)
        print("Running visual test... (watch the window for the bear sprite)")
        frame_count = 0
        max_frames = 480
        clock = pygame.time.Clock()
        
        running = True
        while running and frame_count < max_frames:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Every second, print progress
            if frame_count % 60 == 0:
                seconds = frame_count // 60
                health_bar = "█" * int(game.boss.health / 150 * 20) + "░" * (20 - int(game.boss.health / 150 * 20))
                print(f"  [{seconds}s] Health: [{health_bar}] Position: ({game.boss.rect.x}, {game.boss.rect.y}), Phase: {game.boss.phase}")
            
            # Update and draw
            game.update()
            game.draw_game()
            pygame.display.flip()
            
            frame_count += 1
            clock.tick(60)
        
        print(f"\n[+] Visual test completed!")
        print(f"[+] Final boss health: {game.boss.health}")
        print(f"[+] Final image size: {game.boss.image.get_size()}")
        print(f"[+] Final position: ({game.boss.rect.x}, {game.boss.rect.y})")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[-] Error during visual test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = visual_test_boss_bear()
    print("\n" + "=" * 60)
    if success:
        print("[+] VISUAL TEST COMPLETED SUCCESSFULLY!")
        print("\nThe scary_bear.png sprite should have been visible")
        print("as the boss enemy on screen during the test.")
    else:
        print("[-] VISUAL TEST FAILED!")
    print("=" * 60 + "\n")
    sys.exit(0 if success else 1)
