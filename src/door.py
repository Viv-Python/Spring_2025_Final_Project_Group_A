import pygame
from settings import CYAN, WIDTH, HEIGHT

class Door(pygame.sprite.Sprite):
    """Door that unlocks when all enemies are defeated"""
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.unlocked = False

    def unlock(self):
        """Unlock the door when all enemies are defeated"""
        self.unlocked = True
        self.image.fill(CYAN)
        # Draw a simple unlock indicator without text rendering
        pygame.draw.polygon(self.image, (0, 0, 0), [
            (10, 15), (30, 15), (30, 35), (10, 35)
        ])

    def is_player_exiting(self, player_rect):
        """Check if player has collided with and exited through the door"""
        return self.unlocked and self.rect.colliderect(player_rect)

    def draw_locked_effect(self, surface):
        """Draw a locked indicator if not unlocked"""
        if not self.unlocked:
            # Draw lock symbol
            lock_color = (255, 0, 0)
            pygame.draw.circle(surface, lock_color, self.rect.center, 8, 2)
