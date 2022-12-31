from sense_hat import SenseHat
from random import randint
import asyncio
import Gamepad

game_over=False
sense = SenseHat()
r = (255,0,0)
b = (0,0,0)
old_x = 0
old_y = 0
last_x = 0
last_y = 0
gamepad = None
buttonHappy = 'CROSS'
buttonBeep = 'CIRCLE'
buttonExit = 'CROSS'
joystickSpeed = 'LEFT-Y'
joystickSteering = 'RIGHT-X'

async def ps4_loop():
    global game_over
    global gamepad
    global last_x
    global last_y
    while game_over==False and gamepad.isConnected():
        if gamepad.beenPressed('CROSS'):
            print('EXIT')
            game_over=True
        dirX = int(gamepad.axis('DPAD-X'))
        dirY = int(gamepad.axis('DPAD-Y'))
        print("X:",dirX, " Y", dirY) 
        sense.set_pixel(last_x, last_y, b)
        last_x = last_x + dirX
        if last_x < 0:
            last_x = 0
        if last_x > 7:
            last_x = 7
        last_y = last_y + dirY
        if last_y < 0:
            last_y = 0
        if last_y > 7:
            last_y = 7
        print("nX:",last_x, " nY", last_y) 
        sense.set_pixel(last_x, last_y, r)
        await asyncio.sleep(0.2)


async def paint_loop():
    global game_over
    global old_x
    global old_y
    global last_x
    global last_y
    while game_over==False:
        sense.set_pixel(old_x, old_y, b)
        x = randint(0, 7)
        y = randint(0, 7)
        sense.set_pixel(x, y, r)
        old_x = x
        old_y = y
#        sense.set_pixel(last_x, last_y, b)
        await asyncio.sleep(0.5)
    
async def main():
    t1 = asyncio.create_task(paint_loop())
    t2 = asyncio.create_task(ps4_loop())
    await t1
    #await t2

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


print('Gamepad connected')
sense.clear(b)
asyncio.run(main())
gamepad.disconnect()
sense.show_message("GAME OVER", scroll_speed=0.04)
