import os, csv, re, time
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import cv2
import numpy as np

import pyautogui, mouse, keyboard
pyautogui.FAILSAFE = True # When mouse is moved to top left, program will exit



current_directory = os.getcwd() + "\\"
width, height = pyautogui.size()
levelup_path = current_directory + "Support_Files\\" + str(height) + "_levelup.png"
victory_path = current_directory + "Support_Files\\" + str(height) + "_victory.png"
defeat_path = current_directory + "Support_Files\\" + str(height) + "_defeat.png"
menu_path = current_directory + "Support_Files\\" + str(height) + "_menu.png"
easter_path = current_directory + "Support_Files\\" + str(height) + "_easter.png"
obyn_hero_path = current_directory + "Support_Files\\" + str(height) + "_obyn.png"
insta_monkey = current_directory + "Support_Files\\" +str(height) + "_instamonkey.png"

button_positions = { # Creates a dictionary of all positions needed for monkeys (positions mapped to 2160 x 1440 resolution)
    "HOME_MENU_START" : [1123, 1248],
    "EXPERT_SELECTION" : [1778, 1304],
    "RIGHT_ARROW_SELECTION" : [2193, 582],
    "DARK_CASTLE" : [1420, 350], # changed to (x=1941, y=513) in latest patch
    "HARD_MODE" : [1729, 562],
    "CHIMPS_MODE" : [2139, 980],
    "STANDARD_GAME_MODE" : [847,780],
    "OVERWRITE_SAVE" : [1520, 974],
    "VICTORY_CONTINUE" : [1283, 1215],
    "VICTORY_HOME" : [939, 1124],
    "EASTER_COLLECTION" : [1279, 911],
    "F_LEFT_INSTA" : [868, 722],
    "F_RIGHT_INSTA" : [1680, 722],
    "LEFT_INSTA" : [1074, 725],
    "RIGHT_INSTA" : [1479, 724],
    "MID_INSTA" : [1276, 727],
    "EASTER_CONTINUE" : [1280, 1330],
    "EASTER_EXIT" : [100, 93],
    "QUIT_HOME" : [1126, 1135],
    "HERO_SELECT" : [799, 1272],
    "SELECT_OBYN" : [],
    "CONFIRM_HERO" : [855, 893],
    "TARGET_BUTTON_MORTAR": [1909, 491],
    "ABILLITY_ONE": [253, 1379],
    "ABILLITY_TWO": [369, 1377],
    "FREEPLAY" : [1611, 1112],
    "OK_MIDDLE" : [1280, 1003],
    "RESTART": [1413, 1094],
    "CONFIRM_CHIMPS" : [1481, 980]

}



monkeys = {
    "DART" : "q",
    "BOOMERANG" : "w",
    "BOMB" : "e",
    "TACK" : "r",
    "ICE" : "t",
    "GLUE" : "y",
    "SNIPER" : "z",
    "SUBMARINE" : "x",
    "BUCCANEER" : "c",
    "ACE" : "v",
    "HELI" : "b",
    "MORTAR" : "n",
    "DARTLING" : "m",
    "WIZARD" : "a",
    "SUPER" : "s",
    "NINJA" : "d",
    "ALCHEMIST" : "f",
    "DRUID" : "g",
    "BANANA" : "h",
    "ENGINEER" : "l",
    "SPIKE" : "j",
    "VILLAGE" : "k",
    "HERO" : "u"
}

upgrade_keybinds = {
    "top" : ",",
    "middle" : ".",
    "bottom" : "/"

}

reso_16 = [
    {
        "width": 1280,
        "height": 720        
    },
    {
        "width": 1920,
        "height": 1080
    },
    {
        "width": 2560,
        "height": 1440
    },
    {
        "width": 3840,
        "height": 2160
    }
]


def padding():
# Get's width and height of current resolution
# we iterate through reso_16 for heights, if current resolution height matches one of the entires 
# then it will calulate the difference of the width's between current resolution and 16:9 (reso_16) resolution
# divides by 2 for each side of padding

# Variables Used
#   width -- used to referance current resolution width
#   height -- used to referance current resolution height
#   pad -- used to output how much padding we expect in different resolutions
#   reso_16 -- list that  
    width, height = pyautogui.size()
    pad = 0
    for x in reso_16: 
        if height == x['height']:
            pad = (width - x['width'])/2
    #print("I have been padding -- " + str(pad))

    return pad

def scaling(pos_list):
# This function will dynamically calculate the differance between current resolution and designed for 2560x1440
# it will also add any padding needed to positions to account for 21:9 

# do_padding -- this is used during start 
    reso_21 = False
    width, height = pyautogui.size()
    for x in reso_16: 
        if height == x['height']:
            if width != x['width']:
                reso_21 = True
                x = pos_list[0]
                break
    if reso_21 != True:
        x = pos_list[0]/2560 
        x = x * width
    y = pos_list[1]/1440
    y = y * height
    #print(" Me wihout padding " + str([x]))
    x = x + padding() # Add's the pad to to the curent x position variable
    #print(" Me with padding -- " + str([x]))
    return (x, y)



def move_mouse(location):
    pyautogui.moveTo(location)
    time.sleep(0.1)

def click(location): #pass in x and y, and it will click for you
    #print(location)
    # mouse.move(*scaling(button_positions[location]))
    # x, y = location
    # mouse.move(*location)
    move_mouse(scaling(location))
    mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
    time.sleep(0.5)

def button_click(btn):
    #print(location)
    # x, y = location
    # mouse.move(*location)
    move_mouse(scaling(button_positions[btn]))
    mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
    time.sleep(0.5)

def press_key(key):
    keyboard.press_and_release(key)
    time.sleep(0.1)

def getRound():
    top, left = scaling([1880, 35])
    width, height = scaling([195, 65])
    img = pyautogui.screenshot(region=(top, left, width, height))
    
    numpyImage = np.array(img)

    # Make image grayscale using opencv
    greyImage = cv2.cvtColor(numpyImage, cv2.COLOR_BGR2GRAY)

    # Threasholding
    final_image = cv2.threshold(greyImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
   
    # Get current round from image with tesseract
    text = pytesseract.image_to_string(final_image,  config='--psm 7').replace("\n", "")

    # regex to look for format [[:digit:]]/[[:digit:]] if not its not round, return None
    if re.search(r"(\d+/\d+)", text):
        print(text)
        text = text.split("/")
        text = tuple(map(int, text))
        return text
    else:
        return None


# Fixar om cordinater till sträng
def fixPositionFormated(posString):
    fixed = posString.split(", ")

    return tuple(map(int, fixed))


def formatData():
    formatedInstructions = []
    with open("instructions.csv") as file:
        csvreader = csv.DictReader(file)
        
        for row in csvreader:
            row["POSITION"] = fixPositionFormated(row["POSITION"])

            if row["TARGET_POS"] != "-":
                row["TARGET_POS"] = fixPositionFormated(row["TARGET_POS"])
            
            
            formatedInstructions.append(row)
    return formatedInstructions
    # pprint(formatedInstructions)

def handleInstruction(instruction):
    # print(instruction)
    upgrade_path = instruction["UPGRADE_DIFF"]
    
    monkey_position = instruction["POSITION"]
    target = instruction["TARGET"]
    keybind = instruction["KEYCODE"]


    # OM det inte finns någon upgrade så finns inte tornet placera ut
    if upgrade_path == "-":
        press_key(keybind)

        click(monkey_position)
        # press_key("esc")
    else:
        click(monkey_position)
        upgrade_path = upgrade_path.split("-")
        top, middle, bottom = tuple(map(int, upgrade_path))
        
        for _ in range(top):
            press_key(upgrade_keybinds["top"])

        for _ in range(middle):
            press_key(upgrade_keybinds["middle"])

        for _ in range(bottom):
            press_key(upgrade_keybinds["bottom"])

        
        print(instruction["MONKEY"], instruction["UPGRADE"], "diff -", instruction["UPGRADE_DIFF"])

        press_key("esc")


    # Om target är - så låt vara
    # Special case för mortar 
    if instruction["TARGET_POS"] != "-":
        print("clicka på mortar")
        
        pyautogui.moveTo(scaling(monkey_position))
        time.sleep(0.5)
        mouse.click(button="left")

        time.sleep(1)

        pyautogui.moveTo(scaling(button_positions["TARGET_BUTTON_MORTAR"]))
        
        time.sleep(1)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        pyautogui.moveTo(scaling(instruction["TARGET_POS"]))
        time.sleep(0.5)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        press_key("esc")

    if instruction["ROUND_START"] == "TRUE":
        press_key("space")
        press_key("space")


        # Om den har en specifik target
    if target != "-":
        splitTarget = target.split(", ")

        # special cases
        if target == "STRONG":
            click(monkey_position)
            press_key("ctrl+tab")
            press_key("esc")
        elif len(splitTarget) > 1:
            click(monkey_position)
            press_key("tab")
            time.sleep(3)
            press_key("ctrl+tab")
            press_key("ctrl+tab")
            press_key("esc")
        elif target == "CLOSE":
            click(monkey_position)
            press_key("tab")            
            press_key("esc")


def check_levelup():

    found = pyautogui.locateOnScreen(levelup_path, confidence=0.9)

    if found:
        print("level up detected")
        return True
    else:
        return False
        
    

def easter_event_check():
    found = pyautogui.locateOnScreen(easter_path, confidence=0.9)
    if found != None:
        print("easter collection detected")
        button_click("EASTER_COLLECTION") #DUE TO EASTER EVENT:
        time.sleep(1)
        button_click("LEFT_INSTA") # unlock insta
        time.sleep(1)
        button_click("LEFT_INSTA") # collect insta
        time.sleep(1)
        button_click("RIGHT_INSTA") # unlock r insta
        time.sleep(1)
        button_click("RIGHT_INSTA") # collect r insta
        time.sleep(1)
        button_click("F_LEFT_INSTA")
        time.sleep(1)
        button_click("F_LEFT_INSTA")
        time.sleep(1)
        button_click("MID_INSTA") # unlock insta
        time.sleep(1)
        button_click("MID_INSTA") # collect insta
        time.sleep(1)
        button_click("F_RIGHT_INSTA")
        time.sleep(1)
        button_click("F_RIGHT_INSTA")
        time.sleep(1)

        time.sleep(1)
        button_click("EASTER_CONTINUE")


        # awe try to click 3 quick times to get out of the easter mode, but also if easter mode not triggered, to open and close profile quick
        button_click("EASTER_EXIT")
        time.sleep(1)
        
def hero_obyn_check():
    found = pyautogui.locateOnScreen(obyn_hero_path, confidence=0.9)
    if not found:
        button_click("HERO_SELECT")
        button_click("SELECT_OBYN")
        button_click("CONFIRM_HERO")
        press_key("esc")

def victory_check():
    found = pyautogui.locateOnScreen(victory_path, confidence=0.9)
    #jprint(victory_path)
    if found:
        return True
    else:
        return False

def defeat_check():     
    #jprint(defeat_path)
    found = pyautogui.locateOnScreen(defeat_path, confidence=0.9)
    if found:
        return True
    else:
        return False

def exit_level():
    
    button_click("VICTORY_CONTINUE")
    time.sleep(2)
    button_click("VICTORY_HOME")
    time.sleep(4)

    easter_event_check()
    time.sleep(2)

def select_map():
    time.sleep(2)

    button_click("HOME_MENU_START") # Move Mouse and click from Home Menu, Start
    button_click("EXPERT_SELECTION") # Move Mouse to expert and click
    button_click("RIGHT_ARROW_SELECTION") # Move Mouse to arrow and click
    button_click("DARK_CASTLE") # Move Mouse to Dark Castle
    button_click("HARD_MODE") # Move Mouse to select easy mode
    button_click("CHIMPS_MODE") # Move mouse to select Standard mode
    button_click("OVERWRITE_SAVE") # Move mouse to overwrite save if exists
    time.sleep(3)
    button_click("CONFIRM_CHIMPS")

def menu_check():
    #jprint(menu_path)
    found = pyautogui.locateOnScreen(menu_path, confidence=0.9)
    if found:
        return True
    else:
        return False

def insta_monkey_check():
    found = pyautogui.locateOnScreen(insta_monkey, confidence=0.9)
    if found: 
        return True
    else:
        return False

def main_game(instructions):
    # uppdelade_upgrades_per_apa = defaultdict(dict)
    # # delar upp alla upgraderingar för sig per apa
    # for idx, instruction in enumerate(instructions):
    #     if instruction["UPGRADE"] != "-":
    #         if len(uppdelade_upgrades_per_apa[instruction["MONKEY"]]) > 0:
    #             uppdelade_upgrades_per_apa[instruction["MONKEY"]].append(instruction["UPGRADE"])
                
    #         else: 
    #             uppdelade_upgrades_per_apa[instruction["MONKEY"]] = [ instruction["UPGRADE"] ]

    # # För varje upgrade per apa
    # for monkey_upgrade in uppdelade_upgrades_per_apa.values():
    #     if len(monkey_upgrade) > 1: # Hoppa ifall det bara är en upgrade på den apan
    #         for index in range(len(monkey_upgrade)): # ifall index av listan är 0 hoppa
    #             if index != 0:
    #                 # Senaste och nuvarande uppgradeing splitar ut alla -
    #                 last_upgrade = monkey_upgrade[index -1].split("-")
    #                 upgrade = monkey_upgrade[index].split("-")

    #                 # mappar om str till int i upgrade listorna
    #                 top_last, middle_last, bottom_last = tuple(map(int, last_upgrade))
    #                 top, middle, bottom = tuple(map(int, upgrade))

    #                 # Hittar diffen mellan förra uppgradering och nuvarande uppgraderingen
    #                 diff = "{}-{}-{}".format(abs(top-top_last), abs(middle-middle_last), abs(bottom-bottom_last))
                    
    #                 print(last_upgrade, upgrade, diff)
                    
    #                 # Ändrar monkey_upgrade
    #                 monkey_upgrade[index] = diff
    current_round = None
    prev = time.time()

    # VÄLDIGT VIKTIGT https://stackoverflow.com/questions/10665591/how-to-remove-list-elements-in-a-for-loop-in-python#10665602 
    for inst in instructions[:]:
        # Check for levelup
        check_levelup()

        while int(inst['ROUND']) != current_round:
            time.sleep(0.2)

            if getRound():
                    current_round, _ = getRound()
            else:
                current_round = -1


            # Insta monkey popup check
            if insta_monkey_check():
                mouse.click(button='left')
                mouse.click(button='left')
            
            # Check for levelup
            if check_levelup():
                button_click("LEFT_INSTA") # Accept lvl
                time.sleep(1)
                button_click("LEFT_INSTA") # Accept knoledge
                time.sleep(1)

                button_click("LEFT_INSTA") # unlock insta
                time.sleep(1)
                button_click("LEFT_INSTA") # collect insta
                time.sleep(1)

                button_click("MID_INSTA") # unlock insta
                time.sleep(1)
                button_click("MID_INSTA") # collect insta
                time.sleep(1)

                button_click("RIGHT_INSTA") # unlock r insta
                time.sleep(1)
                button_click("RIGHT_INSTA") # collect r insta
                #press_key("space") # Fast forward the game

            # Check for finished or failed game
            if defeat_check() or victory_check():
                print("finished detected.. exiting level")
                exit_level()
                return 1

            # print("waiting:", inst['ROUND'], "current_round:", current_round)

            # Saftey net; use abilites every five seconds
            if time.time()-prev >= 5:
                # Leta efter Defeat

                if current_round >= 39:
                    click(button_positions["ABILLITY_ONE"])
                
                if current_round >= 51:
                    click(button_positions["ABILLITY_TWO"])

                prev = time.time()

            continue
        else:
            handleInstruction(inst)


def main():

    print("waiting for 5 seconds, please select the btd 6 window")
    time.sleep(5)
    # Check for obyn
    fixed_instructions = formatData()
    while True:
        print("selecting map")
        # choose map
        select_map()   

        print("Game start")
        # main game
        main_game(fixed_instructions)

    # print(getRound())



if __name__ == "__main__":
    main()