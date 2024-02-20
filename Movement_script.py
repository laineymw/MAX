import serial
import time

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

def home():
    send_command('$H')

def move_to(x, y, z):
    send_command(f'G0 X{x} Y{y} Z{z}')

# Example usage
try:
    home()  # Homing the machine

    # Moving to a specific position
    # move_to(5, 5, 0)

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()


