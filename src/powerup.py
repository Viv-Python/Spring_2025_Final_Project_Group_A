import pygame
from settings import ORANGE, RED, PURPLE, WIDTH, HEIGHT

class PowerUp(pygame.sprite.Sprite):
    """Base class for power-ups"""
    def __init__(self, x, y, duration=300):
        super().__init__()
        self.x = x
        self.y = y
        self.duration = duration  # frames
        self.duration_remaining = duration
        self.size = 20
        self.collected = False
        self.bob_offset = 0
        self.bob_speed = 0.1
    
    def collect(self):
        """Mark power-up as collected and remove from game"""
        self.collected = True
        self.kill()
    
    def update(self, *args):
        """Gentle bobbing animation"""
        self.bob_offset += self.bob_speed
        import math
        self.rect.y += math.sin(self.bob_offset) * 0.5


class ArmorPowerUp(PowerUp):
    """Reduces incoming damage by 50%"""
    def __init__(self, x, y, duration=300):
        super().__init__(x, y, duration)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((150, 150, 150))  # Gray
        # Draw a shield pattern
        pygame.draw.polygon(self.image, (100, 100, 100), [
            (10, 2), (18, 2), (18, 18), (10, 18)
        ])
        pygame.draw.line(self.image, (200, 200, 200), (10, 8), (18, 8), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.powerup_type = "armor"
        self.damage_reduction = 0.5  # Reduce damage by 50%


class AttackPowerUp(PowerUp):
    """Increases attack damage by 50%"""
    def __init__(self, x, y, duration=300):
        super().__init__(x, y, duration)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(RED)  # Red
        # Draw a lightning-like pattern
        pygame.draw.polygon(self.image, (255, 200, 0), [
            (10, 2), (12, 8), (14, 8), (8, 18), (12, 12), (10, 12)
        ])
        self.rect = self.image.get_rect(center=(x, y))
        self.powerup_type = "attack"
        self.damage_multiplier = 1.5  # Increase damage by 50%


class SpeedPowerUp(PowerUp):
    """Increases movement speed by 50%"""
    def __init__(self, x, y, duration=300):
        super().__init__(x, y, duration)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(PURPLE)  # Purple
        # Draw a speed lines pattern
        pygame.draw.line(self.image, (150, 255, 255), (2, 5), (10, 5), 2)
        pygame.draw.line(self.image, (150, 255, 255), (2, 10), (12, 10), 2)
        pygame.draw.line(self.image, (150, 255, 255), (2, 15), (10, 15), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.powerup_type = "speed"
        self.speed_multiplier = 1.5  # Increase speed by 50%
