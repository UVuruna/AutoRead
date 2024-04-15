import pyautogui
import time
import cv2
import pytesseract
import numpy as np
import keyboard
import threading

# Backend Part
XY_start = 'x'
Y_bottom = 'y'
XY_LeftTime = 'n'
XY_RightTime = 'm'
ColorLink = 'c'
ScrollMore = 'f'
ScrollLess = 'r'
END = False
time_toEND = 2 #sec (lower will quit faster, bigger will use less resources cause it loops to check state of END bool)

X,Y,x1,x2,y1,y2,Y_end=0,0,0,0,0,0,0
color_LINK = (48, 51, 52)
Scroll = 0

def Program():
    global Y,END
    pyautogui.scroll(4000)
    pyautogui.scroll(-Scroll)
    while Y<Y_end and not END:
        Y+=1
        pyautogui.moveTo(X,Y)
        color = pyautogui.pixel(X, Y)
        if color == color_LINK:  
            pyautogui.click(X,Y)
            time.sleep(2)
            screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            text = pytesseract.image_to_string(cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR))
            try:
                print(text)
                vremeS = int(text[-3:])
                vremeM = int(text[-6:-4])
                waitTime = vremeM*60+vremeS
                print(waitTime)
                time.sleep(waitTime)
                pyautogui.scroll(4000)
                pyautogui.scroll(-Scroll)
                continue
            except ValueError:
                pyautogui.scroll(4000)
                pyautogui.scroll(-Scroll)
                continue
        else:
            continue
    else:
        print('Uspesno Zavrseno !!!')
        END = True

def Start(e):
    global MainJob
    if e.event_type == keyboard.KEY_DOWN and Y_end!=0 and \
        X!=0 and Y!=0 and x1!=0 and x2!=0 and y1!=0 and y2!=0:
        print("\nProgram je pokrenut")
        MainJob = threading.Thread(target=Program)
        MainJob.start()
    else:
        text = ''
        text += f"X start: {X}  -- button: {XY_start}\n" if X==0 else ''
        text += f"Y start: {Y}  -- button: {XY_start}\n" if Y==0 else ''
        text += f"x1 (bottom-left): {x1}  -- button: {XY_LeftTime}\n" if x1==0 else ''
        text += f"y1 (bottom-left): {y1}  -- button: {XY_LeftTime}\n" if y1==0 else ''
        text += f"x2 (bottom-right): {x2}  -- button: {XY_RightTime}\n" if x2==0 else ''
        text += f"y2 (bottom-right): {y2}  -- button: {XY_RightTime}\n" if y2==0 else ''
        text += f"Y bottom: {Y_end}  -- button: {Y_bottom}\n" if Y_end==0 else ''
        print("\n\tNiste uneli sve koordinate\n"+text)
keyboard.on_press_key('s', Start)

def XY_Start(e):
    global X,Y   
    if e.event_type == keyboard.KEY_DOWN:
        X, Y = pyautogui.position()
        print(f"\nX po koje se krece strelica je: {X},\nPocetni Y je:   {Y}")
keyboard.on_press_key(XY_start, XY_Start)

def Left_XY_Time(e):
    global x1,y1
    if e.event_type == keyboard.KEY_DOWN and e.name==XY_LeftTime: # Ovaj AND da ne bi mesao Z i Y mozda zbog Serbian(Latin) i US tastature
        x1, y1 = pyautogui.position()
        print(f"\nX1:Y1 leva gornja ivica Timera: {x1}:{y1}")
keyboard.on_press_key(XY_LeftTime, Left_XY_Time)

def Right_XY_Time(e):
    global x2,y2
    if e.event_type == keyboard.KEY_DOWN:
        x2, y2 = pyautogui.position()
        print(f"\nX2:Y2 desna donja ivica Timera: {x2}:{y2}")
keyboard.on_press_key(XY_RightTime, Right_XY_Time)

def Y_Bottom(e):
    global Y_end
    if e.event_type == keyboard.KEY_DOWN:
        x, Y_end = pyautogui.position()
        print(f"\nKraj strane, Y: {Y_end}")
keyboard.on_press_key(Y_bottom, Y_Bottom)

def get_Color(e):
    global color_LINK
    if e.event_type == keyboard.KEY_DOWN:
        x,y = pyautogui.position()
        color_LINK = pyautogui.pixel(x,y)
        print(f"\nBoja linka je: {color_LINK}\n"+
              "Za Link Elearning treba da bude: (48, 51, 52)")
keyboard.on_press_key(ColorLink, get_Color)

def Scroll_more(e):
    global Scroll
    if e.event_type == keyboard.KEY_DOWN:
        pyautogui.scroll(4000)
        Scroll +=50
        pyautogui.scroll(-Scroll)
keyboard.on_press_key(ScrollMore, Scroll_more)

def Scroll_less(e):
    global Scroll
    if e.event_type == keyboard.KEY_DOWN:
        pyautogui.scroll(2000)
        Scroll -=50
        pyautogui.scroll(-Scroll)
keyboard.on_press_key(ScrollLess, Scroll_less)

def END_Program(e):
    global END
    if e.event_type == keyboard.KEY_DOWN:
        END = True
        print(f"Ending Program: {END} in less then {time_toEND} sec")
keyboard.on_press_key('esc', END_Program)

print(f"\n\nPress {XY_start} for TOP coordinates\n"
      +f"Press {Y_bottom} for BOTTOM coordinate Y\n"
      +f"Press {XY_LeftTime} for TOP-LEFT Timer coordinates\n"
      +f"Press {XY_RightTime} for BOTTOM-RIGHT Timer coordinates\n\n"

      +"\tOptional:\n"
      +f"Press {ScrollMore} for increase Scroll Down\n"
      +f"Press {ScrollLess} for decrease Scroll Down\n"
      +f"Press {ColorLink} for changing LINK Color\n\n")

while not END:
    time.sleep(time_toEND)
    pass
else:
    try:
        MainJob.join()
        print("Program Ended")
    except NameError:
        print("Program didnt Start correctly")