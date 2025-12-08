import pygame
from settings import OBSTACLE_SIZE, GRAY, RED, YELLOW, GREEN, BLUE, BLACK
from asset_loader import get_loader


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=OBSTACLE_SIZE, height=OBSTACLE_SIZE, damage=0, blocking=False, speed_mod=1.0, color=GRAY, single_use=False, health=None, sprite_type=None):
        super().__init__()
        
        # Try to load obstacle sprite from assets
        if sprite_type:
            loader = get_loader()
            obstacle_sprite = loader.get_obstacle_sprite(sprite_type)
            if obstacle_sprite is not None:
                self.image = pygame.transform.scale(obstacle_sprite, (width, height))
            else:
                # Fallback: draw colored sprite
                self.image = pygame.Surface((width, height))
                self.image.fill(color)
        else:
            # No sprite type provided, use colored fallback
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = damage
        self.blocking = blocking
        self.speed_mod = speed_mod
        self.single_use = single_use
        self.health = health
        self.max_health = health
        self.color = color
        self.width = width
        self.height = height
        self.hitbox = self.rect.copy()

    def take_damage(self, amount):
        """Obstacle takes damage and is destroyed when health reaches zero"""
        if self.health is not None:
            self.health -= amount
            if self.health <= 0:
                self.kill()
                return True
        return False

    def draw_health_bar(self, surface):
        """Draw a health bar above the obstacle if it has health"""
        if self.health is not None and self.max_health is not None:
            bar_width = self.width
            bar_height = 4
            bar_x = self.rect.x
            bar_y = self.rect.y - 8
            
            # Background (red)
            pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
            
            # Health (green)
            health_width = int(bar_width * (self.health / self.max_health))
            if health_width > 0:
                pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))


def spike(x, y):
    return Obstacle(x, y, damage=20, blocking=False, color=RED, single_use=False, health=1, sprite_type='spike')


def fire(x, y):
    return Obstacle(x, y, damage=10, blocking=False, color=(255, 120, 0), single_use=False, health=2, sprite_type='fire')


def slow_trap(x, y):
    return Obstacle(x, y, damage=0, blocking=False, speed_mod=0.5, color=(150, 150, 255), health=1, sprite_type='slow_trap')


def slippery(x, y):
    return Obstacle(x, y, damage=0, blocking=False, speed_mod=1.6, color=(200, 200, 255), health=1, sprite_type='slippery')


def block(x, y, w=OBSTACLE_SIZE, h=OBSTACLE_SIZE):
    return Obstacle(x, y, w, h, damage=0, blocking=True, color=(100, 100, 100), health=3, sprite_type='block')


def falling_rock(x, y):
    return Obstacle(x, y, damage=25, blocking=False, color=(80, 50, 30), single_use=True, health=2, sprite_type='falling_rock')


def spike_row(x, y, count=3):
    return [spike(x + i * OBSTACLE_SIZE, y) for i in range(count)]


def poison_pool(x, y):
    return Obstacle(x, y, damage=5, blocking=False, color=(50, 200, 50), health=1, sprite_type='poison_pool')


def electric(x, y):
    return Obstacle(x, y, damage=15, blocking=False, color=(180, 180, 255), health=2, sprite_type='electric')


def healing_plant(x, y):
    return Obstacle(x, y, damage=-15, blocking=False, color=(120, 255, 120), single_use=True, health=1, sprite_type='healing_plant')


def bouncy(x, y):
    return Obstacle(x, y, damage=0, blocking=False, color=(255, 150, 255), speed_mod=1.0, health=2, sprite_type='bouncy')

