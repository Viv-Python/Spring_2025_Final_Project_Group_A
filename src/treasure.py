import pygame
import random
from settings import YELLOW, ORANGE, WIDTH, HEIGHT

class Treasure(pygame.sprite.Sprite):
    """Collectible treasure that grants stickers"""
    def __init__(self, x, y, sticker_id=None, hidden_initially=True):
        super().__init__()
        self.size = 25
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(YELLOW)
        # Draw a star-like pattern
        pygame.draw.polygon(self.image, ORANGE, [
            (12, 0), (15, 10), (25, 12), (15, 15), (12, 25),
            (9, 15), (0, 12), (9, 10)
        ])
        self.rect = self.image.get_rect(center=(x, y))
        self.sticker_id = sticker_id if sticker_id is not None else random.randint(0, 9)
        self.collected = False
        self.hidden = hidden_initially
        self._base_image = self.image.copy()
        if self.hidden:
            self.hide()

    def hide(self):
        """Hide the treasure until enemies are defeated"""
        self.hidden = True
        # Make it invisible by filling with transparency
        self.image = pygame.Surface((self.size, self.size))
        self.image.set_alpha(0)

    def reveal(self):
        """Reveal the treasure after enemies are defeated"""
        self.hidden = False
        self.image = self._base_image.copy()

    def collect(self):
        """Mark treasure as collected and remove from game"""
        self.collected = True
        self.kill()

    def update(self, *args):
        """Gentle bobbing animation"""
        if not self.hidden:
            import math
            # This would normally animate the bobbing, but position is fixed in this implementation
            pass
