import pygame
from settings import OBSTACLE_SIZE, GRAY, RED, YELLOW, GREEN, BLUE


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=OBSTACLE_SIZE, height=OBSTACLE_SIZE, damage=0, blocking=False, speed_mod=1.0, color=GRAY, single_use=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = damage
        self.blocking = blocking
        self.speed_mod = speed_mod
        self.single_use = single_use


def spike(x, y):
    return Obstacle(x, y, damage=20, blocking=False, color=RED, single_use=False)


def fire(x, y):
    return Obstacle(x, y, damage=10, blocking=False, color=(255, 120, 0), single_use=False)


def slow_trap(x, y):
    return Obstacle(x, y, damage=0, blocking=False, speed_mod=0.5, color=(150, 150, 255))


def slippery(x, y):
    return Obstacle(x, y, damage=0, blocking=False, speed_mod=1.6, color=(200, 200, 255))


def block(x, y, w=OBSTACLE_SIZE, h=OBSTACLE_SIZE):
    return Obstacle(x, y, w, h, damage=0, blocking=True, color=(100, 100, 100))


def falling_rock(x, y):
    return Obstacle(x, y, damage=25, blocking=False, color=(80, 50, 30), single_use=True)


def spike_row(x, y, count=3):
    return [spike(x + i * OBSTACLE_SIZE, y) for i in range(count)]


def poison_pool(x, y):
    return Obstacle(x, y, damage=5, blocking=False, color=(50, 200, 50))


def electric(x, y):
    return Obstacle(x, y, damage=15, blocking=False, color=(180, 180, 255))


def healing_plant(x, y):
    return Obstacle(x, y, damage=-15, blocking=False, color=(120, 255, 120), single_use=True)


def bouncy(x, y):
    return Obstacle(x, y, damage=0, blocking=False, color=(255, 150, 255), speed_mod=1.0)
