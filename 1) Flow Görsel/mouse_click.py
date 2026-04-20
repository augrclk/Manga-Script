import sys
import subprocess
import time

try:
    import pyautogui
except ImportError:
    print("PyAutoGUI not installed, installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

def click(x, y):
    # PyAutoGUI will click the coordinates
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            x_pos = int(sys.argv[1])
            y_pos = int(sys.argv[2])
            click(x_pos, y_pos)
        except Exception as e:
            print(f"Error clicking: {e}")
            sys.exit(1)
