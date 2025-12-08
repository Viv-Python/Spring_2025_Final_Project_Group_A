import pygame
from settings import BLUE, PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY, WIDTH, HEIGHT
from asset_loader import get_loader

class Attack(pygame.sprite.Sprite):
    """Represents the player's attack hitbox"""
    def __init__(self, x, y, width=70, height=50, direction=1, damage=15):
        super().__init__()
        self.image = pygame.Surface((width, height))
        # Draw a sword-like shape
        self.image.fill((100, 100, 100))
        pygame.draw.polygon(self.image, (200, 200, 100), [
            (width // 2 - 5, 5), (width // 2 + 5, 5), 
            (width // 2 + 3, height - 5), (width // 2 - 3, height - 5)
        ])
        self.image.set_alpha(180)  # Semi-transparent
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
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
        # Try to load player sprite from assets
        loader = get_loader()
        player_sprite = loader.get_player_idle()
        if player_sprite is not None:
            # Scale sprite to match player dimensions
            self.image = pygame.transform.scale(player_sprite, (self.width, self.height))
            print(f"✓ Player sprite loaded successfully ({self.width}x{self.height})")
        else:
            # Fallback: draw a character sprite
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(BLUE)
            # Draw a simple character face and body
            pygame.draw.circle(self.image, (255, 200, 150), (self.width // 2, 12), 8)  # Head
            pygame.draw.line(self.image, (255, 200, 150), (self.width // 2, 20), (self.width // 2, 40), 3)  # Body
            pygame.draw.circle(self.image, (50, 50, 100), (self.width // 2 - 4, 12), 2)  # Left eye
            pygame.draw.circle(self.image, (50, 50, 100), (self.width // 2 + 4, 12), 2)  # Right eye
            print("⚠ Player sprite not found, using fallback")
        
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
        self.falling_through = False
        self.fall_through_timer = 0
        
        # Power-up attributes
        self.armor_active = False
        self.armor_timer = 0
        self.attack_mod = 1.0
        self.attack_mod_timer = 0
        
        # Feedback timers
        self.damage_taken_timer = 0
        self.pickup_collected_timer = 0
        
        # Animation attributes
        self.walking_animation = loader.get_player_walking()
        self.animation_frame = 0
        self.animation_counter = 0

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
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.vel_y = -15
            elif keys[pygame.K_DOWN] and not self.falling_through:
                # Allow jumping down from non-ground platforms
                self.falling_through = True
                self.fall_through_timer = 10
                self.vel_y = 5  # Start falling
        if keys[pygame.K_a]:
            self.attack()

    def attack(self):
        """Create an attack hitbox"""
        if self.attack_cooldown <= 0:
            attack_width = 70  # Increased reach
            attack_height = 50
            # Apply attack damage modifier from power-ups
            base_damage = 15
            final_damage = int(base_damage * self.attack_mod)
            if self.facing_right:
                attack_x = self.rect.right
            else:
                attack_x = self.rect.left - attack_width
            
            attack = Attack(attack_x, self.rect.centery - attack_height // 2, 
                          attack_width, attack_height, 
                          direction=1 if self.facing_right else -1, damage=final_damage)
            self.attacks.add(attack)
            self.attack_cooldown = 15  # 15 frame cooldown

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

    def update(self, platforms):
        self.handle_input()
        
        # update temporary modifiers
        if self.speed_mod_timer > 0:
            self.speed_mod_timer -= 1
            if self.speed_mod_timer == 0:
                self.speed_mod = 1.0
        if self.attack_mod_timer > 0:
            self.attack_mod_timer -= 1
            if self.attack_mod_timer == 0:
                self.attack_mod = 1.0
        if self.armor_timer > 0:
            self.armor_timer -= 1
            if self.armor_timer == 0:
                self.armor_active = False
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.damage_taken_timer > 0:
            self.damage_taken_timer -= 1
        if self.pickup_collected_timer > 0:
            self.pickup_collected_timer -= 1
        
        # Update fall-through timer
        if self.fall_through_timer > 0:
            self.fall_through_timer -= 1
            if self.fall_through_timer == 0:
                self.falling_through = False

        # Apply horizontal movement
        self.rect.x += self.vel_x
        
        # Apply vertical movement and check collision
        self.rect.y += self.vel_y
        self.on_ground = False
        
        # Check collision with platforms
        for platform in platforms:
            # Use a slightly expanded platform rect for collision to avoid missing edge cases
            # This prevents the player from falling through when exactly on the platform surface
            check_rect = platform.rect.inflate(0, 2)
            
            if self.rect.colliderect(check_rect):
                if self.vel_y >= 0:  # Only collide when moving down or stationary
                    # Player is landing on this platform
                    if not self.falling_through:
                        # Place player on top of platform
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                        self.falling_through = False
                        break  # Don't check other platforms once landed

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
            self.falling_through = False
        
        # Apply gravity AFTER collision check
        # This ensures on_ground is properly set before gravity is applied
        if not self.on_ground or self.vel_y < 0:
            self.apply_gravity()
        else:
            # When on ground and not jumping, vel_y stays 0
            self.vel_y = 0

        # Update attacks
        self.attacks.update()

    def take_damage(self, amount):
        if self.invuln_timer > 0:
            return
        
        # Apply armor reduction if active
        actual_damage = amount
        if self.armor_active:
            actual_damage = int(amount * 0.5)  # 50% damage reduction
        
        self.health -= actual_damage
        print(f"Player took {actual_damage} damage (armor: {self.armor_active}); health={self.health}")
        self.invuln_timer = 30
        self.damage_taken_timer = 30  # Show damage feedback for 30 frames
        
        if self.health <= 0:
            print("Player died")
            self.health = 0
    
    def activate_armor(self, duration=300):
        """Activate armor power-up"""
        self.armor_active = True
        self.armor_timer = duration
        print(f"Armor activated for {duration} frames!")
    
    def activate_attack(self, duration=300):
        """Activate attack power-up"""
        self.attack_mod = 1.5
        self.attack_mod_timer = duration
        print(f"Attack boost activated for {duration} frames!")
    
    def activate_speed(self, duration=300):
        """Activate speed power-up"""
        self.speed_mod = 1.5
        self.speed_mod_timer = duration
        print(f"Speed boost activated for {duration} frames!")

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)
        self.pickup_collected_timer = 30  # Show pickup feedback for 30 frames
        print(f"Player healed by {amount}; health={self.health}")


