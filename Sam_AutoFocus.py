import os,time,glob,sys,time,tqdm,cv2, serial, json, 
import numpy as np
# import movement.simple_stream
import atexit

# How function is called in main
'''
if well_index == 0:
                lights.labjackU3_control.turn_off_everything(d)
                # get first autofocus and return the cap
                z_pos_found_autofocus_inital, cap = run_autofocus_at_current_position(controller, 
                    this_well_coords, coolLED_port, this_plate_parameters, autofocus_min_max = [3,-3], 
                    autofocus_delta_z = 0.1, cap = None, af_area=af_area)
                this_well_coords['z_pos'] = z_pos_found_autofocus_inital
                found_autofocus_positions.append(z_pos_found_autofocus_inital)
            else:  
                z_pos_found_autofocus, cap = run_autofocus_at_current_position(controller, 
                    this_well_coords, coolLED_port, this_plate_parameters, autofocus_min_max = [0.5,-0.5], 
                    autofocus_delta_z = (1/6), cap = cap, af_area=af_area)
                this_well_coords['z_pos'] = z_pos_found_autofocus
                found_autofocus_positions.append(z_pos_found_autofocus)
'''

def run_autofocus_at_current_position(controller, starting_location, coolLED_port, 
    this_plate_parameters, autofocus_min_max = [1,-1], autofocus_delta_z = 0.25, cap = None, show_results = False, af_area = 2560):

    lights.coolLed_control.turn_everything_off(coolLED_port) # turn everything off

    autofocus_steps = int(abs(np.diff(autofocus_min_max) / autofocus_delta_z)) + 1
    z_limit = [-10,-94]
    offset = 25 # this is for the autofocus algorithm how many pixels apart is the focus to be measures
    thresh = 5 # same as above but now ignores all the values under thresh

    # find the z locations for the loop to step through
    z_positions_start = np.linspace(starting_location['z_pos']+autofocus_min_max[0],starting_location['z_pos']+autofocus_min_max[1],num = autofocus_steps)
    z_positions = []

    # turn on the RGB lights to get a white light for focusing 
    lights.coolLed_control.turn_specified_on(coolLED_port, 
        uv = True, uv_intensity = 1,
        blue = True, blue_intensity = 10,
        green = True, green_intensity = 10,
        red = True, red_intensity = 0)
  
    # go though all the z_positions and get the most in focus position
    images = []
    uncalib_fscore = []
    for counter,z_pos in enumerate(z_positions_start):
        this_location = starting_location.copy()
        this_location['z_pos'] = z_pos
        # jprint(this_location)

        if z_pos < z_limit[0] and z_pos > z_limit[1]:
            z_positions.append(z_pos)

            controller.move_XYZ(position = this_location) # move the said location 
                
            if (counter == 0) and (cap is not None): # capture the frame and return the image and camera 'cap' object
                frame, cap = camera.camera_control.capture_fluor_img_return_img(s_camera_settings, cap = cap, return_cap = True, clear_N_images_from_buffer = 3) 
            elif (counter == 0) and (cap == None):
                frame, cap = camera.camera_control.capture_fluor_img_return_img(s_camera_settings, return_cap = True, clear_N_images_from_buffer = 3) 
            else:
                frame, cap = camera.camera_control.capture_fluor_img_return_img(s_camera_settings, cap = cap, return_cap = True, clear_N_images_from_buffer = 1)
            images.append(frame)
            temp = analysis.fluor_postprocess.crop_center_numpy_return(frame, af_area, center = [1440,1252] )
            temp = sq_grad(temp,thresh = thresh,offset = offset)
            uncalib_fscore.append(np.sum(temp))
            camera.camera_control.imshow_resize(frame_name = "stream", frame = frame)
    
    lights.coolLed_control.turn_everything_off(coolLED_port) # turn everything off

    assumed_focus_idx = np.argmax(uncalib_fscore)

    if show_results:
        plt.plot(uncalib_fscore)
        plt.plot(assumed_focus_idx,uncalib_fscore[assumed_focus_idx],'go')
        plt.show(block = True)
        plt.pause(5)
        plt.close('all')

    if (assumed_focus_idx == 0):
        print('rerunning AF Moving UP')
        [assumed_focus_idx, uncalib_fscore, z_positions, controller, starting_location, coolLED_port, this_plate_parameters, 
         autofocus_min_max, autofocus_delta_z, cap , show_results, af_area] = quick_autofocus_rerun(controller, 
            starting_location, coolLED_port, 
            this_plate_parameters, autofocus_min_max, autofocus_delta_z , cap, show_results, af_area, up_or_down=1)
    elif (assumed_focus_idx == len(uncalib_fscore)-1):
        print('rerunning AF Moving DOWN')
        [assumed_focus_idx, uncalib_fscore, z_positions, controller, starting_location, coolLED_port, this_plate_parameters, 
         autofocus_min_max, autofocus_delta_z, cap , show_results, af_area] = quick_autofocus_rerun(controller, 
            starting_location, coolLED_port, 
            this_plate_parameters, autofocus_min_max, autofocus_delta_z , cap, show_results, af_area, up_or_down=-1)

    z_pos = z_positions[assumed_focus_idx] # for the final output
    this_location = starting_location.copy()
    this_location['z_pos'] = z_positions[assumed_focus_idx] + 0.05
    controller.move_XYZ(position = this_location)

    lights.coolLed_control.turn_specified_on(coolLED_port, 
        uv = int(this_plate_parameters['fluorescence_UV']) > 0, 
        uv_intensity = int(this_plate_parameters['fluorescence_UV']),
        blue = int(this_plate_parameters['fluorescence_BLUE']) > 0, 
        blue_intensity = int(this_plate_parameters['fluorescence_BLUE']),
        green = int(this_plate_parameters['fluorescence_GREEN']) > 0, 
        green_intensity = int(this_plate_parameters['fluorescence_GREEN']),
        red = int(this_plate_parameters['fluorescence_RED']) > 0, 
        red_intensity = int(this_plate_parameters['fluorescence_RED']))

    frame, cap = camera.camera_control.capture_fluor_img_return_img(s_camera_settings, cap = cap,return_cap = True, clear_N_images_from_buffer = 2)
    camera.camera_control.imshow_resize(frame_name = "stream", frame = frame)

    return z_pos, cap
