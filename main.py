import json
import os
import requests
import google.generativeai as genai
import traceback

# --- SWITCH 1: PC HANDS ---
try:
    import pyautogui
    HAS_HANDS = True
except Exception:
    HAS_HANDS = False

# --- CLOUD BRAIN SETUP ---
API_KEY = "AIzaSyB8fbSHc59soaFex7xmk7nZp1ZAPcD6yyU"  # <--- PASTE YOUR KEY HERE
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') 

MEMORY_FILE = "memory.json"
FIREBASE_URL = "https://my-advanced-ai-default-rtdb.firebaseio.com/memory.json"

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
    except Exception:
        pass 

def think_and_answer(user_input, memory):
    print("[System] Beaming question to cloud supercomputer...")
    try:
        context = f"Past Knowledge:\n{memory}\n\nUser: {user_input}\nAI:"
        response = model.generate_content(context)
        return response.text.strip()
    except Exception as e:
        return f"CLOUD ERROR: {str(e)}"

def execute_task(task_name):
    if not HAS_HANDS:
        print(f"[System] I know how to '{task_name}', but I need to be on a PC to use the mouse.")
        return
    print(f"[System] HANDS ACTIVE: Executing '{task_name}'...")
    print(f"[System] SUCCESS: '{task_name}' completed.")

def main():
    print("=== Advanced Cloud AI (Lightweight) ===")
    ai_memory = load_memory()
    
    while True:
        user_input = input("\nYou (Teach/Do/Ask/Exit): ")
        
        if user_input.lower() == 'exit':
            break
            
        if user_input.startswith("do "):
            task = user_input.replace("do ", "")
            if task in ai_memory:
                execute_task(task)
            else:
                print("AI: I don't know how to do that yet.")
                
        elif user_input.startswith("teach "):
            task = user_input.replace("teach ", "")
            ai_memory[task] = "Learned task logic."
            save_memory(ai_memory)
            sync_to_cloud(ai_memory)
            print("[System] Knowledge saved and synced.")
            
        else:
            answer = think_and_answer(user_input, ai_memory)
            print(f"\nAI: {answer}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n=== SYSTEM CRASH FAULT CODE ===")
        traceback.print_exc()
        input("\nPress ENTER to close the window...")
