import pygame
from settings import BLUE, PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY, WIDTH, HEIGHT

class Attack(pygame.sprite.Sprite):
    """Represents the player's attack hitbox"""
    def __init__(self, x, y, width=50, height=40, direction=1, damage=15):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 200, 255))
        self.image.set_alpha(100)  # Semi-transparent
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = damage
        self.direction = direction
        self.lifetime = 10  # frames

    def update(self, *args):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.speed_mod = 1.0
        self.speed_mod_timer = 0
        self.invuln_timer = 0
        self.attack_cooldown = 0
        self.facing_right = True
        self.attacks = pygame.sprite.Group()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        base_speed = 5 * self.speed_mod
        if keys[pygame.K_LEFT]:
            self.vel_x = -base_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel_x = base_speed
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
        if keys[pygame.K_a]:
            self.attack()

    def attack(self):
        """Create an attack hitbox"""
        if self.attack_cooldown <= 0:
            attack_width = 40
            attack_height = 40
            if self.facing_right:
                attack_x = self.rect.right
            else:
                attack_x = self.rect.left - attack_width
            
            attack = Attack(attack_x, self.rect.centery - attack_height // 2, 
                          attack_width, attack_height, 
                          direction=1 if self.facing_right else -1, damage=15)
            self.attacks.add(attack)
            self.attack_cooldown = 15  # 15 frame cooldown

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()
        
        # update temporary modifiers
        if self.speed_mod_timer > 0:
            self.speed_mod_timer -= 1
            if self.speed_mod_timer == 0:
                self.speed_mod = 1.0
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Enforce strict horizontal bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Safety: enforce a ground floor
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Update attacks
        self.attacks.update()

    def take_damage(self, amount):
        if self.invuln_timer > 0:
            return
        self.health -= amount
        print(f"Player took {amount} damage; health={self.health}")
        self.invuln_timer = 30
        if self.health <= 0:
            print("Player died")
            self.health = 0

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)

