import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime


def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_experiment():
    global experiment_folder
    
    experiment_type = experiment_var.get()
    save_folder = folder_entry.get()
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    # depending on new or existing experiment,
    # make a new folder directory or day folder
    
    if experiment_type == "New":
        experiment_name = new_experiment_name_entry.get()
        repeat_val = repeat_entry.get()
        condition_val = condition_entry.get()
        plate_id_day_val = plate_id_day_entry_new.get()
        print(f"New Experiment: {experiment_name}, Repeat: {repeat_val}, Condition: {condition_val}, Plate ID and Day (ex. ID_D#): {plate_id_day_val}")
        current_folder_name = f"{current_time}--{plate_id_day_val}"
        experiment_folder = os.path.join(save_folder, experiment_name, repeat_val, condition_val, current_folder_name)
    else:
        plate_id_day_val = plate_id_day_entry_existing.get()
        print(f"Existing Experiment: Plate ID and Day (ex. ID_D#): {plate_id_day_val}")
        current_folder_name = f"{current_time}--{plate_id_day_val}"
        experiment_folder = os.path.join(save_folder, current_folder_name)
    
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
    
    #close window after getting user inputs
    root.destroy()

def run_gui():
    global root, experiment_var, folder_entry, new_experiment_name_entry,\
        repeat_entry, condition_entry, plate_id_day_entry_new, plate_id_day_entry_existing,\
        existing_experiment_frame, new_experiment_frame         
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

    plate_id_day_label_new = tk.Label(new_experiment_frame, text="Plate ID and Day (ex. ID_D#):")
    plate_id_day_label_new.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    plate_id_day_entry_new = tk.Entry(new_experiment_frame)
    plate_id_day_entry_new.grid(row=3, column=1, padx=5, pady=5)

    existing_experiment_frame = tk.Frame(root)

    plate_id_day_label_existing = tk.Label(existing_experiment_frame, text="Plate ID and Day (ex. ID_D#):")
    plate_id_day_label_existing.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    plate_id_day_entry_existing = tk.Entry(existing_experiment_frame)
    plate_id_day_entry_existing.grid(row=0, column=1, padx=5, pady=5)

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
    
    return experiment_folder

if __name__ == "__main__":
    experiment_folder = run_gui()
    print("Experiment Folder:", experiment_folder)
