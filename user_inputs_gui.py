import csv
import tkinter as tk
from tkinter import filedialog

def read_positions_from_csv(filename):
    positions = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            positions.append((float(row[0]), float(row[1]), float(row[2])))
    return positions

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        positions = read_positions_from_csv(filename)
        # Here you can use the positions data as needed
        print("Positions loaded from:", filename)

def select_plate(plate_type):
    print("Selected plate type:", plate_type)

# Create the main window
root = tk.Tk()
root.title("Plate Selection")

# Create a frame for the plate selection
plate_frame = tk.LabelFrame(root, text="Select Plate Type")
plate_frame.pack(padx=10, pady=10)

# Add buttons for plate selection
plate_types = ["Terasaki", "Wormmotel", "Other"]
for plate_type in plate_types:
    tk.Button(plate_frame, text=plate_type, command=lambda t=plate_type: select_plate(t)).pack(side=tk.LEFT, padx=5)

# Add a button to browse for CSV file
tk.Button(root, text="Browse CSV", command=browse_file).pack(pady=10)

# Start the GUI main loop
root.mainloop()
