import pygame
from settings import GREEN
from asset_loader import get_loader

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        # Try to load and tile grass texture
        loader = get_loader()
        grass_sprite = loader.get_tile_sprite('grass')
        
        if grass_sprite is not None:
            # Create a tiled surface using the grass texture
            self.image = pygame.Surface((width, height))
            tile_size = 64
            for tx in range(0, width, tile_size):
                for ty in range(0, height, tile_size):
                    # Draw grass tile
                    scaled_tile = pygame.transform.scale(grass_sprite, 
                                                        (min(tile_size, width - tx), 
                                                         min(tile_size, height - ty)))
                    self.image.blit(scaled_tile, (tx, ty))
        else:
            # Fallback: use solid green color
            self.image = pygame.Surface((width, height))
            self.image.fill(GREEN)
        
        self.rect = self.image.get_rect(topleft=(x, y))
