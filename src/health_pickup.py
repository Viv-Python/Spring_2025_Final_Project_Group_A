import pygame
from settings import GREEN, WIDTH, HEIGHT

class HealthPickup(pygame.sprite.Sprite):
    """Collectible health pickup that restores player health"""
    def __init__(self, x, y, heal_amount=20):
        super().__init__()
        self.heal_amount = heal_amount
        self.size = 15
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((0, 255, 0))
        # Draw a plus sign
        center = self.size // 2
        pygame.draw.line(self.image, (0, 0, 0), (center, 2), (center, self.size - 2), 2)
        pygame.draw.line(self.image, (0, 0, 0), (2, center), (self.size - 2, center), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.collected = False
        self.bob_offset = 0
        self.bob_speed = 0.1

    def collect(self):
        """Mark pickup as collected and remove from game"""
        self.collected = True
        self.kill()

    def update(self, *args):
        """Gentle bobbing animation"""
        self.bob_offset += self.bob_speed
        import math
        self.rect.y += math.sin(self.bob_offset) * 0.5
