import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageGrab
import cv2


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