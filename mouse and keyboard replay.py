from pynput.mouse import Button, Controller as mController,Listener
import keyboard
import time
import sys,os
from threading import Thread
mouse = mController()
double_clk =0
cnfm =0
terminate = 0
no_of_loops =1
sleep_time =0.5
tm =0
lst =[]

is_windows = sys.platform.startswith('win')
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console , colorama
        win_unicode_console.enable()
        colorama.init()
        #Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed, no coloring will be used [Check the readme]")
        G = Y = B = R = W = G = Y = B = R = W = ''

    
else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white

print("""%s

               _ 
     /\       | |
    /  \      | |
   / /\ \ _   | |
  / ____ \ |__| |
 /_/    \_\____/ %s
                     
            """%(G,B))

win_unicode_console.disable()

def get_inputs():
    try:
        global no_of_loops,sleep_time,tm
        tm=float(input("Enter time gap between eache action (0.5 by default)")[:5].strip() or 0.5)
        no_of_loops =float(input("Enter no.of times to repeat (1 by default)")[:5].strip() or 1)
        no_of_loops = int(no_of_loops)
    except:
        tm = 0.5
        no_of_loops = 1
    if tm < 0.1:
        tm = 0.1
    if no_of_loops < 1:
        no_of_loops = 1
    print("default time gap b/w eache action ={} no.of time to repeat ={}".format(tm,no_of_loops))
    sleep_time =tm
    for i in range(6):
        print("KEEP THE SCREEN READY WE WILL START IN {}sec ".format(i),end ='\r')
        time.sleep(1)

def mouse_ctrl(num, action):
    def _mouse(x, y, L_R='L_CLK', clicks=1):
        mouse.position = (int(x),int(y))
        if L_R == 'L_CLK': mouse.click(Button.left, clicks); mouse.release(Button.left)
        else: mouse.click(Button.right, clicks);mouse.release(Button.right)
    try:
        global double_clk
        L_R = action[:5] # get left or right click
        x,y = action[6:].split(' ') # get x and y possitions
        next_action = keys_clicks[num+1] # get the next click 
        if action == next_action and double_clk==0: #double click chk           
            double_clk = 1
        else:
            if double_clk: _mouse(x, y, L_R=L_R, clicks=2)
            else: _mouse(x,y,L_R=L_R,clicks=1)
    except IndexError: _mouse(x,y,L_R=L_R,clicks=1) # if only one input is available in the recordings.txt file 
    except: clrprint('Unknown mouse input', action); time.sleep(1)

def keyboard_ctrl(num, action):    
    try:
        if action[:3] =='Key':  
            if ' ' in action:
                key1,key2 = action.split(' ')
            else:
                key1 = action
                key2 = ''
            if '_l' in key1[-2:] or '_r' in key1[-2:]:
                key1 = key1.replace('_r','')
                key1 = key1.replace('_l','')                
            if "'" in key2:
              ky = key1[4:]+'+'+key2[1]    
            else:
              ky = key1[4:]+'+'+key2[4:]
            if ky[-1]=='+':
                    ky=ky.replace('+','')
            keyboard.press_and_release(ky)
        else:
            keyboard.press_and_release(action[1])
    except:
        print('Unknown Keyboard input',action)
        time.sleep(1)

def lstner():
    def on_scroll(x, y, dx, dy):
        global terminate
        terminate = 1

    with Listener(
    on_scroll=on_scroll) as listener:
        listener.join()  
        
def start():
    try:
        global sleep_time
        t = Thread(target=lstner)
        t.start()
        with open('a.txt','r')as f:
            for k,i in enumerate(f):
                    lst.append(i.strip('\n'))
        for i in range(no_of_loops):
            print(no_of_loops)
            for k,i in enumerate(lst):
                if terminate ==1:
                    input('Press enter to continue')
                    # break
                #print(lst)
                if i =='':
                    pass
                elif i[0] =='<':
                    pass
                elif i[0]=='L' or i[0]=='R':
                    mouse_ctrl(k,i)
                elif i[0]=="'" or i[0]=="\""or i[0]=='K':
                    keyboard_ctrl(k,i)
                elif i[0]=='t':
                    _,val =i.split(' ')
                    sleep_time = float(val)
                time.sleep(sleep_time)
                sleep_time=tm
    except Exception as a:
            time.sleep(1)
while True:
    get_inputs()
    start()
    lst =[]
    cnt = input('press Enter to repeat ...')
    if cnt !='':
        break
