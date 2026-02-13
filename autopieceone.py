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

print(f"Physical mover started. Screen: {width}x{height}. Center: ({center_x}, {center_y})")
sys.stdout.flush()

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
                                else:
                                    # Press space to open chat
                                    pyautogui.press('space')
                                    time.sleep(1)
                                    
                                    # Use clipboard to paste (avoids emoji issues)
                                    pyperclip.copy(str(chat_data))
                                    pyautogui.hotkey('ctrl', 'v')
                                    
                                    # Press enter
                                    pyautogui.press('enter')
                except Exception as req_err:
                    print(f"Request failed or timed out: {req_err}")
                    sys.stdout.flush()
            
            # Sub-logic if random value < 0.5 (and >= 0.2): Drop Item
            elif sub_rand < 0.5:
                print(f"Action: Drop Item ({rand_val:.2f}, sub: {sub_rand:.2f})")
                sys.stdout.flush()
                
                # Pick random item first to log it
                drop_item = random.choice(AVAILABLE_DROPS)
                
                if IS_DEBUG:
                    print(f"[DEBUG] Would drop item: {drop_item}")
                else:
                    # Press space
                    pyautogui.press('space')
                    time.sleep(1)
                    
                    # Type "drop:" using keyboard
                    pyautogui.write("drop:")
                    time.sleep(0.3)
                    
                    # Use clipboard to paste item emoji
                    pyperclip.copy(drop_item)
                    pyautogui.hotkey('ctrl', 'v')
                    
                    # Press enter
                    pyautogui.press('enter')
                
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
