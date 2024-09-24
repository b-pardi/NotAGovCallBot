import time
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageGrab
import os
import cv2
import pyautogui
import pygame

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
    ('4:03', '0'), # speak to rep
    ('4:48', 'END') # check if call ended (if not then live agent soon)
]

def screen_grab(roi=None):
    screen = ImageGrab.grab(bbox=roi)
    screen_arr = np.array(screen, dtype=np.uint8)
    return screen_arr

def select_points(instr, num_required_pts):
    screen_arr = screen_grab()
    fig, ax = plt.subplots(figsize=(16,10))
    ax.imshow(screen_arr)
    ax.set_title(instr)
    points = []

    def onclick(event):
        points.append((int(event.xdata), int(event.ydata)))
        ax.plot(event.xdata, event.ydata, 'ro')
        if len(points) == num_required_pts: # only need to indicate keypad nums 1 and 2, and later phone call btn
            fig.canvas.mpl_disconnect(conn_id)
            plt.close()
        fig.canvas.draw() 

    conn_id = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    return points

def find_keypad_locations(init_key_points):
    try:
        p1, p2 = init_key_points
    except Exception as e:
        print(f"Invalid number of points: {e}")

    if p1[0] < p2[0]: # 1 key will be leftmost between nums 1 and 2
        x1, y1 = p1
        x2, y2 = p2
    else:
        x2, y2 = p1
        x1, y1 = p2

    dx = x2 - x1
    dy = y2 - y1

    keypad_positions = {'1': (x1, y1)} # initial known keypad positions
    for i in range(2, 10): # fill in rest of digits 3-9
        row = (i-1) // 3
        col = (i-1) % 3
        keypad_positions[f'{i}'] = (x1 + col * dx, y1 + row * dy)
    
    # adding exception chars (bottom row of keypad)
    keypad_positions['0'] = (x2, y1 + 3 * dy)
    keypad_positions['*'] = (x1, y1 + 3 * dy)
    keypad_positions['#'] = (x1 + 2 * dx, y1 + 3 * dy)

    return keypad_positions

def convert_timestamps_to_seconds(timestamp):
    m, s = map(int, timestamp.split(':'))
    return m * 60 + s

def move_keypad_locs_for_call_start(keypad_locs):
    dy = keypad_locs['0'][1] - keypad_locs['2'][1]
    updated_keypad_locs = {}
    for key, loc in keypad_locs.items():
        updated_keypad_locs[key] = (loc[0], loc[1] - dy)

    return updated_keypad_locs

def locate_button_from_image(img_path, thresh=0.85):
    screen_img = cv2.cvtColor(screen_grab(), cv2.COLOR_RGB2BGR)

    template = cv2.imread(img_path)
    match_res = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(match_res >= thresh)
    if len(loc[0]) == 0:
        print(f"Did not find img {img_path}")
        return False
    else:
        print(loc[1][0], loc[0][0])
        return (loc[1][0], loc[0][0]) # xy coords of button

def scheduled_key_press(keypad_locs, call_btn_loc, target_number):
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

def notify():
    # Initialize Pygame
    pygame.init()
    
    # Setup the display
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Alert")

    # Define colors
    red = (255, 0, 0)
    white = (255, 255, 255)

    # Load and play sound
    pygame.mixer.init()
    pygame.mixer.music.load("res/coffin_dance.mp3")
    pygame.mixer.music.play()

    # Set the font for the text
    font = pygame.font.Font(None, 36)
    text = font.render("Found EDD AGENT", True, white)
    text_rect = text.get_rect(center=(width/2, height/2))

    # Event loop flag
    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with red
        screen.fill(red)
        
        # Blit the text onto the screen
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

def spam(keypad_locations_dict, phone_call_button_location, target_phone_number):
    i = 1
    while True:
        print(f"Attempting {i} calls")
        found_live_agent = scheduled_key_press(keypad_locations_dict, phone_call_button_location, target_phone_number)
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
    spam(keypad_locations_dict, phone_call_button_location, target_phone_number)

if __name__ == '__main__':
    main()