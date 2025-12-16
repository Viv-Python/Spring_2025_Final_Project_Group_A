#!/usr/bin/env python3
"""Generate a scary bear boss asset"""

import pygame
import os

def generate_scary_bear():
    """Generate a scary bear sprite with menacing features"""
    
    # Create surface for the bear (larger size for boss)
    size = 100
    bear_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Bear body - brown
    body_color = (139, 69, 19)  # Dark brown
    pygame.draw.ellipse(bear_surface, body_color, (15, 30, 70, 60))
    
    # Bear head - slightly darker
    head_color = (101, 50, 14)  # Darker brown
    pygame.draw.circle(bear_surface, head_color, (50, 25), 20)
    
    # Ears - pointy and menacing
    ear_color = (70, 35, 10)  # Very dark brown
    pygame.draw.polygon(bear_surface, ear_color, [(30, 5), (35, 15), (25, 18)])  # Left ear
    pygame.draw.polygon(bear_surface, ear_color, [(70, 5), (65, 15), (75, 18)])  # Right ear
    
    # Inner ear details
    pygame.draw.polygon(bear_surface, (255, 150, 100), [(31, 7), (33, 13), (28, 12)])  # Left inner ear
    pygame.draw.polygon(bear_surface, (255, 150, 100), [(69, 7), (67, 13), (72, 12)])  # Right inner ear
    
    # Snout - lighter brown
    snout_color = (160, 82, 45)
    pygame.draw.ellipse(bear_surface, snout_color, (35, 28, 30, 20))
    
    # Eyes - glowing red for scary effect
    pygame.draw.circle(bear_surface, (255, 0, 0), (42, 20), 4)  # Left eye
    pygame.draw.circle(bear_surface, (255, 0, 0), (58, 20), 4)  # Right eye
    
    # Eyes glare - brighter red dots
    pygame.draw.circle(bear_surface, (255, 100, 100), (43, 19), 2)  # Left eye glare
    pygame.draw.circle(bear_surface, (255, 100, 100), (59, 19), 2)  # Right eye glare
    
    # Nose - black
    pygame.draw.circle(bear_surface, (0, 0, 0), (50, 32), 3)
    
    # Mouth - scary grin
    mouth_color = (0, 0, 0)
    pygame.draw.line(bear_surface, mouth_color, (50, 32), (45, 38), 2)
    pygame.draw.line(bear_surface, mouth_color, (50, 32), (55, 38), 2)
    
    # Fangs - white sharp teeth
    fang_color = (255, 255, 255)
    pygame.draw.polygon(bear_surface, fang_color, [(45, 38), (43, 44), (47, 40)])  # Left fang
    pygame.draw.polygon(bear_surface, fang_color, [(55, 38), (57, 44), (53, 40)])  # Right fang
    
    # Front paws - large and menacing
    paw_color = (101, 50, 14)
    pygame.draw.ellipse(bear_surface, paw_color, (20, 70, 20, 25))  # Left paw
    pygame.draw.ellipse(bear_surface, paw_color, (60, 70, 20, 25))  # Right paw
    
    # Claws - dark and sharp
    claw_color = (20, 20, 20)
    for paw_x in [25, 65]:
        for claw_offset in [-5, 0, 5]:
            pygame.draw.polygon(bear_surface, claw_color, 
                              [(paw_x + claw_offset, 95), 
                               (paw_x + claw_offset - 2, 98), 
                               (paw_x + claw_offset + 2, 98)])
    
    # Spiky back/mane for scary effect
    spine_color = (60, 30, 0)
    for i in range(6):
        x = 20 + i * 12
        pygame.draw.polygon(bear_surface, spine_color, 
                          [(x, 30), (x - 3, 20), (x + 3, 20)])
    
    # Angry eyebrows
    pygame.draw.line(bear_surface, (0, 0, 0), (38, 18), (48, 16), 2)  # Left brow
    pygame.draw.line(bear_surface, (0, 0, 0), (52, 16), (62, 18), 2)  # Right brow
    
    return bear_surface


if __name__ == "__main__":
    pygame.init()
    
    # Create assets/enemies directory if it doesn't exist
    os.makedirs('assets/enemies', exist_ok=True)
    
    # Generate the bear
    bear_surface = generate_scary_bear()
    
    # Save as PNG
    output_path = 'assets/enemies/scary_bear.png'
    pygame.image.save(bear_surface, output_path)
    
    print(f"Scary bear asset generated: {output_path}")
    print(f"Image size: {bear_surface.get_size()}")
