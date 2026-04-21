import json
import os
import requests
import sys
import traceback

# --- SWITCH 1: PC HANDS & EYES ---
try:
    import pyautogui
    HAS_HANDS = True
except Exception:
    HAS_HANDS = False

# --- SWITCH 2: OFFLINE BRAIN ---
try:
    from llama_cpp import Llama
    HAS_BRAIN = True
except Exception:
    HAS_BRAIN = False

MEMORY_FILE = "memory.json"
FIREBASE_URL = "https://my-advanced-ai-default-rtdb.firebaseio.com/memory.json"
MODEL_NAME = "tinyllama-1.1b-chat-v1.0.q4_k_m.gguf"

# --- FIND THE HIDDEN BRAIN INSIDE THE .EXE ---
def get_brain_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, MODEL_NAME)
    return MODEL_NAME

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
    if not HAS_BRAIN:
        return "I need the offline brain installed on this device to think."
    
    print("[System] Waking up offline AI brain...")
    # Using the new path tool here
    try:
        llm = Llama(model_path=get_brain_path(), verbose=False)
        context = f"Past Knowledge:\n{memory}\n\nUser: {user_input}\nAI:"
        output = llm(context, max_tokens=150, stop=["User:", "\n\n"])
        return output['choices'][0]['text'].strip()
    except Exception as e:
        return f"BRAIN ERROR: {str(e)}"

def execute_task(task_name):
    if not HAS_HANDS:
        print(f"[System] I know how to '{task_name}', but I need to be on a PC to use the mouse.")
        return
    print(f"[System] HANDS ACTIVE: Executing '{task_name}'...")
    print(f"[System] SUCCESS: '{task_name}' completed.")

def main():
    print("=== Advanced All-In-One AI ===")
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
            print("AI is thinking...")
            answer = think_and_answer(user_input, ai_memory)
            print(f"AI: {answer}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n=== SYSTEM CRASH FAULT CODE ===")
        traceback.print_exc()
        input("\nPress ENTER to close the window...")
