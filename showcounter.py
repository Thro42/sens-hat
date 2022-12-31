from sense_hat import SenseHat
from time import sleep
from random import randint
import asyncio
from pynput import keyboard


L = 0
game_over=False

sense = SenseHat()

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

async def display_loop():
    global game_over
    while game_over==False:
        sense.clear(255,0,0)
        await asyncio.sleep(0.3)
        sense.clear(255,255,255)
        await asyncio.sleep(0.3)

async def print_loop():
    global game_over
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    while game_over==False:
        L = L + 1

        
async def main():
    t1 = asyncio.create_task(display_loop())
    t2 = asyncio.create_task(print_loop())
    await t1
    #await t2

asyncio.run(main())
sense.show_message("GAME OVER", scroll_speed=0.04)
