"""
Asset loader module to handle loading and caching sprites throughout the game.
Provides functions to load player, enemy, obstacle, and tile sprites.
"""

import pygame
import os
from typing import Dict, Optional

class AssetLoader:
    """Manages loading and caching of all game assets"""
    
    def __init__(self):
        self.sprite_cache: Dict = {}
        self.animation_cache: Dict = {}
        self.asset_dir = 'assets'
        self.available = self._check_assets()
    
    def _check_assets(self) -> bool:
        """Check if assets directory and key files exist"""
        if not os.path.exists(self.asset_dir):
            return False
        
        key_assets = [
            'player/player_idle.png',
            'enemies/forest_creature.png',
            'obstacles/spike.png',
            'tiles/grass.png',
            'animations/player_walk_0.png',
            'animations/enemy_idle_0.png',
        ]
        
        for asset in key_assets:
            if not os.path.exists(os.path.join(self.asset_dir, asset)):
                return False
        
        return True
    
    def load_sprite(self, path: str) -> Optional[pygame.Surface]:
        """
        Load a sprite from disk and cache it.
        
        Args:
            path: Relative path to sprite file (relative to assets dir)
        
        Returns:
            Pygame Surface or None if load fails
        """
        if not self.available:
            return None
        
        full_path = os.path.join(self.asset_dir, path)
        
        # Check cache first
        if full_path in self.sprite_cache:
            return self.sprite_cache[full_path]
        
        # Try to load
        try:
            if not os.path.exists(full_path):
                print(f"Asset not found: {full_path}")
                return None
            
            # Load without convert_alpha to avoid "No video mode has been set" error
            # convert_alpha will be called when needed at runtime
            surface = pygame.image.load(full_path)
            if surface.get_colorkey() is None and surface.get_alpha() is None:
                # Only convert if not already in alpha mode
                surface = surface.convert_alpha()
            self.sprite_cache[full_path] = surface
            return surface
        except pygame.error as e:
            # Fallback: load without convert_alpha if video mode isn't set yet
            try:
                surface = pygame.image.load(full_path)
                self.sprite_cache[full_path] = surface
                return surface
            except Exception as inner_e:
                print(f"Error loading sprite {full_path}: {inner_e}")
                return None
        except Exception as e:
            print(f"Error loading sprite {full_path}: {e}")
            return None
    
    def load_animation(self, name_pattern: str, frames: int) -> Optional[list]:
        """
        Load an animation sequence (multiple frames).
        
        Args:
            name_pattern: Pattern like 'animations/player_walk' (frame number added)
            frames: Number of frames in animation
        
        Returns:
            List of pygame Surfaces or None if load fails
        """
        if not self.available:
            return None
        
        cache_key = f"{name_pattern}_{frames}"
        if cache_key in self.animation_cache:
            return self.animation_cache[cache_key]
        
        animation_frames = []
        for frame in range(frames):
            path = f"{name_pattern}_{frame}.png"
            surface = self.load_sprite(path)
            if surface is None:
                print(f"Failed to load animation frame: {path}")
                return None
            animation_frames.append(surface)
        
        self.animation_cache[cache_key] = animation_frames
        return animation_frames
    
    def get_player_idle(self) -> Optional[pygame.Surface]:
        """Get player idle sprite"""
        return self.load_sprite('player/player_idle.png')
    
    def get_player_walking(self) -> Optional[list]:
        """Get player walking animation frames"""
        return self.load_animation('animations/player_walk', 4)
    
    def get_player_running(self) -> Optional[list]:
        """Get player running animation frames"""
        return self.load_animation('animations/player_run', 4)
    
    def get_enemy_sprite(self, enemy_type: str = 'forest_creature') -> Optional[pygame.Surface]:
        """Get enemy sprite"""
        return self.load_sprite(f'enemies/{enemy_type}.png')
    
    def get_enemy_idle(self) -> Optional[list]:
        """Get enemy idle animation frames"""
        return self.load_animation('animations/enemy_idle', 4)
    
    def get_sword_swing(self) -> Optional[list]:
        """Get sword swing attack animation frames"""
        return self.load_animation('animations/sword_swing', 4)
    
    def get_sword_swing_left(self) -> Optional[list]:
        """Get sword swing left attack animation frames"""
        return self.load_animation('animations/sword_swing_left', 4)
    
    def get_obstacle_sprite(self, obstacle_type: str) -> Optional[pygame.Surface]:
        """Get obstacle sprite by type"""
        return self.load_sprite(f'obstacles/{obstacle_type}.png')
    
    def get_tile_sprite(self, tile_type: str) -> Optional[pygame.Surface]:
        """Get terrain tile sprite"""
        return self.load_sprite(f'tiles/{tile_type}.png')
    
    def scale_sprite(self, sprite: pygame.Surface, width: int, height: int) -> pygame.Surface:
        """
        Scale a sprite to specified dimensions.
        
        Args:
            sprite: Original pygame Surface
            width: Target width in pixels
            height: Target height in pixels
        
        Returns:
            Scaled pygame Surface
        """
        if sprite is None:
            return None
        return pygame.transform.scale(sprite, (width, height))

# Global asset loader instance
_loader: Optional[AssetLoader] = None

def get_loader() -> AssetLoader:
    """Get or create the global asset loader"""
    global _loader
    if _loader is None:
        _loader = AssetLoader()
    return _loader

def are_assets_available() -> bool:
    """Check if assets are available"""
    return get_loader().available
