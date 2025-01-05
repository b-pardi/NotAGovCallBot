from dotenv import load_dotenv
import os
import keyboard

from utils.screen_grab import *
from utils.press_buttons import *
from utils.misc import *

load_dotenv()

msgs = [
    'You are a waste of space',
    'You do not deserve life',
    'You are sick and twisted with your rape fantasies',
    'Wanna spam text girls over voip?',
    'You get what you deserve'
]

def spam_text(init_key_locations, target_phone_number, num_msgs):
    i = 0
    while i // len(msgs) < num_msgs:
        if keyboard.is_pressed('esc'):
            break

        print(f"Sending msg num {i+1}")
        msg_idx = i % len(msgs)
        scheduled_msgs(init_key_locations, target_phone_number, msgs[msg_idx])
        i+=1

def main():
    num_msgs = 30
    init_key_locations = select_points("Select 'send new message' button, top of phone number entry box, bottom of same, and the message entry box", 4)
    target_phone_number =  os.getenv('TARGET_TEXT_NUMBER')
    
    print(init_key_locations)
    init_msgs_send(init_key_locations, target_phone_number)
    time.sleep(1)
    spam_text(init_key_locations, target_phone_number, num_msgs)

