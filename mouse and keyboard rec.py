from pynput import mouse
from pynput.keyboard import Key, Listener
from pynput import keyboard
import time,sys,os
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
                 
        >>> FOR EACH AND EVERY ACTION THERE WILL BE A DELAY OF 0.5 sec BY DEFAULT. YOU CAN CHANGE IT WHILE REPLAYING ACTIONS 
            IN CONTROLLER 
        >>> YOU CAN ALSO ADD ADDITIONAL TIME FOR A PARTICULER ACTION USING ctrl + ` (Negation Key) 
        >>> APPLICATION WILL START RECORDING MOUSE AND KEYBOARD ACTIONS IN 5sec AFTER THE ENTRY OF INPUTS
        >>> NOTE: Ctrl+C is accepted but ctrl+alt+a/del are not accepted Only 2 combination of keys are accepted
        >>> Plz contribute and give your valuable feedback and comments, so that I can come up with future updates...
        
        """%(G,B))
win_unicode_console.disable()

try:
    extradelay = float(input("ctrl_l + ` Key will add given delay to next action (1 by default): ")[:5].strip() or 1)
    if float(extradelay) < 0.1:
        extradelay = 1
    else:
        extradelay = float(extradelay[:5])
    append_wright = input('Do you want to attach these with previous actions saved (Y/N) (default NO):  ')[:1].strip()
    print(append_wright)
    if append_wright =='y' or append_wright =='Y' :
        append_wright = 'a'
    else:
        append_wright = 'w'
except Exception as a:
    extradelay = 1
    append_wright = 'w'

print("delay to next action when ctrl_l + ` is pressed={}".format(extradelay))

os.system('mode con: cols=20 lines=10')

for i in range(6):
    print(i,end ='\r')
    time.sleep(1)

print('')
    
def save(key):
    global append_wright
    if key =="Key.esc":
        listener.stop()
    else:
        if key =="Key.ctrl_l ['`']" or key =="Key.ctrl_l '`'":
            key = 'time '+str(extradelay)
        with open('a.txt',append_wright)as f:
            f.write(str(key)+'\n')
            print(str(key))
        append_wright = 'a'

def on_press(key):
    global lst
    if len(str(key)) > 3:
        a = str(key)+' pressed'
        lst.append(a)  

def on_release(key):
    global lst
    try:
        if 'pressed' in lst[0]:
            key = lst[0].strip('pressed')+str(key)
            a,b =key.split(' ') 
            if a==b:
                key = a                
                save(key)
            else:
                save(str(key))
        lst=[]  
    except:
        if len(str(key))<4:
            save(str(key))
        else:
            pass

def on_click(x, y, button, pressed):
    if pressed == False:
        pass
    else:
        if button == mouse.Button.left:
            x = str(x)
            y = str(y)
            point_click = 'L_CLK '+x+' '+y
            save(point_click)
        if button == mouse.Button.right:
            x = str(x)
            y = str(y)
            point_click = 'R_CLK '+x+' '+y
            save(point_click)
        if button == mouse.Button.middle:
            pass
def on_scroll(x, y, dx, dy):
    pass

with mouse.Listener(on_click=on_click,on_scroll=on_scroll) as listener:
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
