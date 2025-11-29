import pygame
import math
from settings import RED, ENEMY_SIZE, GRAVITY, WIDTH, HEIGHT, YELLOW, GREEN, BLACK

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy=0, dmg=10):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.damage = dmg

    def update(self, *args):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, pattern='patrol', bounds=None, speed=2, health=20, melee_damage=10, ranged=False):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = health
        self.max_health = health
        self.pattern = pattern
        self.bounds = bounds
        self.vx = speed
        self.vy = 0
        self.melee_damage = melee_damage
        self.ranged = ranged
        self.fire_cooldown = 0
        self.sine_offset = 0
        self.hitbox = self.rect.copy()

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > 10:
            self.vy = 10

    def draw_health_bar(self, surface):
        """Draw a health bar above the enemy"""
        bar_width = ENEMY_SIZE
        bar_height = 5
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        
        # Background (red)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int(bar_width * (self.health / self.max_health))
        if health_width > 0:
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))

    def update(self, player, platforms, projectiles_group=None):
        # movement patterns
        if self.pattern == 'patrol':
            self.rect.x += self.vx
            if self.bounds:
                left, right = self.bounds
                if self.rect.left < left or self.rect.right > right:
                    self.vx *= -1
        elif self.pattern == 'chase':
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
        elif self.pattern == 'sine':
            self.sine_offset += 0.05
            self.rect.y += int(math.sin(self.sine_offset) * 2)
            self.rect.x += self.vx

        # simple gravity and platform collision
        self.apply_gravity()
        self.rect.y += self.vy
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0:
                    self.rect.bottom = p.rect.top
                    self.vy = 0

        # Update hitbox
        self.hitbox = self.rect.copy()

        # ranged attack
        if self.ranged and projectiles_group is not None:
            if self.fire_cooldown <= 0:
                dx = player.rect.centerx - self.rect.centerx
                dir = 1 if dx > 0 else -1
                proj = Projectile(self.rect.centerx + dir * ENEMY_SIZE // 2, self.rect.centery, vx=dir * 6, dmg=8)
                projectiles_group.add(proj)
                self.fire_cooldown = 60
            else:
                self.fire_cooldown -= 1

    def take_damage(self, amount):
        """Enemy takes damage and is removed when health reaches zero"""
        self.health -= amount
        if self.health <= 0:
            self.kill()

