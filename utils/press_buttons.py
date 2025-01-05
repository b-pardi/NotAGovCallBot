import pyautogui
import time
import os
import random

from utils.misc import convert_timestamps_to_seconds
from utils.screen_grab import move_keypad_locs_for_call_start, locate_button_from_image

def scheduled_key_press(keypad_locs, call_btn_loc, target_number, timed_instructions):
    # dial number
    for num in target_number:
        x, y = keypad_locs[num]
        pyautogui.click(x, y)

    pyautogui.click(call_btn_loc)

    # when starting call keypad moves up a bit from it's init location
    keypad_locs = move_keypad_locs_for_call_start(keypad_locs)
    print(keypad_locs)

    start_time = time.time()
    for timestamp, key in timed_instructions:
        # find how long to wait for next instr and wait
        target_time = convert_timestamps_to_seconds(timestamp)
        wait_time = start_time + target_time - time.time()
        if wait_time > 0:
            time.sleep(wait_time)
        
        # execute next key press
        if key == 'KEYPAD': # open up keypad after starting call
            keypad_button_loc = locate_button_from_image("res/keypad_btn.png")
            pyautogui.click(keypad_button_loc)
        elif key == 'SSN': # enter ssn stage
            ssn = os.getenv('SSN')
            for num in ssn:
                pyautogui.click(keypad_locs[num])
        elif key == 'PIN': # enter pin stage
            pin = os.getenv('PIN')
            for num in pin:
                pyautogui.click(keypad_locs[num])
        elif key == 'END': # end of call cycle, check if ended and return False if it did
            call_in_progress = locate_button_from_image("res/hangup_btn.png") # check if hangup button there
            if call_in_progress:
                return True
            else:
                return False
        else: # if just pressing single key according to timed_instructions list
            pyautogui.click(keypad_locs[key])
            print(f"pressed {key} at {timestamp}")

def init_msgs_send(init_key_locations, target_phone_number):
    '''init key locs contains x,y tuples of px coords for the following locations in order:
    send new message button,
    top of phone number entry box,
    bottom of same,
    message entry box
    '''
    
    # press to send new msg
    pyautogui.click(init_key_locations[0])
    time.sleep(1)

    # focus phone num box and enter/confirm num
    dy_num_box = (init_key_locations[2][1] - init_key_locations[1][1])
    y_center_phone_num_box = (init_key_locations[1][1] + dy_num_box / 2)
    #pyautogui.click(init_key_locations[1][0], y_center_phone_num_box)
    #pyautogui.click(init_key_locations[1][0], y_center_phone_num_box)
    time.sleep(1)

    pyautogui.typewrite(target_phone_number, interval=0.1)

    time.sleep(1)
    pyautogui.click(init_key_locations[2][0], init_key_locations[2][1] + dy_num_box*1)
    time.sleep(1)

    # enter focus in text box
    pyautogui.click(init_key_locations[3])
    time.sleep(0.08)
    pyautogui.click(init_key_locations[3])

def scheduled_msgs(init_key_locations, target_phone_number, msg):
    # type msg    
    pyautogui.typewrite(msg, interval=random.uniform(0.03, 0.075))
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press('enter')
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.click(init_key_locations[3])
    time.sleep(random.uniform(4.26, 9.76))
