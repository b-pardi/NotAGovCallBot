from dotenv import load_dotenv
import os

from utils.screen_grab import *
from utils.press_buttons import *
from utils.misc import *

load_dotenv()

timed_instructions = [
    ('0:10', 'KEYPAD'), # open keypad after starting call
    ('0:15', '1'), # press 1 for english
    ('1:20', '1'), # press 1 for having existing claim
    ('1:23', '1'), # press 1 for questions about claim
    ('1:32', 'SSN'), # enter SSN
    ('1:41', '1'), # confirm SSN entered correctly
    ('1:51', '1'), # have pin
    ('1:55', 'PIN'), # enter pin
    ('2:02', '1'), # confirm pin
    ('2:59', '0'), # speak to rep
    ('4:44', 'END') # check if call ended (if not then live agent soon)
]

def spam_call(keypad_locations_dict, phone_call_button_location, target_phone_number):
    i = 1
    while True:
        print(f"Attempting {i} calls")
        found_live_agent = scheduled_key_press(keypad_locations_dict, phone_call_button_location, target_phone_number, timed_instructions)
        if found_live_agent:
            notify()
            break
        i+=1

def main():
    init_key_locations = select_points("Select numbers 1 and 5 on the keypad", 2)
    phone_call_button_location = select_points("Select phone call button", 1)[0]

    target_phone_number =  os.getenv('TARGET_PHONE_NUMBER')
    keypad_locations_dict = find_keypad_locations(init_key_locations)
    print(keypad_locations_dict, phone_call_button_location)
    spam_call(keypad_locations_dict, phone_call_button_location, target_phone_number)

