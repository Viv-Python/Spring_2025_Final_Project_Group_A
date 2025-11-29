import pygame
from settings import BLUE, PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY, WIDTH, HEIGHT

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
        self.speed_mod = 1.0
        self.speed_mod_timer = 0
        self.invuln_timer = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        base_speed = 5 * self.speed_mod
        if keys[pygame.K_LEFT]:
            self.vel_x = -base_speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = base_speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
        if keys[pygame.K_a]:
            print("Attack!")

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

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Enforce strict horizontal bounds so the player can't leave the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Safety: enforce a ground floor at the bottom of the window in case
        # a platform was missed or the player fell through. This keeps the
        # player from disappearing off-screen.
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def take_damage(self, amount):
        if self.invuln_timer > 0:
            return
        self.health -= amount
        print(f"Player took {amount} damage; health={self.health}")
        self.invuln_timer = 30
        if self.health <= 0:
            print("Player died")
