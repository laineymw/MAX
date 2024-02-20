import serial
import time
import csv

#Vanessa Hofschneider with assistant from Samuel Freitas created 1/31/24

# Replace 'your_serial_port' with the actual port where your GRBL controller is connected (e.g., '/dev/ttyUSB0')
serial_port = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'
baud_rate = 115200

# Open the serial port connection
ser = serial.Serial(serial_port, baud_rate, timeout=5)

# Wait for the connection to establish
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

try:
    home()  # Homing the machine

    # change this depending on what plate you are using
    positions = read_positions_from_csv('settings_terasaki_positions.csv')

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()


