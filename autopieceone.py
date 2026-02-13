import pyautogui
import time
import math
import random
import sys
import urllib.request
import json

# Fail-safe: move mouse to corner of screen to abort
pyautogui.FAILSAFE = True

AVAILABLE_DROPS = ['🍔','🍕','🍦','🍩','🍪','🍟','🎂','🍰','🧀','🍖','🍗','🥩','🍿','🍘','🍙','🍢','🍣','🍤','🥮','🥟','🧁','🍫','🍬','🍆','🥔','🥕','🌽','🌶️','🫑','🥒','🥬','🥦','🧄','🧅','🥜','🫘','🌰','🫛','🍠','🍇','🍈','🍉','🍊','🍋','🍋‍🟩','🍌','🍍','🥭','🍎','🍏','🍐','🍑','🍒','🍓','🫐','🥝','🍅','🫒','🥑','🍞','🥐','🥖','🥨','🥯','🥞','🧇','🥪','🌭','🌮','🌯','🫔','🥛','☕️','🍵','🍶','🍷','🍸️','🍹','🍺','🥃','🥤','🧋','🧃','🧉','⚽️','🏀','🥎','🎾','🏐','⚾️','🏈','🏉','🎱','🎲','🃏','🪨','🕸','🎈','🎉','🎆','🎇','🧨','💣','🎨','🎭️','🧊','💩','🕳️','💊','🧲','🍄','🎃','🐵','🐶','🦊','🐱','🦁','🐯','🐷','🐭','🐹','🐰','🐻','🐨','🐼','🐸','🐲','🐽','🌚','🌝','🌞','🤡','🤖','💀','👹','👻','🐮','🧢','👓','🕶️','🎩','🪖','🤿','🐽','🌪️','🪺']

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
            
            # Move mouse
            pyautogui.moveTo(tx, ty, duration=0.5)
            
        # 3. Logic if random value >= 0.6: Chat API Logic
        else:
            sub_rand = random.random()
            if sub_rand < 0.2:
                print(f"Action: Chat Input ({rand_val:.2f}, sub: {sub_rand:.2f})")
                sys.stdout.flush()
                
                try:
                    # Request with 5s timeout
                    with urllib.request.urlopen("https://api.piece.one/chat.php", timeout=5) as response:
                        if response.status == 200:
                            content = response.read().decode('utf-8')
                            data_json = json.loads(content)
                            chat_data = data_json.get('data', '')
                            
                            if chat_data:
                                # Press space
                                pyautogui.press('space')
                                time.sleep(1)
                                
                                # Input data
                                pyautogui.write(str(chat_data))
                                
                                # Press enter
                                pyautogui.press('enter')
                except Exception as req_err:
                    print(f"Request failed or timed out: {req_err}")
                    sys.stdout.flush()
            
            # Sub-logic if random value < 0.5 (and >= 0.2): Drop Item
            elif sub_rand < 0.5:
                print(f"Action: Drop Item ({rand_val:.2f}, sub: {sub_rand:.2f})")
                sys.stdout.flush()
                
                # Press space
                pyautogui.press('space')
                time.sleep(1)
                
                # Type "drop:"
                pyautogui.write("drop:")
                
                # Pick random item
                drop_item = random.choice(AVAILABLE_DROPS)
                pyautogui.write(drop_item)
                
                # Press enter
                pyautogui.press('enter')
                
            else:
                # Placeholder for other sub-cases in >= 0.6
                print(f"Action: Skipped > 0.6 ({rand_val:.2f}, sub: {sub_rand:.2f})")
                sys.stdout.flush()
                # Default wait
                time.sleep(0.5)
        
        # Small pause between actions
        time.sleep(0.5)
    except Exception as e:
        print(f"Stopped: {e}")
        sys.stdout.flush()
        break
