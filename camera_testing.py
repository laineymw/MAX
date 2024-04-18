import cv2, time
import numpy as np
from utils import *

def calculate_fps(prev_time):
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    return fps, current_time

# supported = list_all_potential_cap_APIs()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # using dshow

# get the inital settings
supported_settings, current_settings, cv2_idx = list_supported_capture_properties(cap)
settings_array = np.asarray([cv2_idx,supported_settings,current_settings]).T
print('Inital settings')
print(settings_array)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,5600) # set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,3740) # set heigh
cap.set(cv2.CAP_PROP_FPS,10) # set max fps (max is 4.5fps)
cap.set(cv2.CAP_PROP_GAIN, 1000) # set gain
cap.set(cv2.CAP_PROP_AUTO_WB, 0) # turn off auto white balence
cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 5000) # set the white balence to some number
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # turn off auto exposure 
cap.set(cv2.CAP_PROP_EXPOSURE,-5) # i think this is 2^(exposure)
cap.set(cv2.CAP_PROP_CONVERT_RGB,1) # force to return as rgb image

# fourcc = int(cap.get(cv2.CAP_PROP_FOURCC)) # get and decode the codec, should return YUV2 doesnt really matter
# codec = chr(fourcc & 0xFF) + chr((fourcc >> 8) & 0xFF) + chr((fourcc >> 16) & 0xFF) + chr((fourcc >> 24) & 0xFF)

supported_settings, current_settings, cv2_idx = list_supported_capture_properties(cap)
settings_array = np.asarray([cv2_idx,supported_settings,current_settings]).T
print('Custom settings')
print(settings_array)
# print('CODEC', codec)

clear_camera_image_buffer(cap,N = 10) # get the first N frames and throw them away 

cap.set(cv2.CAP_PROP_SETTINGS, 1) ############### uncomment this for a graphical interface for setting the settings (its bad though)
# Variables for FPS calculation
prev_time = time.time()
start_time = prev_time

counter = 0
while True:

    ret, frame = cap.read() # reads and return the data from the camera
    imshow_resize("img",frame,resize_size=[640,480],move_to=[1000,1]) # shows the image at the top left of screen

    counter += 1
    # every 10 seconds print the frames per second and record an image
    elap = time.time() - start_time
    if elap > 10:
        print(counter, "frames in", elap, "seconds ------ ", counter/elap)
        start_time = time.time()
        counter = 0
        #cv2.imwrite('test.png',frame)


        