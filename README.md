# Auto Piece One - Automation Script Guide

## 1. Environment Preparation

This script is developed based on Python and depends on the `pyautogui` library for mouse and keyboard simulation.

### 1.1 Install Python 3
Ensure that Python 3 is installed on your system.

### 1.2 Create Virtual Environment (Recommended)
To avoid polluting the global environment, it is recommended to run in a virtual environment.

```bash
# Execute in the project root directory
python3 -m venv venv
```

### 1.3 Activate Virtual Environment

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```cmd
  venv\Scripts\activate
  ```

### 1.4 Install Dependencies
After activating the virtual environment, install the required dependencies (including `pyautogui` and `python-dotenv`):

```bash
pip install pyautogui python-dotenv
```

---

## 2. Configuration

### 2.1 Debug Mode
The project uses a `.env` file for configuration. Before the first run, ensure a `.env` file exists in the root directory.

Set in the `.env` file:
```env
IS_DEBUG=true
```
- **IS_DEBUG=true**: Only print logs, no actions performed (recommended for first test run).
- **IS_DEBUG=false**: Enable actual mouse and keyboard actions.

### 2.2 Fail-Safe Mechanism
`pyautogui.FAILSAFE = True`
- When enabled, you can **move the mouse quickly to any of the four corners of the screen** to trigger an exception and stop the script immediately if the program goes out of control.

### 2.3 Execution Interval
`EXECUTION_INTERVAL = 5.0`
- Set the waiting time (in seconds) after each loop execution. Default is 5 seconds.

### 2.4 Available Drops List (AVAILABLE_DROPS)
`AVAILABLE_DROPS` is a list containing all possible drop item emojis. You can add, delete, or modify as needed.

---

## 3. Running the Script

Ensure the virtual environment is activated in your terminal, then execute:

```bash
python autopieceone.py
```

### Runtime Logic
The script runs in an infinite loop after starting. Press `Ctrl+C` to terminate.

Logic branches (based on random numbers):
1. **< 30%**: Move mouse and hold left click (0.5-2 seconds).
2. **30% - 60%**: Move mouse only.
3. **>= 60%**: Special Actions
    - **20% (Sub-probability)**: Request Chat API and automatically input returned content.
    - **30% (Sub-probability)**: Input `drop:` and randomly select a drop item.
    - **50% (Sub-probability)**: Skip action.

---

## 4. FAQ

- **Permission Issues (macOS)**: If running in non-Debug mode for the first time, macOS may prompt that the terminal needs "Accessibility" permissions to control the mouse and keyboard. Please check your terminal application (e.g., Terminal or iTerm) in `System Settings -> Privacy & Security -> Accessibility`.
- **Chat API 403 Error**: If you encounter an HTTP 403 error, it is usually because the API requires a browser identifier (User-Agent). This will be optimized in future versions.
