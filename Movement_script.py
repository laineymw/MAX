import cv2
import numpy as np
import serial
import time
import csv
import os
from utils import *
from user_inputs_gui import run_gui

# Vanessa Hofschneider with assistance from Samuel Freitas
# created 1/31/24

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
cap.set(cv2.CAP_PROP_GAIN, 1000) # set gain
cap.set(cv2.CAP_PROP_AUTO_WB, 0) # turn off auto white balance
cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 5000) # set the white balance to some number
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) # turn off auto exposure 
cap.set(cv2.CAP_PROP_EXPOSURE,-5) # i think this is 2^(exposure)
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

# main code

try:
    # Get the experiment folder from the user using the gui
    experiment_folder = run_gui() 
    # Homing the machine
    home()

    # change this depending on what plate you are using
    positions = read_positions_from_csv('settings_terasaki_positions.csv')
    print("Close door. Imaging will begin in 5 seconds.")
    time.sleep(5) # give the user time to close or turn off lights and leave
        
    for idx,position in enumerate(positions):
        
        #move_to_position(position)  # Move to each position
        move_to_position(position[:3])

        if idx == 0:
            time.sleep(10)
        else:
            time.sleep(2)
        
        for i in range(1,4):  # need to take 3 images per well  
            ret, frame = cap.read()  # Read frame from camera
            time.sleep(0.2)
            if not ret or frame is None:
                print(f"Error: Failed to capture image for {position[3]}_{i:03d}")
                continue  # Skip saving this frame
            
            image_name = f"{position[3]}_{i:03d}.png"  # Format the image name
            image_path = os.path.join(experiment_folder, image_name)
            
            if cv2.imwrite(image_path, frame):
                print(f"Saved: {image_name}")
            else:
                print(f"Error: Failed to save {image_name}")
            #cv2.imwrite(image_path, frame)  # Save image  
    
    print("Plate imaging complete. Please turn off light source.")  
    home()
    
except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()
    