import pygame, sys
from settings import WIDTH, HEIGHT, WHITE, FPS
from player import Player
from platform import Platform

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
        self.all_sprites = pygame.sprite.Group(self.player, *self.platforms)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update(self.platforms)
            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
