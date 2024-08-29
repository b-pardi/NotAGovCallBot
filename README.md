# NotAGovCallBot
Python script designed to not spam call CA EDD in order to get a live agent ;)

You *Definitely* should *not* use this script to spam the California EDD contact number to automate the process of entering all the information and repeating the call process after getting hung up on by the robot voice so you can eventually get a live person to talk to.

## Setup instructions to not spam the government
1. Create a Google voice phone number in your web browser (look up google voice, if you have a google account you get a number for free)
    1.1. Make sure your keypad and hangup buttons match those images in the res folder. **NOTE** They may look similar but the resolutions must also match. If you're unsure, take your own screenshots of the keypad and hangup buttons, and put them in the res file replacing the existing ones.
2. Install Python (3.10.5 was used to create this)
3. Clone/Download this repository and navigate to the directory  containing `spam.py`
4. Create a file called `.env` in the same directory level as `spam.py`. In this file create a variable called `TARGET_PHONE_NUMBER="9998881234"`. Also create a SSN variable if there is a step to add your SSN during the call (say for customer lookup) `SSN="111223333"`
4. Set up a virtual environment: `python -m venv venv`
5. Install required packages: `pip install -r requirements.txt`
6. Modify the `timed_instructions` list at the top of spam.py to instruct the bot at what conversation time should a key be pressed.
    a. the current list is set for calling the California EDD.
    b. To fill in the instructions for a different process, go through the call process manually, and note down at which times do you have to press which button
    c. the number of tuples in the list is the number of executed button pressed, where the first item in the tuple is the timestamp (m:ss) and the second item is the number to press (or flag)
    d. the `KEYPAD` flag indicates the the keypad button will be clicked, since after initiating a call the keypad goes away and needs to be brough up again
    e. the `SSN` flag will enter your social security number, which you must specify in the .env file in step 4 if desired.
    f. the `END` flag should always be at the end of the instructions list, where the time is how long the call lasted before their automated system ended your call. The script will at this point see if the call ended and redial, or if the call is still alive, notify you with a red window popup and coffin_dance.mp3 playing

7. Have a browser window open with google voice showing. Does not need to be fullscreen, just have enough screen space to view the keypad

## Execution instructions to avoid spamming the government
1. Run: `python spam.py`
2. A window pops up with a capture of your screen asking you to click on the numbers 1 and 5 on your keypad. This is all the manual information needed to register the rest of the keypad.
3. After clicking on the 5, a second screen cap comes up asking you to click on the call button
4. The second window closes and the number begins getting dialed and called, and all numbers will be entered at the given times
5. If the call is still going after the `END` time specified, you will be notified via a pygame red window with text indicating an agent is found, and the `coffin_dance.mp3` song plays loudly to make sure you're aware. If call was ended by target number, the process will repeat ad infinitum until the call is still going after `END` time.

## Notes about this tool that doesn't spam government agencies
1. This can be used for more than just government agencies. Any time you call a service and have to answer questions via keypad input just for them to end the call saying "too many people called try again later".
2. In google voice, the initial keypad location is lower than the keypad location after starting the call. There is a function `move_keypad_locs_for_call_start()` to move the previously recorded pixel locations of keypad digits up by the height of the keypad, as that is what worked on my monitor's resolution. Modify the variable `dy = keypad_locs['0'][1] - keypad_locs['2'][1]` to a pixel value indicating how much the keypad moves upwards when call starts.


### Have fun not finally getting ahold of a live person at whatever company/agency you're struggling with ;)