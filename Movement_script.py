import cv2
import numpy as np
import serial
import time
import csv
from utils import *

# Vanessa Hofschneider with assistance from Samuel Freitas
# created 1/31/24

def begin_imaging():

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
    serial_port = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'
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
        next(reader) # skipping my header
        for row in reader:
            positions.append((float(row[0]), float(row[1]), float(row[2])))
    return positions

# main code

try:
    home()  # Homing the machine

    # change this depending on what plate you are using
    positions = read_positions_from_csv('settings_terasaki_positions.csv')
    for position in positions:
        move_to_position(position)  # Move to each position

        ret, frame = cap.read()  # Read frame from camera
        cv2.imwrite(f'position_{position}.png', frame)  # Save image    
    
except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()


