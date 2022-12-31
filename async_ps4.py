from sense_hat import SenseHat
from random import randint
import asyncio
from pyPS4Controller.controller import Controller

game_over=False
sense = SenseHat()
r = (255,0,0)
b = (0,0,0)
old_x = 0
old_y = 0

class MyController(Controller):
    last_x = 3
    last_y = 3
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_left_arrow_press():
        sense.set_pixel(self.last_x, self.last_y, b)
        self.last_x -= 1
        sense.set_pixel(self.last_x, self.last_y, r)
        
    def on_right_arrow_press():
        sense.set_pixel(self.last_x, self.last_y, b)
        self.last_x -= 1
        sense.set_pixel(self.last_x, self.last_y, r)
    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
        global game_over
        print("Goodbye world")
        game_over=True

async def ps4_loop():
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    global game_over
    while game_over==False:
        controller.listen(timeout=1)    
        await asyncio.sleep(0.5)


async def paint_loop():
    global game_over
    while game_over==False:
        sense.set_pixel(old_x, old_y, b)
        x = randint(0, 8)
        y = randint(0, 8)
        sense.set_pixel(x, y, r)
        old_x = x
        old_y = y
        await asyncio.sleep(0.5)
    
async def main():
    t1 = asyncio.create_task(paint_loop())
    t2 = asyncio.create_task(ps4_loop())
    await t1
    #await t2

asyncio.run(main())
sense.show_message("GAME OVER", scroll_speed=0.04)
