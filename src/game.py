import pygame, sys
from settings import WIDTH, HEIGHT, WHITE, FPS
from player import Player
from platform import Platform
from enemies import Enemy
from enemies import Projectile
import enemies
from obstacles import spike, fire, slow_trap, slippery, block, falling_rock, spike_row, poison_pool, electric, healing_plant, bouncy
import obstacles

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Modular Pygame Game")
        self.clock = pygame.time.Clock()
        self.player = Player(100, 400)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform(0, HEIGHT - 40, WIDTH, 40))
        self.platforms.add(Platform(300, 450, 200, 20))
        # groups for enemies, projectiles and obstacles
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        # sample enemy spawns
        e1 = Enemy(400, 400, pattern='patrol', bounds=(300, 500), speed=2, melee_damage=8)
        e2 = Enemy(600, 350, pattern='sine', bounds=None, speed=1.5, ranged=True)
        e3 = Enemy(200, 400, pattern='chase', bounds=None, speed=1.8)
        self.enemies.add(e1, e2, e3)

        # sample obstacles (10 types)
        self.obstacles.add(spike(500, HEIGHT - 40 - 40))
        self.obstacles.add(fire(150, HEIGHT - 40 - 40))
        self.obstacles.add(slow_trap(350, HEIGHT - 40 - 40))
        self.obstacles.add(slippery(450, HEIGHT - 40 - 40))
        self.obstacles.add(block(50, HEIGHT - 140, 80, 100))
        self.obstacles.add(falling_rock(700, 0))
        for s in spike_row(100, HEIGHT - 40 - 40, count=3):
            self.obstacles.add(s)
        self.obstacles.add(poison_pool(250, HEIGHT - 40 - 40))
        self.obstacles.add(electric(320, HEIGHT - 40 - 40))
        self.obstacles.add(healing_plant(720, HEIGHT - 40 - 40))

        self.all_sprites = pygame.sprite.Group(self.player, *self.platforms, *self.enemies, *self.obstacles)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update(self.platforms)
            # update enemies and their projectiles
            for enemy in list(self.enemies):
                enemy.update(self.player, self.platforms, self.projectiles)
            self.projectiles.update()

            # collisions: enemy melee contact
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for en in hits:
                self.player.take_damage(en.melee_damage)

            # projectiles hitting player
            proj_hits = pygame.sprite.spritecollide(self.player, self.projectiles, True)
            for p in proj_hits:
                self.player.take_damage(getattr(p, 'damage', 8))

            # obstacles effects
            obs_hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            for o in obs_hits:
                if o.damage != 0:
                    # healing if negative damage
                    self.player.take_damage(o.damage)
                    if o.single_use:
                        o.kill()
                if o.speed_mod != 1.0:
                    self.player.speed_mod = o.speed_mod
                    self.player.speed_mod_timer = 120
                if o.blocking:
                    # simple push back: move player up onto platform-like surface
                    if self.player.rect.bottom > o.rect.top:
                        self.player.rect.bottom = o.rect.top
                        self.player.vel_y = 0

            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            self.projectiles.draw(self.screen)
            pygame.display.flip()
