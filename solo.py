import tkinter as tk
from tkinter import messagebox
import json
import datetime
import os

# Daily quest structure
DAILY_QUEST = {
    "Push-ups": 100,
    "Sit-ups": 100,
    "Squats": 100,
    "Run (km)": 10
}

DATA_FILE = "progress.json"

# Load or initialize progress
def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_completion(data):
    for task, goal in DAILY_QUEST.items():
        if data["quests"].get(task, 0) < goal:
            return False
    return True

# GUI app
class SoloGymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solo Leveling - Daily Quest System")

        self.data = load_progress()
        self.today = str(datetime.date.today())

        if self.today not in self.data:
            self.data[self.today] = {"quests": {}, "complete": False}

        self.user_data = self.data[self.today]["quests"]

        tk.Label(root, text="Sung Jin-Woo Daily Quest System", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.entries = {}
        for task, goal in DAILY_QUEST.items():
            frame = tk.Frame(root)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{task} (Goal: {goal}):").pack(side="left")
            var = tk.IntVar(value=self.user_data.get(task, 0))
            entry = tk.Entry(frame, textvariable=var, width=5)
            entry.pack(side="left")
            self.entries[task] = var

        tk.Button(root, text="Submit Progress", command=self.submit).pack(pady=10)
        self.status_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.status_label.pack()

        self.update_status()

    def submit(self):
        for task in DAILY_QUEST:
            self.user_data[task] = self.entries[task].get()

        self.data[self.today]["quests"] = self.user_data
        self.data[self.today]["complete"] = check_completion(self.data[self.today])
        save_progress(self.data)
        self.update_status()

    def update_status(self):
        if self.data[self.today]["complete"]:
            self.status_label.config(text="✅ Quest Complete! Stats Increased!", fg="green")
        else:
            self.status_label.config(text="⚠️ Quest Incomplete - Complete All Tasks!", fg="red")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = SoloGymApp(root)
    root.mainloop()
