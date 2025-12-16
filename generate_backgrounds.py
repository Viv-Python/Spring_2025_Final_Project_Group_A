#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate background images for game levels
"""

from PIL import Image, ImageDraw
import random
import os

WIDTH, HEIGHT = 800, 600

def generate_swamp_background(width=WIDTH, height=HEIGHT):
    """Generate a swamp background with murky water, vegetation, and trees"""
    img = Image.new('RGB', (width, height), color=(60, 80, 40))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Water/ground base gradient effect
    for y in range(height):
        color_val = int(60 + (y / height) * 40)
        green = int(80 + (y / height) * 50)
        draw.line([(0, y), (width, y)], fill=(color_val, green, 40))
    
    # Draw some water patches
    random.seed(42)
    for i in range(15):
        x = random.randint(0, width)
        y = random.randint(height // 2, height)
        size = random.randint(40, 120)
        # Water patches
        draw.ellipse([x, y, x + size, y + size // 2], fill=(40, 60, 30, 80))
    
    # Draw vegetation/cattails
    for i in range(30):
        x = random.randint(0, width)
        y = random.randint(height // 2, height - 50)
        # Draw cattail-like vegetation
        for dy in range(0, 80, 10):
            draw.line([(x, y + dy), (x - 3, y + dy + 5)], fill=(50, 100, 30), width=2)
            draw.line([(x, y + dy), (x + 3, y + dy + 5)], fill=(50, 100, 30), width=2)
    
    # Add some "fog" effect with semi-transparent rectangles
    for i in range(5):
        y = random.randint(100, height - 100)
        draw.rectangle([0, y, width, y + 40], fill=(100, 120, 80, 40))
    
    return img

def generate_jungle_background(width=WIDTH, height=HEIGHT):
    """Generate a jungle background with dense vegetation and vines"""
    img = Image.new('RGB', (width, height), color=(80, 120, 60))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient from darker top to lighter bottom
    for y in range(height):
        green = int(80 + (y / height) * 60)
        draw.line([(0, y), (width, y)], fill=(40, green, 30))
    
    # Draw tree trunks
    random.seed(42)
    for i in range(10):
        x = random.randint(50, width - 50)
        trunk_width = random.randint(30, 60)
        trunk_height = random.randint(200, height - 100)
        # Trunk
        draw.rectangle([x - trunk_width // 2, height - trunk_height, 
                       x + trunk_width // 2, height], fill=(80, 50, 20))
        # Canopy circles
        canopy_color = (60, 140, 40)
        for dy in range(0, trunk_height, 40):
            cy = height - trunk_height + dy
            cx = x
            canopy_radius = random.randint(60, 100)
            draw.ellipse([cx - canopy_radius, cy - canopy_radius, 
                         cx + canopy_radius, cy + canopy_radius], fill=canopy_color)
    
    # Draw vines
    for i in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height - 200)
        # Wavy vine
        for dy in range(0, 200, 10):
            x_offset = random.randint(-5, 5)
            draw.line([(x + x_offset, y + dy), (x + x_offset + 3, y + dy + 10)], 
                     fill=(50, 120, 30), width=2)
    
    return img

def generate_forest_background(width=WIDTH, height=HEIGHT):
    """Generate a forest background with tall trees and undergrowth"""
    img = Image.new('RGB', (width, height), color=(40, 80, 30))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient from lighter sky-top to darker ground-bottom
    for y in range(height):
        if y < height // 3:
            color_val = int(40 + (y / (height // 3)) * 20)
            green = int(80 + (y / (height // 3)) * 30)
        else:
            color_val = 60 + random.randint(-10, 10)
            green = 110 + random.randint(-10, 10)
        draw.line([(0, y), (width, y)], fill=(color_val, green, 20))
    
    # Draw evergreen trees (triangular shape)
    random.seed(42)
    for i in range(12):
        x = random.randint(30, width - 30)
        y = random.randint(50, height - 100)
        tree_height = random.randint(150, 300)
        tree_width = tree_height // 2
        
        # Tree trunk
        draw.rectangle([x - 10, y + tree_height - 30, x + 10, y + tree_height], 
                      fill=(101, 67, 33))
        
        # Tree foliage (multiple triangles)
        for layer in range(3):
            layer_y = y - (layer * tree_height // 3)
            layer_width = tree_width - (layer * 10)
            draw.polygon([(x, layer_y), (x - layer_width, layer_y + 60), 
                         (x + layer_width, layer_y + 60)], fill=(34, 120, 34))
    
    # Add some undergrowth bushes
    for i in range(25):
        x = random.randint(0, width)
        y = random.randint(height - 150, height - 50)
        size = random.randint(20, 50)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=(50, 100, 40))
    
    return img

def generate_cave_background(width=WIDTH, height=HEIGHT):
    """Generate a cave background with dark stone walls and stalagmites"""
    img = Image.new('RGB', (width, height), color=(50, 50, 50))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient from slightly lighter walls to darker ground
    for y in range(height):
        gray = int(50 + (y / height) * 30)
        draw.line([(0, y), (width, y)], fill=(gray, gray, gray - 10))
    
    # Draw stalagmites from bottom
    random.seed(42)
    for i in range(8):
        x = random.randint(50, width - 50)
        height_var = random.randint(100, 250)
        width_var = random.randint(30, 80)
        
        # Stalagmite shape (inverted triangle from bottom)
        points = [
            (x - width_var // 2, height),
            (x, height - height_var),
            (x + width_var // 2, height)
        ]
        draw.polygon(points, fill=(60, 60, 60))
        # Add some texture
        draw.polygon([(x - width_var // 3, height - height_var // 3),
                     (x, height - height_var),
                     (x + width_var // 3, height - height_var // 3)], 
                    fill=(70, 70, 70))
    
    # Draw stalactites from ceiling
    for i in range(8):
        x = random.randint(50, width - 50)
        height_var = random.randint(80, 180)
        width_var = random.randint(20, 50)
        
        # Stalactite shape (triangle from top)
        points = [
            (x - width_var // 2, 0),
            (x, height_var),
            (x + width_var // 2, 0)
        ]
        draw.polygon(points, fill=(55, 55, 55))
    
    # Add crystalline formations
    for i in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(3, 8)
        draw.polygon([(x, y - size), (x + size, y), (x, y + size), (x - size, y)], 
                    fill=(100, 100, 120))
    
    # Add some luminescent glow spots
    for i in range(5):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        # Glow effect with semi-transparent circles
        draw.ellipse([x - 30, y - 30, x + 30, y + 30], fill=(150, 150, 200, 30))
        draw.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(180, 180, 220, 40))
    
    return img

def main():
    """Generate and save all background images"""
    backgrounds = {
        'swamp.png': generate_swamp_background(),
        'jungle.png': generate_jungle_background(),
        'forest.png': generate_forest_background(),
        'cave.png': generate_cave_background(),
    }
    
    output_dir = 'assets/backgrounds'
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, img in backgrounds.items():
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        print(f"[+] Generated background: {filepath}")
    
    print("[+] All backgrounds generated successfully!")

if __name__ == '__main__':
    main()
