import pygame
import random
import os
from enemies import Enemy
from settings import PURPLE, ENEMY_SIZE, GRAVITY, WIDTH, HEIGHT, YELLOW, GREEN, BLACK

class Boss(pygame.sprite.Sprite):
    """Boss enemy with distinct behavior and higher difficulty"""
    def __init__(self, x, y):
        super().__init__()
        # Try to load the scary bear asset
        bear_image = self._load_bear_asset()
        if bear_image is not None:
            self.image = bear_image
        else:
            # Fallback: create a purple square with crown if asset not found
            self.image = pygame.Surface((ENEMY_SIZE * 2, ENEMY_SIZE * 2))
            self.image.fill(PURPLE)
            # Draw a crown-like pattern
            pygame.draw.polygon(self.image, (255, 215, 0), [
                (20, 20), (25, 10), (30, 20), (35, 10), (40, 20),
                (40, 40), (20, 40)
            ])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1.5
        self.health = 150
        self.max_health = 150
        self.pattern = 'boss_pattern'
        self.vx = self.speed
        self.vy = 0
        self.melee_damage = 20
        self.ranged = True
        self.fire_cooldown = 0
        self.phase = 1  # Boss has phases
        self.phase_timer = 0
        self.attack_pattern = 0
        self.hitbox = self.rect.copy()
        self.bounds = (50, WIDTH - 50)

    def _load_bear_asset(self):
        """Load the scary bear asset from disk"""
        bear_paths = [
            'assets/enemies/scary_bear.png',
            '../assets/enemies/scary_bear.png',
            'src/../assets/enemies/scary_bear.png',
        ]
        
        for path in bear_paths:
            if os.path.exists(path):
                try:
                    bear_image = pygame.image.load(path)
                    # Convert to ensure compatibility
                    bear_image = bear_image.convert_alpha()
                    return bear_image
                except Exception as e:
                    print(f"Failed to load bear asset from {path}: {e}")
                    continue
        
        print("Bear asset not found, using fallback purple square")
        return None

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > 10:
            self.vy = 10

    def draw_health_bar(self, surface, camera=None):
        """
        Draw a large health bar for the boss.
        
        Args:
            surface: Pygame surface to draw on
            camera: Optional Camera object to apply offset for scrolling
        """
        bar_width = ENEMY_SIZE * 2
        bar_height = 10
        bar_x = self.rect.x
        bar_y = self.rect.y - 15
        
        # Apply camera offset if provided (for scrolling support)
        if camera is not None:
            bar_x, bar_y = camera.apply_offset_pos(bar_x, bar_y)
        
        # Background (red)
        pygame.draw.rect(surface, (220, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int(bar_width * (self.health / self.max_health))
        if health_width > 0:
            pygame.draw.rect(surface, (50, 200, 50), (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height), 2)

    def update(self, player, platforms, projectiles_group=None):
        """Boss has advanced movement and attack patterns"""
        
        # Update phase based on health
        if self.health < self.max_health * 0.5:
            self.phase = 2
        if self.health < self.max_health * 0.25:
            self.phase = 3
        
        self.phase_timer += 1
        
        # Boss movement pattern
        if self.phase == 1:
            # Normal patrol
            self.rect.x += self.vx
            if self.rect.left <= self.bounds[0]:
                self.vx = abs(self.vx)
                self.rect.left = self.bounds[0]
            elif self.rect.right >= self.bounds[1]:
                self.vx = -abs(self.vx)
                self.rect.right = self.bounds[1]
        elif self.phase == 2:
            # Faster movement and occasional jumps
            self.rect.x += self.vx * 1.5
            if self.rect.left <= self.bounds[0]:
                self.vx = abs(self.vx)
                self.rect.left = self.bounds[0]
                self.vy = -12  # Jump
            elif self.rect.right >= self.bounds[1]:
                self.vx = -abs(self.vx)
                self.rect.right = self.bounds[1]
                self.vy = -12  # Jump
        else:  # phase 3
            # Aggressive zigzag pattern
            offset = int((self.phase_timer % 20) * 2 - 20)
            self.rect.x = player.rect.centerx - ENEMY_SIZE + offset
            if self.phase_timer % 10 == 0:
                self.vy = -10  # Frequent jumps

        # Gravity and platform collision
        self.apply_gravity()
        self.rect.y += self.vy
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0:
                    self.rect.bottom = p.rect.top
                    self.vy = 0

        # Prevent falling off screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy = 0

        # Boss ranged attack with patterns
        if projectiles_group is not None:
            if self.phase == 1 and self.fire_cooldown <= 0:
                # Single shots
                self.fire_projectile(player, projectiles_group)
                self.fire_cooldown = 80
            elif self.phase == 2 and self.fire_cooldown <= 0:
                # Burst attacks
                for _ in range(2):
                    self.fire_projectile(player, projectiles_group)
                self.fire_cooldown = 60
            elif self.phase == 3 and self.fire_cooldown <= 0:
                # Spread attack
                self.fire_spread_attack(player, projectiles_group)
                self.fire_cooldown = 40
            
            if self.fire_cooldown > 0:
                self.fire_cooldown -= 1

        # Update hitbox
        self.hitbox = self.rect.copy()

    def fire_projectile(self, player, projectiles_group):
        """Fire a projectile at the player"""
        from enemies import Projectile
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            vx = (dx / distance) * 7
            vy = (dy / distance) * 7
        else:
            vx, vy = 7, 0
        proj = Projectile(self.rect.centerx, self.rect.centery, vx=vx, vy=vy, dmg=15)
        if hasattr(projectiles_group, 'add'):
            projectiles_group.add(proj)
        else:
            projectiles_group.append(proj)

    def fire_spread_attack(self, player, projectiles_group):
        """Fire multiple projectiles in a spread pattern"""
        from enemies import Projectile
        angles = [-0.3, 0, 0.3]  # Spread pattern
        dx = player.rect.centerx - self.rect.centerx
        base_speed = 7
        for angle_offset in angles:
            angle = angle_offset
            vx = base_speed * (1 + angle)
            vy = base_speed * angle * 0.5
            proj = Projectile(self.rect.centerx, self.rect.centery, vx=vx, vy=vy, dmg=12)
            if hasattr(projectiles_group, 'add'):
                projectiles_group.add(proj)
            else:
                projectiles_group.append(proj)

    def take_damage(self, amount):
        """Boss takes damage"""
        self.health -= amount
        if self.health <= 0:
            self.kill()
