import pygame
import sys
import random
from settings import WIDTH, HEIGHT, WHITE, BLACK, FPS, GAME_STATE_PLAYING, GAME_STATE_GAMEOVER
from player import Player
from platform import Platform
from enemies import Enemy, Projectile
from obstacles import spike, fire, slow_trap, slippery, block, falling_rock, spike_row, poison_pool, electric, healing_plant, bouncy
from utils import generate_terrain, generate_obstacles


class Game:
    def __init__(self, level=1, seed=None):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Modular Pygame Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.level = level
        self.seed = seed if seed is not None else random.randint(0, 100000)
        self.game_state = GAME_STATE_PLAYING
        
        self.init_level()

    def init_level(self):
        """Initialize a new level with procedurally generated terrain and obstacles"""
        self.player = Player(100, 400)
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        # Generate terrain procedurally with difficulty scaling
        difficulty = min(1 + (self.level - 1) // 3, 3)
        platforms_list = generate_terrain(seed=self.seed + self.level, difficulty=difficulty)
        for platform in platforms_list:
            self.platforms.add(platform)
        
        # Generate obstacles procedurally
        obstacles_list = generate_obstacles(seed=self.seed + self.level * 100, count=10, difficulty=difficulty)
        for obstacle in obstacles_list:
            self.obstacles.add(obstacle)
        
        # Spawn enemies based on level difficulty
        enemy_count = 1 + (self.level - 1) // 2
        for i in range(enemy_count):
            x = 200 + i * 150
            y = 300
            pattern = ['patrol', 'chase', 'sine'][i % 3]
            ranged = i % 2 == 1
            speed = 1.5 + (difficulty * 0.5)
            e = Enemy(x, y, pattern=pattern, bounds=(x - 100, x + 100), 
                     speed=speed, health=20 + difficulty * 10, ranged=ranged)
            self.enemies.add(e)
        
        self.all_sprites = pygame.sprite.Group(self.player, *self.platforms, *self.enemies, *self.obstacles)

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_state == GAME_STATE_GAMEOVER:
                    if event.key == pygame.K_r:
                        self.__init__(level=self.level)
                    elif event.key == pygame.K_q:
                        return False
        return True

    def update(self):
        """Update game state"""
        if self.game_state != GAME_STATE_PLAYING:
            return
        
        # Update player
        self.player.update(self.platforms)
        
        # Update enemies and projectiles
        for enemy in list(self.enemies):
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
        
        # Check if player is dead
        if self.player.health <= 0:
            self.game_state = GAME_STATE_GAMEOVER
        
        # Check if all enemies are defeated (level complete)
        if len(self.enemies) == 0 and self.level > 0:
            self.level += 1
            self.init_level()

    def draw_game(self):
        """Draw the game scene"""
        self.screen.fill(WHITE)
        
        # Draw all sprites
        self.platforms.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.player.attacks.draw(self.screen)
        self.projectiles.draw(self.screen)
        
        # Draw enemy health bars
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)
        
        # Draw obstacle health bars
        for obstacle in self.obstacles:
            obstacle.draw_health_bar(self.screen)
        
        # Draw player health
        health_text = self.small_font.render(f"Health: {self.player.health}/{self.player.max_health}", True, (0, 0, 0))
        self.screen.blit(health_text, (10, 10))
        
        # Draw level
        level_text = self.small_font.render(f"Level: {self.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (WIDTH - 200, 10))
        
        # Draw controls hint
        controls_text = self.small_font.render("Arrow Keys: Move | Space: Jump | A: Attack", True, (100, 100, 100))
        self.screen.blit(controls_text, (10, HEIGHT - 30))

    def draw_gameover(self):
        """Draw the game over screen"""
        self.screen.fill(WHITE)
        
        gameover_text = self.font.render("GAME OVER", True, (255, 0, 0))
        level_text = self.font.render(f"Level Reached: {self.level}", True, BLACK)
        restart_text = self.small_font.render("Press R to Restart or Q to Quit", True, BLACK)
        
        self.screen.blit(gameover_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        self.screen.blit(level_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        self.screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            
            if self.game_state == GAME_STATE_PLAYING:
                self.draw_game()
            else:
                self.draw_gameover()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

