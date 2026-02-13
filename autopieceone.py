import pyautogui
import time
import math
import random
import sys

# Fail-safe: move mouse to corner of screen to abort
pyautogui.FAILSAFE = True

width, height = pyautogui.size()
center_x, center_y = width // 2, height // 2
radius = 150

print(f"Physical mover started. Screen: {width}x{height}. Center: ({center_x}, {center_y})")
sys.stdout.flush()

while True:
    try:
        rand_val = random.random()
        
        # Only execute if random value > 0.5
        if rand_val > 0.5:
            angle = random.uniform(0, 2 * math.pi)
            tx = center_x + radius * math.cos(angle)
            ty = center_y + radius * math.sin(angle)
            
            # 1. Move mouse to target coordinate
            pyautogui.moveTo(tx, ty, duration=0.5)
            
            # 2. Press and hold left button for 2 seconds
            pyautogui.mouseDown(button='left')
            time.sleep(2)
            pyautogui.mouseUp(button='left')
        else:
            # Do nothing, just wait
            print(f"Skipped (random: {rand_val:.2f})")
            sys.stdout.flush()
        
        # 3. Small pause between movements
        time.sleep(0.5)
    except Exception as e:
        print(f"Stopped: {e}")
        sys.stdout.flush()
        break
