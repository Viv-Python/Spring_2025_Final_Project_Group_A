import pygame
from settings import CYAN, WIDTH, HEIGHT, GREEN

class Door(pygame.sprite.Sprite):
    """Door that unlocks when all enemies are defeated"""
    def __init__(self, x, y, width=50, height=80):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((50, 50, 50))  # Dark gray when locked
        self.rect = self.image.get_rect(topleft=(x, y))
        self.unlocked = False
        self._draw_locked_state()

    def _draw_locked_state(self):
        """Draw the door in locked state"""
        self.image.fill((50, 50, 50))
        # Draw door frame
        pygame.draw.rect(self.image, (100, 100, 100), (2, 2, self.width - 4, self.height - 4), 3)
        # Draw lock indicator
        pygame.draw.circle(self.image, (255, 0, 0), (self.width // 2, self.height // 2), 8, 2)

    def _draw_unlocked_state(self):
        """Draw the door in unlocked state"""
        self.image.fill(CYAN)
        # Draw door frame
        pygame.draw.rect(self.image, (0, 150, 150), (2, 2, self.width - 4, self.height - 4), 3)
        # Draw unlock indicator (open door symbol)
        pygame.draw.polygon(self.image, (0, 0, 0), [
            (self.width // 4, self.height // 4),
            (3 * self.width // 4, self.height // 4),
            (3 * self.width // 4, 3 * self.height // 4),
            (self.width // 4, 3 * self.height // 4)
        ])
        # Draw arrow pointing up
        pygame.draw.polygon(self.image, (255, 255, 0), [
            (self.width // 2, self.height // 6),
            (self.width // 3, self.height // 3),
            (2 * self.width // 3, self.height // 3)
        ])

    def unlock(self):
        """Unlock the door when all enemies are defeated"""
        self.unlocked = True
        self._draw_unlocked_state()

    def is_player_exiting(self, player_rect):
        """Check if player has collided with and exited through the door"""
        return self.unlocked and self.rect.colliderect(player_rect)

    def draw_locked_effect(self, surface):
        """Draw a locked indicator if not unlocked"""
        if not self.unlocked:
            # Draw lock symbol
            lock_color = (255, 0, 0)
            pygame.draw.circle(surface, lock_color, self.rect.center, 8, 2)
