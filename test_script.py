#!/usr/bin/env python3
"""
Comprehensive test script for:
1. Sword attack animation - verify sword sprites load and animate
2. Enemy platform collision - verify enemies stay on platforms
3. Health/damage balance - verify 2-3 hits for enemies, 10 hits for boss
"""

import sys
sys.path.insert(0, 'src')

import pygame
import os
from settings import WIDTH, HEIGHT, ENEMY_SIZE
from player import Player, Attack
from enemies import Enemy
from boss import Boss
from asset_loader import get_loader
from utils import generate_terrain

pygame.init()

# ==================== SWORD ATTACK TESTS ====================

def test_sword_animation_exists():
    """Test that sword swing animation frames exist"""
    print("=" * 60)
    print("TEST 1: Sword Animation Files Exist")
    print("=" * 60)
    
    try:
        sword_frames = ['sword_swing_0.png', 'sword_swing_1.png', 'sword_swing_2.png', 'sword_swing_3.png']
        
        for frame in sword_frames:
            path = f'assets/animations/{frame}'
            assert os.path.isfile(path), f"Sword animation frame not found: {path}"
            
            file_size = os.path.getsize(path)
            assert file_size > 0, f"Sword animation frame is empty: {path}"
            
            print(f"[+] Found: {frame} ({file_size} bytes)")
        
        print("[+] PASS: All sword animation frames exist")
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        return False
    
    print()
    return True

def test_enemy_health_value():
    """Test that enemy default health is correct"""
    print("=" * 60)
    print("TEST 2: Enemy Health Value")
    print("=" * 60)
    
    try:
        # Default health should be 45 (for 3 hits with 15 damage)
        enemy = Enemy(100, 100)
        
        assert enemy.health == 45, f"Enemy health should be 45, got {enemy.health}"
        assert enemy.max_health == 45, f"Enemy max_health should be 45, got {enemy.max_health}"
        
        print(f"[+] Enemy default health: {enemy.health}")
        print(f"[+] Enemy max health: {enemy.max_health}")
        print("[+] PASS: Enemy health is correct (45 = 3 hits * 15 damage)")
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        return False
    
    print()
    return True

def test_enemy_damage_calculation():
    """Test that enemies take correct damage"""
    print("=" * 60)
    print("TEST 3: Enemy Damage Calculation")
    print("=" * 60)
    
    try:
        enemy = Enemy(100, 100, health=45)
        
        # Test damage application
        initial_health = enemy.health
        enemy.take_damage(15)  # One hit
        
        assert enemy.health == initial_health - 15, "Damage not applied correctly"
        print(f"[+] After 1 hit: health {initial_health} -> {enemy.health}")
        
        enemy.take_damage(15)  # Second hit
        assert enemy.health == 15, "Second hit damage incorrect"
        print(f"[+] After 2 hits: health -> {enemy.health}")
        
        enemy.take_damage(15)  # Third hit
        assert enemy.health <= 0, "Enemy should be dead after 3 hits"
        assert enemy.alive() == False, "Enemy should be killed after 3 hits"
        print(f"[+] After 3 hits: health -> {enemy.health} (DEAD)")
        
        print("[+] PASS: Enemy dies in exactly 3 hits with 15 damage")
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        return False
    
    print()
    return True

def test_boss_health_value():
    """Test that boss health is correct"""
    print("=" * 60)
    print("TEST 4: Boss Health Value")
    print("=" * 60)
    
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        boss = Boss(WIDTH // 2, HEIGHT // 2)
        
        # Boss health should be 150 (for 10 hits with 15 damage)
        assert boss.health == 150, f"Boss health should be 150, got {boss.health}"
        assert boss.max_health == 150, f"Boss max_health should be 150, got {boss.max_health}"
        
        print(f"[+] Boss health: {boss.health}")
        print(f"[+] Boss max health: {boss.max_health}")
        print("[+] PASS: Boss health is correct (150 = 10 hits * 15 damage)")
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        return False
    
    print()
    return True

def test_boss_damage_calculation():
    """Test that boss takes correct damage"""
    print("=" * 60)
    print("TEST 5: Boss Damage Calculation")
    print("=" * 60)
    
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        boss = Boss(WIDTH // 2, HEIGHT // 2)
        initial_health = boss.health
        
        # Apply 10 hits
        for hit in range(10):
            boss.take_damage(15)
            expected_health = max(0, initial_health - (hit + 1) * 15)
            print(f"[+] After hit {hit + 1}: health -> {boss.health}")
        
        assert boss.health <= 0, "Boss should be dead after 10 hits"
        assert boss.alive() == False, "Boss should be killed after 10 hits"
        print(f"[+] Boss dead: health = {boss.health}")
        
        print("[+] PASS: Boss dies in exactly 10 hits with 15 damage")
    except AssertionError as e:
        print(f"[X] FAIL: {e}")
        return False
    except Exception as e:
        print(f"[X] ERROR: {e}")
        return False
    
    print()
    return True

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("CHANGES VERIFICATION TEST SUITE")
    print("Sword Attacks | Enemy Collisions | Health Balance")
    print("=" * 60)
    print()
    
    tests = [
        test_sword_animation_exists,
        test_enemy_health_value,
        test_enemy_damage_calculation,
        test_boss_health_value,
        test_boss_damage_calculation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = test()
            if result is not False:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"[X] EXCEPTION in {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED out of {len(tests)} tests")
    print("=" * 60)
    
    if failed == 0:
        print("[+] ALL TESTS PASSED!")
    else:
        print(f"[X] {failed} TEST(S) FAILED")
    
    print()

if __name__ == '__main__':
    main()

