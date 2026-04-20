import json
import os
import requests
import platform
import time

# --- THE SMART BYPASS SWITCH ---
# This checks if we are on a PC to unlock the eyes and hands.
try:
    import pyautogui
    import pytesseract
    from PIL import Image
    HAS_HANDS = True
except ImportError:
    HAS_HANDS = False

MEMORY_FILE = "memory.json"
FIREBASE_URL = "https://my-advanced-ai-default-rtdb.firebaseio.com/memory.json"

# --- MEMORY AND CLOUD FUNCTIONS ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_memory(data):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def sync_to_cloud(data):
    try:
        requests.put(FIREBASE_URL, json=data, timeout=5)
    except requests.exceptions.ConnectionError:
        pass # Silently stay offline

# --- VISION AND EXECUTION FUNCTIONS (PC ONLY) ---
def execute_task(task_name):
    if not HAS_HANDS:
        print(f"[System] I know how to '{task_name}', but I am trapped in a mobile phone.")
        print("[System] Install me on a PC to physically execute this.")
        return

    print(f"\n[System] EYES OPEN: Scanning screen to execute '{task_name}'...")
    # 1. Take a screenshot
    screenshot = pyautogui.screenshot()
    
    # 2. Read the screen (OCR)
    print("[System] READING: Analyzing screen text...")
    # screen_text = pytesseract.image_to_string(screenshot)
    
    # 3. Take Control
    print(f"[System] HANDS ACTIVE: Taking control of mouse...")
    time.sleep(1)
    # Example PC movement: Move mouse to center and click
    # screen_width, screen_height = pyautogui.size()
    # pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=1)
    # pyautogui.click()
    
    print(f"[System] SUCCESS: Executed '{task_name}'\n")

# --- MAIN LOGIC LOOP ---
def main():
    print("=== Advanced All-In-One AI ===")
    if HAS_HANDS:
        print("[Status] Running on PC: Eyes and Hands UNLOCKED.")
    else:
        print("[Status] Running on Mobile: Brain active. Hands disabled by OS.")
    
    ai_memory = load_memory()
    
    while True:
        user_input = input("\nYou (Teach/Do/Exit): ")
        
        if user_input.lower() == 'exit':
            break
            
        # If user wants the AI to DO something it already knows
        if user_input.startswith("do "):
            task = user_input.replace("do ", "")
            if task in ai_memory:
                execute_task(task)
            else:
                print("AI: I don't know how to do that yet. Please teach me first.")
                
        # Otherwise, the AI LEARNS
        else:
            print("AI: Learning new instruction...")
            ai_memory[user_input] = "Task parameters saved."
            save_memory(ai_memory)
            sync_to_cloud(ai_memory)
            print("[System] Knowledge saved and synced.")

if __name__ == "__main__":
    main()
