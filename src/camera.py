import pygame
import math
from settings import WIDTH, HEIGHT, WHITE, GRAY

class Camera:
    """
    Camera system for vertical scrolling with smooth lerp and parallax support.
    
    This camera class handles:
    - Smooth vertical scrolling using linear interpolation (lerp)
    - Camera boundary constraints to prevent scrolling beyond level bounds
    - Parallax scrolling for background layers
    - Viewport culling to only render visible objects
    - Smooth following of the player with configurable behavior
    """
    
    def __init__(self, level_width=800, level_height=2400, 
                 screen_width=WIDTH, screen_height=HEIGHT,
                 smooth_enabled=True, smooth_factor=0.1):
        """
        Initialize the camera.
        
        Args:
            level_width: Total width of the level in pixels
            level_height: Total height of the level in pixels
            screen_width: Width of the visible viewport
            screen_height: Height of the visible viewport
            smooth_enabled: Whether to use smooth scrolling (lerp)
            smooth_factor: Lerp factor (0.0-1.0), lower = smoother
        """
        self.level_width = level_width
        self.level_height = level_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Camera position (top-left corner of visible area)
        self.x = 0.0
        self.y = 0.0
        
        # Target position for smooth scrolling
        self.target_x = 0.0
        self.target_y = 0.0
        
        # Smooth scrolling settings
        self.smooth_enabled = smooth_enabled
        self.smooth_factor = smooth_factor
        
        # Player tracking settings
        self.player_offset_y = 0.3  # Keep player at 30% from top of screen
        self.deadzone_height = 100   # Vertical deadzone where camera doesn't move

    def update(self, player_rect):
        """
        Update camera position based on player location.
        
        Args:
            player_rect: pygame.Rect of the player
        """
        # Calculate target position to keep player near center
        # Player should be at (screen_height * player_offset_y) from top
        target_y = player_rect.centery - (self.screen_height * self.player_offset_y)
        
        # Apply deadzone - camera doesn't move if player is within this zone
        if abs(target_y - self.target_y) > self.deadzone_height:
            self.target_y = target_y
        
        # Apply smooth scrolling (lerp)
        if self.smooth_enabled:
            self.y = self._lerp(self.y, self.target_y, self.smooth_factor)
        else:
            self.y = self.target_y
        
        # Clamp camera to level boundaries
        self._clamp_to_boundaries()

    def _lerp(self, start, end, factor):
        """
        Linear interpolation between two values.
        
        Args:
            start: Starting value
            end: Target value
            factor: Interpolation factor (0.0-1.0)
        
        Returns:
            Interpolated value
        """
        return start + (end - start) * factor

    def _clamp_to_boundaries(self):
        """
        Ensure camera doesn't scroll beyond level boundaries.
        Camera should never show empty space beyond level edges.
        """
        # Clamp horizontal (if needed for future horizontal scrolling)
        if self.x < 0:
            self.x = 0
        if self.x + self.screen_width > self.level_width:
            self.x = self.level_width - self.screen_width
        
        # Clamp vertical - most important for vertical scrolling
        if self.y < 0:
            self.y = 0
        if self.y + self.screen_height > self.level_height:
            self.y = self.level_height - self.screen_height

    def apply_offset(self, rect):
        """
        Apply camera offset to a rect for drawing.
        Returns a new rect with adjusted position for screen rendering.
        
        Args:
            rect: pygame.Rect to offset
        
        Returns:
            New pygame.Rect with camera offset applied
        """
        offset_rect = rect.copy()
        offset_rect.x -= int(self.x)
        offset_rect.y -= int(self.y)
        return offset_rect

    def apply_offset_pos(self, x, y):
        """
        Apply camera offset to x, y coordinates.
        
        Args:
            x, y: Coordinates to offset
        
        Returns:
            Tuple of (offset_x, offset_y)
        """
        return (int(x - self.x), int(y - self.y))

    def is_visible(self, rect):
        """
        Check if a rect is visible in the current viewport (with some margin).
        Useful for culling objects that shouldn't be rendered.
        
        Args:
            rect: pygame.Rect to check
        
        Returns:
            True if rect is visible or partially visible, False otherwise
        """
        # Add margin for safety (some objects might be just outside but affect gameplay)
        margin = 100
        viewport_rect = pygame.Rect(
            int(self.x) - margin,
            int(self.y) - margin,
            self.screen_width + margin * 2,
            self.screen_height + margin * 2
        )
        return rect.colliderect(viewport_rect)

    def get_visible_sprites(self, sprite_group):
        """
        Filter sprite group to only visible sprites (culling for optimization).
        
        Args:
            sprite_group: pygame.sprite.Group to filter
        
        Returns:
            List of visible sprites
        """
        return [sprite for sprite in sprite_group 
                if self.is_visible(sprite.rect)]

    def draw_parallax_background(self, surface, layers=None):
        """
        Draw parallax scrolling background layers.
        Creates visual depth by moving background at different speeds.
        
        Args:
            surface: Pygame surface to draw on
            layers: List of dicts with keys:
                   - 'color': RGB tuple
                   - 'depth': float (0.0-1.0), lower = further away, slower movement
                   - 'offset_y': optional starting y offset
        """
        if layers is None:
            # Default parallax layers
            layers = [
                {'color': (50, 30, 60), 'depth': 0.1},    # Far background
                {'color': (80, 50, 100), 'depth': 0.3},   # Mid background
                {'color': (120, 70, 140), 'depth': 0.6},  # Near background
            ]
        
        for layer in layers:
            color = layer['color']
            depth = layer['depth']
            
            # Calculate parallax offset - multiply camera y by depth factor
            parallax_y = int(self.y * depth)
            
            # Draw multiple sections to handle wrapping
            section_height = self.screen_height
            
            # Calculate which section we're in
            section_offset = parallax_y % section_height
            
            # Draw the current section and wrap around
            surface.fill(color, (0, 0, self.screen_width, section_height))
            
            # Optional: Draw pattern or texture on background
            # This creates visual interest without much performance cost
            if depth == 0.1:  # Farthest layer - draw stars
                pygame.draw.line(surface, (255, 255, 255), 
                               (100, 50), (150, 50), 2)
            elif depth == 0.3:  # Mid layer - draw clouds
                pygame.draw.circle(surface, (200, 200, 200), (100, 100), 30)
            
            # Important: draw only once per update since parallax is pre-calculated
            break  # For now, use simple background - expand this for visual polish

    def reset(self):
        """Reset camera to origin"""
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0

    def set_smooth_enabled(self, enabled):
        """Enable or disable smooth scrolling"""
        self.smooth_enabled = enabled

    def set_smooth_factor(self, factor):
        """Set smooth scrolling factor (0.0-1.0)"""
        self.smooth_factor = max(0.0, min(1.0, factor))

    def set_player_tracking(self, offset_y, deadzone_height):
        """
        Configure how the camera tracks the player.
        
        Args:
            offset_y: Vertical position where player should appear (0.0-1.0)
            deadzone_height: Pixels of vertical deadzone before camera moves
        """
        self.player_offset_y = max(0.0, min(1.0, offset_y))
        self.deadzone_height = deadzone_height

    def get_info(self):
        """
        Get debug information about camera state.
        
        Returns:
            String with camera information
        """
        return (f"Camera Y: {self.y:.1f} | Target Y: {self.target_y:.1f} | "
                f"Level Height: {self.level_height} | "
                f"Visible: ({int(self.y)}, {int(self.y + self.screen_height)})")
