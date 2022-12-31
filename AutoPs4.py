from sense_hat import SenseHat
import sense_hat
from time import sleep
from random import randint
import asyncio
import Gamepad

pos=1
left_key = sense_hat
right_key = sense_hat.DIRECTION_RIGHT
pressed = sense_hat.ACTION_PRESSED
released = sense_hat.ACTION_RELEASED
sense = SenseHat()
r = (255,0,0)
b = (0,0,0)
g = (0,255,0)
street = [
    b,r,b,b,b,r,b,b,
    b,r,b,b,b,r,b,b,
    b,r,b,b,b,r,b,b,
    b,r,b,b,b,r,b,b,
    b,r,b,b,b,r,b,b,
    b,r,b,b,b,r,b,b,
    b,r,b,g,b,r,b,b,
    b,r,b,g,b,r,b,b
]
pos_auto_i=51
pos_auto_j=59
auto_pos=3
old_pos_i=0
old_pos_j=0
game_over=False
strase=[1,1,1,1,1,1,1,1]


def auto():
    global pos
    global auto_pos
    global game_over
    zahl=0
    events = sense.stick.get_events()
    if events:
        for e in events:
            if e.direction == left_key and e.action == pressed:
                zahl=-1
            if e.direction == right_key and e.action == pressed:
                zahl=1
    global pos_auto_i
    global pos_auto_j
    auto_pos=auto_pos+zahl

    pos_auto_i=auto_pos+48
    pos_auto_j=auto_pos+56
   
    if street[pos_auto_j]==r or street[pos_auto_i]==r:
        print("Strase:",strase)
        print("auto_pos:",auto_pos)
        print("Strasse 6", strase[6], "Strasse 7", strase[7])
        print("pos I:",street[pos_auto_i])
        print("pos j:",street[pos_auto_j])
        game_over=True
    street[pos_auto_j]=g
    street[pos_auto_i]=g

def clear_auto():
    global pos_auto_i
    global pos_auto_j
    street[pos_auto_j]=b
    street[pos_auto_i]=b

def shift():
    global street
    global strase
    for i in range (0,8):
        for j in range (0,7):
            index = 63 - ( 7-i)-(8*j)
            street[index] = street[index-8]
    for i in range (0,8):
        street[i]=b
    for i in range (6,-1,-1):
        strase[i+1]=strase[i]
        print("pos", i, strase[i])

def next():
    global pos
    global street
    global strase
    new_pos = randint(0,2)-1+pos
    if new_pos<0:
        new_pos=0
    if new_pos>3:
        new_pos=3
    pos = new_pos
    street[pos] = r
    street[pos+4] = r
    strase[0]=pos
    print(pos)


async def steet_loop():
    global auto_pos
    global game_over
    while game_over==False:
        sense.set_pixels(street)
        paint_auto(auto_pos)
        shift()
        next()
        await asyncio.sleep(0.4)

def paint_auto(new_pos):
    global auto_pos
    sense.set_pixel(auto_pos, 6, b)
    sense.set_pixel(auto_pos, 7, b)
    auto_pos = new_pos
    sense.set_pixel(auto_pos, 6, g)
    sense.set_pixel(auto_pos, 7, g)


async def auto_loop():
    global game_over
    global gamepad
    global auto_pos
    while game_over==False and gamepad.isConnected():
        dirX = int(gamepad.axis('DPAD-X'))
        #dirY = int(gamepad.axis('DPAD-Y'))
        new_pos = auto_pos + dirX
        paint_auto(new_pos)
        pos_auto_i=auto_pos+48
        pos_auto_j=auto_pos+56
    
        if street[pos_auto_j]==r or street[pos_auto_i]==r:
            print("Strase:",strase)
            print("auto_pos:",auto_pos)
            print("Strasse 6", strase[6], "Strasse 7", strase[7])
            print("pos I:",street[pos_auto_i])
            print("pos j:",street[pos_auto_j])
            game_over=True
        await asyncio.sleep(0.2)

async def main():
    t1 = asyncio.create_task(steet_loop())
    t2 = asyncio.create_task(auto_loop())
    await t1

#while game_over==False:
#    clear_auto()
#    shift()
#    auto()
#    next()
#    sleep(0.3)
print("start")

# Gamepad settings
gamepadType = Gamepad.PS4
# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
# Start the background updating
gamepad.startBackgroundUpdates()
asyncio.run(main())
for k in range (0,2):
    sense.clear(255,0,0)
    sleep(0.2)
    sense.clear(255,255,255)
    sleep(0.2)
sense.show_message("GAME OVER", scroll_speed=0.04)




