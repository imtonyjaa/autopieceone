import subprocess
import time
import os
import sys

SCRIPT_PATH = r"C:\Users\ezshi\.openclaw\workspace\autopieceone\autopieceone.py"
NAME = "大钳子"
STOP_FILE = r"C:\Users\ezshi\.openclaw\workspace\autopieceone\stop.flag"

def main():
    while True:
        # Check stop flag
        if os.path.exists(STOP_FILE):
            print("Stop flag detected. Exiting wrapper.")
            os.remove(STOP_FILE)
            break
        
        print("Starting autopieceone.py...")
        sys.stdout.flush()
        
        # Run the script with UTF-8 encoding
        proc = subprocess.Popen(
            [sys.executable, SCRIPT_PATH, NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            errors='replace',
            bufsize=1
        )
        
        # Stream output
        try:
            for line in proc.stdout:
                print(line, end='')
                sys.stdout.flush()
        except Exception as e:
            print(f"Error reading output: {e}")
        
        proc.wait()
        
        # Check if stopped by flag
        if os.path.exists(STOP_FILE):
            print("Stop flag detected. Exiting wrapper.")
            os.remove(STOP_FILE)
            break
        
        print(f"Script exited with code {proc.returncode}. Restarting in 3 seconds...")
        sys.stdout.flush()
        time.sleep(3)

if __name__ == "__main__":
    main()
