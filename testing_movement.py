import cv2
import numpy as np
import serial
import time
import csv
import os
import tkinter as tk
from utils import *
from user_inputs_gui import run_gui

# Function to close the loading window after 5 seconds
def close_loading_window():
    loading_window.destroy()

# Function to run the main script
def run_main_script():
    # Main script code here
    try:
        # Get the experiment folder from the user using the gui
        experiment_folder = run_gui() 
        # Homing the machine
        home()

        # change this depending on what plate you are using
        positions = read_positions_from_csv('settings_terasaki_positions.csv')
        
        for position in positions:
            time.sleep(0.2) # give the user time to close or turn off lights and leave
            #move_to_position(position)  # Move to each position
            move_to_position(position[:3])

            for i in range(1,4):  # need to take 3 images per well  
                ret, frame = cap.read()  # Read frame from camera
                image_name = f"{position[3]}_{i:03d}.png"  # Format the image name
                image_path = os.path.join(experiment_folder, image_name)
                cv2.imwrite(image_path, frame)  # Save image  
        
        print("Plate imaging complete. Please turn off light source.")  
        home()
        
    except KeyboardInterrupt:
        print("Script interrupted by user")
    finally:
        ser.close()

# OpenCV Setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # using dshow

# Get the initial settings
supported_settings, current_settings, cv2_idx = list_supported_capture_properties(cap)
settings_array = np.asarray([cv2_idx,supported_settings,current_settings]).T
print('Inital settings')
print(settings_array)

# Custom camera settings
cap.set(cv2.CAP_PROP_FRAME_WIDTH,5472) # set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,3648) # set height
cap.set(cv2.CAP_PROP_FPS,10) # set max fps (max is 4.5fps)
cap.set(cv2.CAP_PROP_GAIN, 256) # set gain
cap.set(cv2.CAP_PROP_AUTO_WB, 0) # turn off auto white balance
cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 5000) # set the white balance to some number
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) # turn off auto exposure 
cap.set(cv2.CAP_PROP_EXPOSURE,-8) # i think this is 2^(exposure)
cap.set(cv2.CAP_PROP_CONVERT_RGB,1) # force to return as RGB image

# Uncomment the following line for a graphical interface for setting the settings (it's not recommended)
# cap.set(cv2.CAP_PROP_SETTINGS, 1)

# Clear camera image buffer
clear_camera_image_buffer(cap, N=10)

# Variables for FPS calculation
prev_time = time.time()
start_time = prev_time
counter = 0

# Replace 'your_serial_port' with the port
# (e.g., '/dev/ttyUSB0')
# this is the one for the pi
# serial_port = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'

# this is the one for my personal computer
serial_port = 'COM3'
baud_rate = 115200

# Open the serial port connection
ser = serial.Serial(serial_port, baud_rate, timeout=5)
time.sleep(2)

def send_command(command):
    ser.write((command + '\n').encode())
    while True:
        response = ser.readline().decode().strip()
        if response == 'ok':
            break
        print(response)

# homing sequence 
def home():
    send_command('$H')

def move_to(x, y, z):
    send_command(f'G0 X{x} Y{y} Z{z}')
    
def move_to_position(position):
    x, y, z = position
    move_to(x,y,z)

# reading csv file of well positions
def read_positions_from_csv(filename):
    positions = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skipping the header
        for row in reader:
            x, y, z = map(float, row[:3])  # Extracting first three columns as positions and fourth column as the name
            name = row[3]
            positions.append((x, y, z, name))  # Appending to positions list
    return positions

# Main script starts here
if __name__ == "__main__":
    # Create a loading window
    loading_window = tk.Tk()
    loading_window.title("Loading Settings...")
    
    # Label for loading message
    loading_label = tk.Label(loading_window, text="Loading settings...")
    loading_label.pack()

    # Close the loading window after 5 seconds
    loading_window.after(5000, close_loading_window)
    
    # Run the main script after 5 seconds
    loading_window.after(5000, run_main_script)
    
    # Start the Tkinter event loop
    loading_window.mainloop()
