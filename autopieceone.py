import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pyautogui
import pyperclip
import time
import math
import random
import urllib.request
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get name from command line argument (default: 大钳子)
NAME = sys.argv[1] if len(sys.argv) > 1 else "大钳子"

# Fail-safe: move mouse to corner of screen to abort
pyautogui.FAILSAFE = True

# Debug mode: If True, simulate actions with logs instead of executing
IS_DEBUG = os.getenv("IS_DEBUG", "false").lower() == "true"

AVAILABLE_DROPS = ['🍔','🍕','🍦','🍩','🍪','🍟','🎂','🍰','🧀','🍖','🍗','🥩','🍿','🍘','🍙','🍢','🍣','🍤','🥮','🥟','🧁','🍫','🍬','🍆','🥔','🥕','🌽','🌶️','🫑','🥒','🥬','🥦','🧄','🧅','🥜','🫘','🌰','🫛','🍠','🍇','🍈','🍉','🍊','🍋','🍋‍🟩','🍌','🍍','🥭','🍎','🍏','🍐','🍑','🍒','🍓','🫐','🥝','🍅','🫒','🥑','🍞','🥐','🥖','🥨','🥯','🥞','🧇','🥪','🌭','🌮','🌯','🫔','🥛','☕️','🍵','🍶','🍷','🍸️','🍹','🍺','🥃','🥤','🧋','🧃','🧉','⚽️','🏀','🥎','🎾','🏐','⚾️','🏈','🏉','🎱','🎲','🃏','🪨','🕸','🎈','🎉','🎆','🎇','🧨','💣','🎨','🎭️','🧊','💩','🕳️','💊','🧲','🍄','🎃','🐵','🐶','🦊','🐱','🦁','🐯','🐷','🐭','🐹','🐰','🐻','🐨','🐼','🐸','🐲','🐽','🌚','🌝','🌞','🤡','🤖','💀','👹','👻','🐮','🧢','👓','🕶️','🎩','🪖','🤿','🐽','🌪️','🪺']

# Global execution interval in seconds
EXECUTION_INTERVAL = 5.0

width, height = pyautogui.size()
center_x, center_y = width // 2, height // 2
radius = 150

print(f"Physical mover started. Screen: {width}x{height}. Center: ({center_x}, {center_y}), Name: {NAME}")
sys.stdout.flush()

# First action: set name
print(f"Action: Setting name to {NAME}")
sys.stdout.flush()
if not IS_DEBUG:
    pyperclip.copy(f"name:{NAME}")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)

# Track last action to prevent consecutive same actions
last_action_type = None

while True:
    try:
        rand_val = random.random()
        
        # 1. Logic if random value < 0.3: Move and Click (0.5s - 2s)
        if rand_val < 0.3:
            angle = random.uniform(0, 2 * math.pi)
            tx = center_x + radius * math.cos(angle)
            ty = center_y + radius * math.sin(angle)
            
            print(f"Action: Move & Click ({rand_val:.2f})")
            sys.stdout.flush()
            
            if IS_DEBUG:
                print(f"[DEBUG] Would move to ({tx:.0f}, {ty:.0f}), hold left click.")
                
                # Simulate hold duration in debug? Maybe just log duration.
                hold_time = random.uniform(0.5, 2.0)
                print(f"[DEBUG] maintain click for {hold_time:.2f}s")
            else:
                # Move mouse
                pyautogui.moveTo(tx, ty, duration=0.5)
                
                # Click and hold
                pyautogui.mouseDown(button='left')
                hold_time = random.uniform(0.5, 2.0)
                time.sleep(hold_time)
                pyautogui.mouseUp(button='left')
            
        # 2. Logic if random value < 0.6: Only Move
        elif rand_val < 0.6:
            angle = random.uniform(0, 2 * math.pi)
            tx = center_x + radius * math.cos(angle)
            ty = center_y + radius * math.sin(angle)
            
            print(f"Action: Move Only ({rand_val:.2f})")
            sys.stdout.flush()
            
            if IS_DEBUG:
                print(f"[DEBUG] Would move to ({tx:.0f}, {ty:.0f}) without clicking.")
            else:
                # Move mouse
                pyautogui.moveTo(tx, ty, duration=0.5)
            
        # 3. Logic if random value >= 0.6: Chat API Logic
        else:
            sub_rand = random.random()
            if sub_rand < 0.2:
                # Check consecutive action
                if last_action_type == "chat":
                    print(f"Action: Skipped Chat (consecutive) ({rand_val:.2f}, sub: {sub_rand:.2f})")
                    sys.stdout.flush()
                    last_action_type = None  # Reset or leave as is? Let's leave as is so it doesn't loop
                    # If user wants to skip, we just do nothing and wait
                    time.sleep(0.5)
                else:
                    print(f"Action: Chat Input ({rand_val:.2f}, sub: {sub_rand:.2f})")
                    sys.stdout.flush()
                    
                    try:
                        # Request with 5s timeout and User-Agent to avoid 403
                        req = urllib.request.Request(
                            "https://api.piece.one/chat.php", 
                            headers={'User-Agent': 'Mozilla/5.0'}
                        )
                        with urllib.request.urlopen(req, timeout=5) as response:
                            if response.status == 200:
                                content = response.read().decode('utf-8')
                                data_json = json.loads(content)
                                chat_data = data_json.get('data', '')
                                
                                if chat_data:
                                    if IS_DEBUG:
                                        print(f"[DEBUG] Got chat data: '{chat_data}'. Would type it.")
                                        last_action_type = "chat"
                                    else:
                                        # Press space to open chat
                                        pyautogui.press('space')
                                        time.sleep(1)
                                        
                                        # Use clipboard to paste (avoids emoji issues)
                                        pyperclip.copy(str(chat_data))
                                        pyautogui.hotkey('ctrl', 'v')
                                        
                                        # Press enter
                                        pyautogui.press('enter')
                                        
                                        # Update last action
                                        last_action_type = "chat"
                    except Exception as req_err:
                        print(f"Request failed or timed out: {req_err}")
                        sys.stdout.flush()
            
            # Sub-logic if random value < 0.5 (and >= 0.2): Drop Item
            elif sub_rand < 0.5:
                # Check consecutive action
                if last_action_type == "drop":
                    print(f"Action: Skipped Drop (consecutive) ({rand_val:.2f}, sub: {sub_rand:.2f})")
                    sys.stdout.flush()
                    time.sleep(0.5)
                else:
                    print(f"Action: Drop Item ({rand_val:.2f}, sub: {sub_rand:.2f})")
                    sys.stdout.flush()
                    
                    # Pick random item first to log it
                    drop_item = random.choice(AVAILABLE_DROPS)
                    
                    if IS_DEBUG:
                        print(f"[DEBUG] Would drop item: {drop_item}")
                        last_action_type = "drop"
                    else:
                        # Press space
                        pyautogui.press('space')
                        time.sleep(1)
                        
                        # Use clipboard to paste item emoji
                        pyperclip.copy("drop:" + drop_item)
                        pyautogui.hotkey('ctrl', 'v')
                        
                        # Press enter
                        pyautogui.press('enter')
                        
                        # Update last action
                        last_action_type = "drop"
                
            # Sub-logic if random value < 0.7 (and >= 0.5): Color Command
            elif sub_rand < 0.7:
                # Check consecutive action
                if last_action_type == "color":
                    print(f"Action: Skipped Color (consecutive) ({rand_val:.2f}, sub: {sub_rand:.2f})")
                    sys.stdout.flush()
                    time.sleep(0.5)
                else:
                    color_hex = f"#{random.randint(0, 0xFFFFFF):06x}"
                    print(f"Action: Color Command ({rand_val:.2f}, sub: {sub_rand:.2f}) -> {color_hex}")
                    sys.stdout.flush()
                    
                    if IS_DEBUG:
                        print(f"[DEBUG] Would send color: {color_hex}")
                        last_action_type = "color"
                    else:
                        # Press space
                        pyautogui.press('space')
                        time.sleep(1)
                        
                        # Use clipboard to paste color command
                        pyperclip.copy(f"color: {color_hex}")
                        pyautogui.hotkey('ctrl', 'v')
                        
                        # Press enter
                        pyautogui.press('enter')
                        
                        # Update last action
                        last_action_type = "color"
                
            else:
                # Placeholder for other sub-cases in >= 0.6
                print(f"Action: Skipped > 0.6 ({rand_val:.2f}, sub: {sub_rand:.2f})")
                sys.stdout.flush()
                # Default wait
                time.sleep(0.5)
        
        # Wait for the next execution interval
        time.sleep(EXECUTION_INTERVAL)
    except Exception as e:
        print(f"Stopped: {e}")
        sys.stdout.flush()
        break
