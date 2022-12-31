from sense_hat import SenseHat
from time import sleep
from random import randint
import asyncio

L = 0
game_over=False

sense = SenseHat()

async def display_loop():
    global game_over
    while game_over==False:
        sense.clear(255,0,0)
        await asyncio.sleep(0.3)
        sense.clear(255,255,255)
        await asyncio.sleep(0.3)

async def print_loop():
    global L
    global game_over
    while game_over==False:
        await asyncio.sleep(0.1)
        L = L +1
        print("L" , L, "\n")
        if L>=10:
            game_over = True

async def main():
    t1 = asyncio.create_task(display_loop())
    t2 = asyncio.create_task(print_loop())
    await t1
    #await t2

asyncio.run(main())
sense.show_message("GAME OVER", scroll_speed=0.04)
