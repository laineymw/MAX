import csv
import tkinter as tk
from tkinter import filedialog
import os

import tkinter as tk
from tkinter import filedialog

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_experiment():
    experiment_type = experiment_var.get()
    save_folder = folder_entry.get()
    
    if experiment_type == "New":
        experiment_name = new_experiment_name_entry.get()
        repeat = repeat_entry.get()
        condition = condition_entry.get()
        day = day_entry.get()
        print(f"New Experiment: {experiment_name}, Repeat: {repeat}, Condition: {condition}, Day: {day}")
        experiment_folder = os.path.join(save_folder, experiment_name, repeat, condition, day)
    else:
        day = day_entry.get()
        print(f"Existing Experiment: {experiment_name}, Day: {day}")
        experiment_folder = os.path.join(save_folder, day)
        
    
    # Check if the folder already exists
    folder_exists = True
    folder_index = 1
    while folder_exists:
        if not os.path.exists(experiment_folder):
            os.makedirs(experiment_folder, exist_ok=True)
            print(f"Experiment folder created: {experiment_folder}")
            folder_exists = False
        else:
            # Append a number to the folder name and check again
            experiment_folder = f"{experiment_folder}_{folder_index}"
            folder_index += 1
            
root = tk.Tk()
root.title("Experiment Setup")

experiment_label = tk.Label(root, text="Experiment Type:")
experiment_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

experiment_var = tk.StringVar(root, "New")
new_experiment_radio = tk.Radiobutton(root, text="New", variable=experiment_var, value="New")
new_experiment_radio.grid(row=0, column=1, padx=5, pady=5, sticky="w")
existing_experiment_radio = tk.Radiobutton(root, text="Existing", variable=experiment_var, value="Existing")
existing_experiment_radio.grid(row=0, column=2, padx=5, pady=5, sticky="w")

new_experiment_frame = tk.Frame(root)

new_experiment_name_label = tk.Label(new_experiment_frame, text="Experiment Name:")
new_experiment_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
new_experiment_name_entry = tk.Entry(new_experiment_frame)
new_experiment_name_entry.grid(row=0, column=1, padx=5, pady=5)

repeat_label = tk.Label(new_experiment_frame, text="Repeat:")
repeat_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
repeat_entry = tk.Entry(new_experiment_frame)
repeat_entry.grid(row=1, column=1, padx=5, pady=5)

condition_label = tk.Label(new_experiment_frame, text="Condition:")
condition_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
condition_entry = tk.Entry(new_experiment_frame)
condition_entry.grid(row=2, column=1, padx=5, pady=5)

day_label = tk.Label(new_experiment_frame, text="Day:")
day_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
day_entry = tk.Entry(new_experiment_frame)
day_entry.grid(row=3, column=1, padx=5, pady=5)

existing_experiment_frame = tk.Frame(root)

day_label = tk.Label(existing_experiment_frame, text="Day:")
day_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
day_entry = tk.Entry(existing_experiment_frame)
day_entry.grid(row=1, column=1, padx=5, pady=5)

folder_label = tk.Label(root, text="Save Folder:")
folder_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
folder_entry = tk.Entry(root)
folder_entry.grid(row=4, column=1, padx=5, pady=5)
folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.grid(row=4, column=2, padx=5, pady=5)

start_button = tk.Button(root, text="Start Experiment", command=start_experiment)
start_button.grid(row=5, column=1, padx=5, pady=5)

def show_frame():
    if experiment_var.get() == "New":
        existing_experiment_frame.grid_remove()
        new_experiment_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
    else:
        new_experiment_frame.grid_remove()
        existing_experiment_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

experiment_var.trace("w", lambda *args: show_frame())
show_frame()

root.mainloop()
