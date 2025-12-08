import pygame
import sys
import random
from settings import (WIDTH, HEIGHT, LEVEL_HEIGHT, WHITE, BLACK, FPS, GAME_STATE_PLAYING, 
                      GAME_STATE_GAMEOVER, GAME_STATE_LEVEL_COMPLETE, GAME_STATE_BOSS_STAGE,
                      NUM_REGULAR_LEVELS, BOSS_LEVEL, ENEMY_COLORS, ENEMY_SIZE,
                      CAMERA_SMOOTH_ENABLED, CAMERA_SMOOTH_FACTOR, CAMERA_PLAYER_OFFSET, CAMERA_DEADZONE)
from camera import Camera
from player import Player
from platform import Platform
from enemies import Enemy, Projectile
from boss import Boss
from obstacles import spike, fire, slow_trap, slippery, block, falling_rock, spike_row, poison_pool, electric, healing_plant, bouncy
from door import Door
from treasure import Treasure
from health_pickup import HealthPickup
from powerup import ArmorPowerUp, AttackPowerUp, SpeedPowerUp
from utils import generate_terrain, generate_obstacles


class Game:
    def __init__(self, level=1, seed=None):
        pygame.init()
        pygame.mixer.init()  # Initialize sound system
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Modular Pygame Game - Level Progression")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.level = level
        self.seed = seed if seed is not None else random.randint(0, 100000)
        self.game_state = GAME_STATE_PLAYING
        self.collected_stickers = set()  # Track collected treasure stickers
        
        # Initialize camera for vertical scrolling
        self.camera = Camera(
            level_width=WIDTH,
            level_height=LEVEL_HEIGHT,
            screen_width=WIDTH,
            screen_height=HEIGHT,
            smooth_enabled=CAMERA_SMOOTH_ENABLED,
            smooth_factor=CAMERA_SMOOTH_FACTOR
        )
        self.camera.set_player_tracking(CAMERA_PLAYER_OFFSET, CAMERA_DEADZONE)
        
        # Music handling
        self.victory_music_playing = False
        self.try_load_victory_music()
        
        # Initialize the level after setting up music
        self.init_level()
        
    def try_load_victory_music(self):
        """Try to load victory music from assets folder"""
        import os
        try:
            # Look for music file in various locations
            possible_paths = [
                'assets/victory_music.mp3',
                'assets/victory_music.wav',
                'assets/victory_music.ogg',
                'src/assets/victory_music.mp3',
                'src/assets/victory_music.wav',
                'src/assets/victory_music.ogg',
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    self.victory_music_path = path
                    print(f"Victory music found at: {path}")
                    return True
            print("No victory music file found. Victory screen will play without music.")
            self.victory_music_path = None
            return False
        except Exception as e:
            print(f"Error loading victory music: {e}")
            self.victory_music_path = None
            return False

    def init_level(self):
        """Initialize a new level with procedurally generated terrain and obstacles"""
        # Player starts at the bottom of the level (in world coordinates), not screen coordinates
        self.player = Player(WIDTH // 2, LEVEL_HEIGHT - 120)
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        self.health_pickups = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.boss = None
        self.enemies_defeated = False
        
        is_boss = (self.level == BOSS_LEVEL)
        
        # Generate terrain
        difficulty = min(1 + (self.level - 1) // 3, 3)
        platforms_list = generate_terrain(seed=self.seed + self.level, difficulty=difficulty, is_boss=is_boss)
        for platform in platforms_list:
            self.platforms.add(platform)
        
        if is_boss:
            self.init_boss_level(difficulty)
        else:
            self.init_regular_level(difficulty)
        
        # Generate obstacles for regular levels (4-6 obstacles instead of 10 to reduce clutter)
        if not is_boss:
            obstacles_count = random.randint(4, 6)
            obstacles_list = generate_obstacles(seed=self.seed + self.level * 100, count=obstacles_count, difficulty=difficulty)
            for obstacle in obstacles_list:
                self.obstacles.add(obstacle)
        
        # Add health pickups (1-3 per level, placed in challenging but accessible spots)
        self._spawn_health_pickups(difficulty)
        
        # Add power-ups (1-2 per level)
        self._spawn_powerups(difficulty)
        
        # Door spawn: at top of level on the highest platform
        self._spawn_door()
        
        # Treasure spawn: only one per level, spawns after enemies defeated (starts hidden)
        self._spawn_treasure()
        
        self.all_sprites = pygame.sprite.Group(self.player, *self.platforms, *self.enemies, 
                                               *self.obstacles, *self.treasures, *self.health_pickups, 
                                               *self.powerups, *self.doors)
        if self.boss:
            self.all_sprites.add(self.boss)
    
    def _spawn_health_pickups(self, difficulty):
        """Spawn 1-3 health pickups at challenging but accessible locations"""
        num_pickups = random.randint(1, 3)
        for _ in range(num_pickups):
            # Place pickups at various heights and x positions
            x = random.randint(100, WIDTH - 100)
            y = random.randint(150, HEIGHT - 200)
            heal_amount = random.randint(10, 30)
            pickup = HealthPickup(x, y, heal_amount=heal_amount)
            self.health_pickups.add(pickup)
    
    def _spawn_powerups(self, difficulty):
        """Spawn 1-2 power-ups at random locations"""
        num_powerups = random.randint(1, 2)
        powerup_types = [ArmorPowerUp, AttackPowerUp, SpeedPowerUp]
        
        for _ in range(num_powerups):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(150, HEIGHT - 200)
            powerup_class = random.choice(powerup_types)
            powerup = powerup_class(x, y, duration=300)  # 300 frames = 5 seconds at 60 FPS
            self.powerups.add(powerup)
    
    def _spawn_door(self):
        """Spawn door sitting ON the topmost platform"""
        # Find the topmost platform and place door on top of it
        topmost_platform = min(self.platforms, key=lambda p: p.rect.y)
        door_width = 50
        door_height = 80
        # Place door ON the platform (door's bottom sits on platform's top)
        door_x = topmost_platform.rect.centerx - door_width // 2
        door_y = topmost_platform.rect.top - door_height  # Door sits on top
        door = Door(door_x, door_y, width=door_width, height=door_height)
        self.doors.add(door)
    
    def _spawn_treasure(self):
        """Spawn one treasure at the middle of the level, hidden until enemies defeated"""
        treasure_x = WIDTH // 2
        treasure_y = HEIGHT // 2
        treasure = Treasure(treasure_x, treasure_y, sticker_id=self.level - 1)
        treasure.hide()  # Hide until enemies are defeated
        self.treasures.add(treasure)

    def init_regular_level(self, difficulty):
        """Initialize a regular level with multiple enemies"""
        # Spawn enemies with color variations (4-7 per level)
        enemy_count = 4 + difficulty
        for i in range(enemy_count):
            x = 100 + i * 100
            y = 250
            pattern = ['patrol', 'chase', 'sine'][i % 3]
            ranged = i % 2 == 1
            speed = 1.5 + (difficulty * 0.5)
            health = 20 + difficulty * 10
            color = ENEMY_COLORS[i % len(ENEMY_COLORS)]
            
            e = Enemy(x, y, pattern=pattern, bounds=(x - 100, x + 100), 
                     speed=speed, health=health, ranged=ranged, color=color)
            self.enemies.add(e)

    def init_boss_level(self, difficulty):
        """Initialize the boss level"""
        # Spawn boss in center
        boss_x = WIDTH // 2 - ENEMY_SIZE
        boss_y = HEIGHT // 2
        self.boss = Boss(boss_x, boss_y)
        self.enemies.add(self.boss)

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_state == GAME_STATE_GAMEOVER:
                    if event.key == pygame.K_r:
                        self.__init__(level=1)
                    elif event.key == pygame.K_q:
                        return False
                elif self.game_state == GAME_STATE_LEVEL_COMPLETE:
                    if event.key == pygame.K_SPACE:
                        # Advance to next level
                        if self.level >= NUM_REGULAR_LEVELS:
                            self.level = BOSS_LEVEL
                        else:
                            self.level += 1
                        self.init_level()
                        self.game_state = GAME_STATE_PLAYING
        return True

    def update(self):
        """Update game state"""
        if self.game_state != GAME_STATE_PLAYING:
            return
        
        # Update player
        self.player.update(self.platforms)
        
        # Update doors
        for door in self.doors:
            door.update()
        
        # Update enemies and projectiles
        for enemy in list(self.enemies):
            if isinstance(enemy, Boss):
                enemy.update(self.player, self.platforms, self.projectiles)
            else:
                enemy.update(self.player, self.platforms, self.projectiles)
        
        self.projectiles.update()
        
        # Player attacks hitting enemies
        for attack in self.player.attacks:
            hits = pygame.sprite.spritecollide(attack, self.enemies, False)
            for enemy in hits:
                enemy.take_damage(attack.damage)
        
        # Player attacks hitting obstacles
        for attack in self.player.attacks:
            hits = pygame.sprite.spritecollide(attack, self.obstacles, False)
            for obstacle in hits:
                if obstacle.take_damage(attack.damage):
                    pass  # Obstacle was destroyed
        
        # Enemy melee contact with player
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            self.player.take_damage(enemy.melee_damage)
        
        # Projectiles hitting player
        proj_hits = pygame.sprite.spritecollide(self.player, self.projectiles, True)
        for p in proj_hits:
            self.player.take_damage(getattr(p, 'damage', 8))
        
        # Obstacles effects on player
        obs_hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        for obstacle in obs_hits:
            if obstacle.damage != 0:
                self.player.take_damage(obstacle.damage)
                if obstacle.single_use:
                    obstacle.kill()
            if obstacle.speed_mod != 1.0:
                self.player.speed_mod = obstacle.speed_mod
                self.player.speed_mod_timer = 120
            if obstacle.blocking:
                if self.player.rect.bottom > obstacle.rect.top and self.player.vel_y > 0:
                    self.player.rect.bottom = obstacle.rect.top
                    self.player.vel_y = 0
        
        # Health pickup collection
        pickup_hits = pygame.sprite.spritecollide(self.player, self.health_pickups, False)
        for pickup in pickup_hits:
            self.player.heal(pickup.heal_amount)
            pickup.collect()
        
        # Power-up collection
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, False)
        for powerup in powerup_hits:
            if powerup.powerup_type == "armor":
                self.player.activate_armor(powerup.duration_remaining)
            elif powerup.powerup_type == "attack":
                self.player.activate_attack(powerup.duration_remaining)
            elif powerup.powerup_type == "speed":
                self.player.activate_speed(powerup.duration_remaining)
            powerup.collect()
        
        # Treasure collection
        treasure_hits = pygame.sprite.spritecollide(self.player, self.treasures, False)
        for treasure in treasure_hits:
            if not treasure.hidden:  # Only collectible if not hidden
                self.collected_stickers.add(treasure.sticker_id)
                treasure.collect()
        
        # Check if all enemies are defeated
        if len(self.enemies) == 0 and not self.enemies_defeated:
            self.enemies_defeated = True
            # Reveal all treasures
            for treasure in self.treasures:
                treasure.reveal()
            # Unlock door
            for door in self.doors:
                door.unlock()
        
        # Check if player exited through door
        for door in self.doors:
            if door.is_player_exiting(self.player.rect):
                if door.unlocked:
                    self.game_state = GAME_STATE_LEVEL_COMPLETE
        
        # Check if player is dead
        if self.player.health <= 0:
            self.game_state = GAME_STATE_GAMEOVER
        
        # Check if we beat the final boss
        if self.level == BOSS_LEVEL and len(self.enemies) == 0 and not self.enemies_defeated:
            # Player won! Mark as enemies defeated to trigger victory sequence
            self.enemies_defeated = True
            self.boss_defeated_timer = 120  # Show victory for 2 seconds before triggering gameover
        
        # Auto-transition to game over screen after boss is defeated
        if self.level == BOSS_LEVEL and self.enemies_defeated and len(self.enemies) == 0:
            if not hasattr(self, 'boss_defeated_timer'):
                self.boss_defeated_timer = 120
            self.boss_defeated_timer -= 1
            if self.boss_defeated_timer <= 0:
                self.game_state = GAME_STATE_GAMEOVER

    def draw_game(self):
        """Draw the game scene with camera offset applied"""
        # Fill background with a gradient effect (parallax-like)
        self.screen.fill((120, 70, 140))  # Base background color
        
        # Update camera based on player position
        self.camera.update(self.player.rect)
        
        # Draw parallax background (creates depth effect)
        # The background scrolls slower than foreground elements
        self._draw_parallax_background()
        
        # Draw game objects with camera offset applied
        # Platforms
        for platform in self.platforms:
            if self.camera.is_visible(platform.rect):
                offset_rect = self.camera.apply_offset(platform.rect)
                self.screen.blit(platform.image, offset_rect)
        
        # Obstacles
        for obstacle in self.obstacles:
            if self.camera.is_visible(obstacle.rect):
                offset_rect = self.camera.apply_offset(obstacle.rect)
                self.screen.blit(obstacle.image, offset_rect)
        
        # Health pickups
        for pickup in self.health_pickups:
            if self.camera.is_visible(pickup.rect):
                offset_rect = self.camera.apply_offset(pickup.rect)
                self.screen.blit(pickup.image, offset_rect)
        
        # Power-ups
        for powerup in self.powerups:
            if self.camera.is_visible(powerup.rect):
                offset_rect = self.camera.apply_offset(powerup.rect)
                self.screen.blit(powerup.image, offset_rect)
        
        # Treasures
        for treasure in self.treasures:
            if self.camera.is_visible(treasure.rect):
                offset_rect = self.camera.apply_offset(treasure.rect)
                self.screen.blit(treasure.image, offset_rect)
        
        # Enemies
        for enemy in self.enemies:
            if self.camera.is_visible(enemy.rect):
                offset_rect = self.camera.apply_offset(enemy.rect)
                self.screen.blit(enemy.image, offset_rect)
        
        # Doors
        for door in self.doors:
            if self.camera.is_visible(door.rect):
                offset_rect = self.camera.apply_offset(door.rect)
                self.screen.blit(door.image, offset_rect)
        
        # Player
        player_offset_rect = self.camera.apply_offset(self.player.rect)
        self.screen.blit(self.player.image, player_offset_rect)
        
        # Player attacks
        for attack in self.player.attacks:
            if self.camera.is_visible(attack.rect):
                offset_rect = self.camera.apply_offset(attack.rect)
                self.screen.blit(attack.image, offset_rect)
        
        # Projectiles
        for projectile in self.projectiles:
            if self.camera.is_visible(projectile.rect):
                offset_rect = self.camera.apply_offset(projectile.rect)
                self.screen.blit(projectile.image, offset_rect)
        
        # Draw enemy health bars (offset applied)
        for enemy in self.enemies:
            if self.camera.is_visible(enemy.rect):
                enemy.draw_health_bar(self.screen, self.camera)
        
        # Draw UI (not affected by camera, stays on screen)
        self._draw_ui()
    
    def _draw_parallax_background(self):
        """
        Draw parallax background layers to create depth perception.
        Background elements move slower than the foreground.
        Different backgrounds for each level.
        """
        camera_y = self.camera.y
        
        # Define level-specific color schemes
        if self.level == 1:
            # Level 1: Forest/Green theme
            far_color = (20, 40, 20)      # Dark green
            mid_color = (40, 80, 40)      # Forest green
            near_color = (60, 120, 60)    # Light green
        elif self.level == 2:
            # Level 2: Sky/Blue theme
            far_color = (30, 50, 100)     # Deep blue
            mid_color = (50, 100, 150)    # Sky blue
            near_color = (100, 150, 200)  # Light blue
        elif self.level == 3:
            # Level 3: Lava/Orange theme
            far_color = (60, 20, 10)      # Dark red
            mid_color = (120, 40, 20)     # Lava orange
            near_color = (180, 80, 40)    # Light orange
        elif self.level == BOSS_LEVEL:
            # Boss level: Dark/Purple theme
            far_color = (40, 10, 60)      # Dark purple
            mid_color = (80, 20, 120)     # Purple
            near_color = (140, 50, 180)   # Light purple
        else:
            # Default fallback
            far_color = (80, 40, 100)
            mid_color = (100, 50, 120)
            near_color = (120, 70, 140)
        
        # Far background (moves slowly)
        far_offset = int(camera_y * 0.2)
        far_rect = pygame.Rect(0, -far_offset % HEIGHT, WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, far_color, (0, 0, WIDTH, HEIGHT))
        
        # Mid background (moves at medium speed)
        mid_offset = int(camera_y * 0.5)
        mid_y = (-mid_offset % HEIGHT)
        pygame.draw.rect(self.screen, mid_color, (0, mid_y, WIDTH, HEIGHT))
        if mid_y > 0:
            pygame.draw.rect(self.screen, mid_color, (0, mid_y - HEIGHT, WIDTH, HEIGHT))
        
        # Near background (moves with most parallax effect)
        near_offset = int(camera_y * 0.7)
        near_y = (-near_offset % HEIGHT)
        pygame.draw.rect(self.screen, near_color, (0, near_y, WIDTH, HEIGHT))
        if near_y > 0:
            pygame.draw.rect(self.screen, near_color, (0, near_y - HEIGHT, WIDTH, HEIGHT))
    
    def _draw_ui(self):
        """
        Draw UI elements that should stay fixed on screen (not scroll with camera).
        Includes health, level, stickers, power-ups, and controls.
        """
        # Draw player health
        health_color = (0, 255, 0) if self.player.health > 50 else (255, 165, 0) if self.player.health > 25 else (255, 0, 0)
        # Add damage feedback effect
        if self.player.damage_taken_timer > 0:
            health_color = (255, 0, 0)
        health_text = self.small_font.render(f"Health: {self.player.health}/{self.player.max_health}", True, health_color)
        self.screen.blit(health_text, (10, 10))
        
        # Draw level
        level_text = self.small_font.render(f"Level: {self.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (WIDTH - 200, 10))
        
        # Draw collected stickers
        sticker_text = self.small_font.render(f"Stickers: {len(self.collected_stickers)}", True, (255, 165, 0))
        self.screen.blit(sticker_text, (WIDTH // 2 - 60, 10))
        
        # Draw sticker indicators
        sticker_x = 50
        for i in range(10):
            if i in self.collected_stickers:
                pygame.draw.circle(self.screen, (255, 215, 0), (sticker_x + i * 20, 40), 5)
            else:
                pygame.draw.circle(self.screen, (200, 200, 200), (sticker_x + i * 20, 40), 5)
        
        # Draw active power-ups with duration
        powerup_y = 70
        if self.player.armor_active:
            armor_text = self.small_font.render(f"ARMOR: {self.player.armor_timer // 60}s", True, (150, 150, 150))
            self.screen.blit(armor_text, (10, powerup_y))
            powerup_y += 25
        
        if self.player.attack_mod > 1.0:
            attack_text = self.small_font.render(f"ATTACK+: {self.player.attack_mod_timer // 60}s", True, (255, 100, 100))
            self.screen.blit(attack_text, (10, powerup_y))
            powerup_y += 25
        
        if self.player.speed_mod > 1.0:
            speed_text = self.small_font.render(f"SPEED+: {self.player.speed_mod_timer // 60}s", True, (200, 0, 200))
            self.screen.blit(speed_text, (10, powerup_y))
            powerup_y += 25
        
        # Draw pickup collected feedback
        if self.player.pickup_collected_timer > 0:
            pickup_text = self.small_font.render("HEALTH +", True, (0, 255, 0))
            self.screen.blit(pickup_text, (WIDTH - 150, 50))
        
        # Draw controls hint
        controls_text = self.small_font.render("Arrow Keys: Move | Space: Jump | A: Attack | Down+Space: Jump Down", True, (100, 100, 100))
        self.screen.blit(controls_text, (10, HEIGHT - 30))
        
        # Draw door unlock message if applicable
        for door in self.doors:
            if door.should_show_unlock_message():
                unlock_text = self.font.render("DOOR UNLOCKED!", True, (0, 255, 0))
                text_rect = unlock_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                # Draw semi-transparent background for text
                bg_rect = text_rect.inflate(40, 20)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
                pygame.draw.rect(self.screen, (0, 255, 0), bg_rect, 3)
                self.screen.blit(unlock_text, text_rect)
        
        # Optional: Draw camera debug info (can be toggled)
        # camera_info = self.camera.get_info()
        # debug_text = self.small_font.render(camera_info, True, (0, 0, 0))
        # self.screen.blit(debug_text, (10, HEIGHT - 60))

    def draw_gameover(self):
        """Draw the game over screen"""
        self.screen.fill(WHITE)
        
        # Check if player won by defeating the boss
        if self.level == BOSS_LEVEL and self.enemies_defeated and len(self.enemies) == 0:
            # Victory screen - YOU WON!!
            # Play victory music once
            if not self.victory_music_playing and self.victory_music_path:
                try:
                    pygame.mixer.music.load(self.victory_music_path)
                    pygame.mixer.music.play(-1)  # Loop the music
                    self.victory_music_playing = True
                    print("Victory music started playing!")
                except Exception as e:
                    print(f"Error playing victory music: {e}")
            
            self.screen.fill((50, 100, 50))  # Dark green background
            
            victory_text = pygame.font.Font(None, 80).render("YOU WON!!", True, (0, 255, 0))
            subtitle_text = self.font.render("You defeated the Boss and collected the treasure!", True, (255, 255, 0))
            final_text = self.small_font.render(f"Final Stickers Collected: {len(self.collected_stickers)}/10", True, (255, 255, 255))
            restart_text = self.small_font.render("Press R to Play Again or Q to Quit", True, (200, 200, 200))
            
            self.screen.blit(victory_text, (WIDTH // 2 - 200, HEIGHT // 2 - 150))
            self.screen.blit(subtitle_text, (WIDTH // 2 - 230, HEIGHT // 2 - 50))
            self.screen.blit(final_text, (WIDTH // 2 - 150, HEIGHT // 2 + 30))
            self.screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 100))
        else:
            # Defeat screen
            gameover_text = self.font.render("GAME OVER", True, (255, 0, 0))
            level_text = self.font.render(f"Level Reached: {self.level}", True, BLACK)
            restart_text = self.small_font.render("Press R to Restart or Q to Quit", True, BLACK)
            
            self.screen.blit(gameover_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
            self.screen.blit(level_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
            self.screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))

    def draw_level_complete(self):
        """Draw the level complete screen"""
        self.screen.fill(WHITE)
        
        complete_text = self.font.render("LEVEL COMPLETE", True, (0, 150, 0))
        next_text = self.small_font.render(f"Level {self.level + 1} Ready", True, BLACK)
        continue_text = self.small_font.render("Press SPACE to Continue", True, BLACK)
        
        self.screen.blit(complete_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        self.screen.blit(next_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        self.screen.blit(continue_text, (WIDTH // 2 - 140, HEIGHT // 2 + 60))

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            
            if self.game_state == GAME_STATE_PLAYING:
                self.draw_game()
            elif self.game_state == GAME_STATE_LEVEL_COMPLETE:
                self.draw_level_complete()
            else:  # GAME_STATE_GAMEOVER
                self.draw_gameover()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

