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
import atexit
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cleanup: release mouse button on exit
def cleanup():
    try:
        pyautogui.mouseUp(button='left')
        print("Cleanup: mouse button released")
    except:
        pass

atexit.register(cleanup)

# Get name from command line argument (default: 大钳子)
NAME = sys.argv[1] if len(sys.argv) > 1 else "大钳子"

# Fail-safe: move mouse to corner of screen to abort
pyautogui.FAILSAFE = True

# Debug mode: If True, simulate actions with logs instead of executing
IS_DEBUG = os.getenv("IS_DEBUG", "false").lower() == "true"

# Stop flag file - if this exists, script will not auto-restart
STOP_FLAG_FILE = "stop.flag"

AVAILABLE_DROPS = ['🍔','🍕','🍦','🍩','🍪','🍟','🎂','🍰','🧀','🍖','🍗','🥩','🍿','🍘','🍙','🍢','🍣','🍤','🥮','🥟','🧁','🍫','🍬','🍆','🥔','🥕','🌽','🌶️','🫑','🥒','🥬','🥦','🧄','🧅','🥜','🫘','🌰','🫛','🍠','🍇','🍈','🍉','🍊','🍋','🍋‍🟩','🍌','🍍','🥭','🍎','🍏','🍐','🍑','🍒','🍓','🫐','🥝','🍅','🫒','🥑','🍞','🥐','🥖','🥨','🥯','🥞','🧇','🥪','🌭','🌮','🌯','🫔','🥛','☕️','🍵','🍶','🍷','🍸️','🍹','🍺','🥃','🥤','🧋','🧃','🧉','⚽️','🏀','🥎','🎾','🏐','⚾️','🏈','🏉','🎱','🎲','🃏','🪨','🕸','🎈','🎉','🎆','🎇','🧨','💣','🎨','🎭️','🧊','💩','🕳️','💊','🧲','🍄','🎃','🐵','🐶','🦊','🐱','🦁','🐯','🐷','🐭','🐹','🐰','🐻','🐨','🐼','🐸','🐲','🐽','🌚','🌝','🌞','🤡','🤖','💀','👹','👻','🐮','🧢','👓','🕶️','🎩','🪖','🤿','🐽','🌪️','🪺']

# Global execution interval in seconds
EXECUTION_INTERVAL = 5.0

# Refresh browser every 10 minutes (600 seconds)
REFRESH_INTERVAL = 600

# Track last refresh time
last_refresh_time = time.time()

width, height = pyautogui.size()
center_x, center_y = width // 2, height // 2
radius = 300

print(f"Physical mover started. Screen: {width}x{height}. Center: ({center_x}, {center_y}), Name: {NAME}")
sys.stdout.flush()

# First action
sys.stdout.flush()
if not IS_DEBUG:
    pyautogui.press('space')
    pyperclip.copy(f"name:{NAME}")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
else:
    print(f"Action: Setting name to {NAME}")
    sys.stdout.flush()

time.sleep(1)

if not IS_DEBUG:
    pyautogui.press('space')
    pyperclip.copy(f"color:#BB2521")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)
else:
    print(f"Action: Setting color to #BB2521")
    sys.stdout.flush()

# Helper: Send Message to Chat
def send_chat_msg(message):
    if IS_DEBUG:
        print(f"[DEBUG] Would send to chat: {message}")
        return

    # Press space to open chat
    pyautogui.press('space')
    time.sleep(1)

    # Use clipboard to paste
    pyperclip.copy(str(message))
    pyautogui.hotkey('ctrl', 'v')

    # Press enter
    pyautogui.press('enter')
    time.sleep(1)

# Function: Chat
def do_chat(last_action_type):
    if last_action_type == "chat":
        if IS_DEBUG:
            print(f"Action: Skipped Chat (consecutive)")
        sys.stdout.flush()
        return last_action_type

    print(f"Action: Chat Input")
    sys.stdout.flush()
    try:
        # Request with 180s timeout
        req = urllib.request.Request(
            "https://api.piece.one/chat.php", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=180) as response:
            if response.status == 200:
                content = response.read().decode('utf-8')
                data_json = json.loads(content)
                chat_data = data_json.get('data', '')
                
                if chat_data:
                    send_chat_msg(chat_data)
                    return "chat"
    except Exception as req_err:
        print(f"Request failed or timed out: {req_err}")
        sys.stdout.flush()
    
    return "chat"

# Function: Drop
def do_drop(last_action_type):
    if last_action_type == "drop":
        if IS_DEBUG:
            print(f"Action: Skipped Drop (consecutive)")
        sys.stdout.flush()
        return last_action_type

    print(f"Action: Drop Item")
    sys.stdout.flush()
    
    drop_item = random.choice(AVAILABLE_DROPS)
    message = f"drop:{drop_item}"
    
    send_chat_msg(message)
    return "drop"

# Function: Color
def do_color(last_action_type):
    if last_action_type == "color":
        if IS_DEBUG:
            print(f"Action: Skipped Color (consecutive)")
        sys.stdout.flush()
        return last_action_type
        
    color_hex = f"#{random.randint(0, 0xFFFFFF):06x}"
    print(f"Action: Color Command -> {color_hex}")
    sys.stdout.flush()
    
    message = f"color: {color_hex}"
    send_chat_msg(message)
    return "color"

# Main execution loop with auto-restart
def main_loop():
    global last_refresh_time
    
    last_action_type = None
    
    while True:
        # Check stop flag periodically
        if os.path.exists(STOP_FLAG_FILE):
            print("Stop flag detected. Exiting...")
            sys.stdout.flush()
            os.remove(STOP_FLAG_FILE)
            return
        
        try:
            rand_val = random.random()
            
            # 1. Logic if random value < 0.3: Move and Click (0.5s - 2s)
            if rand_val < 0.3:
                angle = random.uniform(0, 2 * math.pi)
                tx = center_x + radius * math.cos(angle)
                ty = center_y + radius * math.sin(angle)
                
                print(f"Action: Move & Click ({rand_val:.2f})")
                sys.stdout.flush()
                
                if not IS_DEBUG:
                    pyautogui.moveTo(tx, ty, duration=0.5)
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
                
                if not IS_DEBUG:
                    pyautogui.moveTo(tx, ty, duration=0.5)
            
            # 3. Logic if random value >= 0.6: Special Actions
            else:
                sub_rand = random.random()
                
                if sub_rand < 0.2:
                    last_action_type = do_chat(last_action_type)
                elif sub_rand < 0.5:
                    last_action_type = do_drop(last_action_type)
                else:
                    print(f"Action: Skipped > 0.6 ({rand_val:.2f}, sub: {sub_rand:.2f})")
                    sys.stdout.flush()
                    time.sleep(0.5)
            
            # Check if need to refresh browser
            current_time = time.time()
            if current_time - last_refresh_time >= REFRESH_INTERVAL:
                print("Action: Refreshing browser...")
                sys.stdout.flush()
                pyautogui.press('f5')
                last_refresh_time = current_time
                time.sleep(2)

            time.sleep(EXECUTION_INTERVAL)
            
        except Exception as e:
            print(f"Error: {e}")
            sys.stdout.flush()
            time.sleep(EXECUTION_INTERVAL)

# Run with auto-restart
while True:
    # Check stop flag before starting
    if os.path.exists(STOP_FLAG_FILE):
        print("Stop flag detected. Exiting...")
        sys.stdout.flush()
        os.remove(STOP_FLAG_FILE)
        break
    
    # Reset refresh time
    last_refresh_time = time.time()
    
    print("Starting main loop...")
    sys.stdout.flush()
    
    try:
        main_loop()
    except Exception as e:
        print(f"Outer loop error: {e}, restarting in 5 seconds...")
        sys.stdout.flush()
        time.sleep(5)
        continue
