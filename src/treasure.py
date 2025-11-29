import pygame
import random
from settings import YELLOW, ORANGE, WIDTH, HEIGHT

class Treasure(pygame.sprite.Sprite):
    """Collectible treasure that grants stickers"""
    def __init__(self, x, y, sticker_id=None):
        super().__init__()
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(YELLOW)
        # Draw a star-like pattern
        pygame.draw.polygon(self.image, ORANGE, [
            (10, 0), (12, 8), (20, 10), (12, 12), (10, 20),
            (8, 12), (0, 10), (8, 8)
        ])
        self.rect = self.image.get_rect(center=(x, y))
        self.sticker_id = sticker_id if sticker_id is not None else random.randint(0, 9)
        self.collected = False

    def collect(self):
        """Mark treasure as collected and remove from game"""
        self.collected = True
        self.kill()

    def update(self, *args):
        # Gentle bobbing animation
        pass
