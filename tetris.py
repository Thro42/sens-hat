import sense_hat
from sense_hat import SenseHat
from time import sleep
from random import randint
import asyncio
import Gamepad

r=(255,0,0)
b=(0,0,0)
g=(0,255,0)
pos=1

space=[
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,g,b,b,b,b,
    b,b,b,g,b,b,b,b
]
strase=[1,1,1,1,1,1,1,1]
game_over=False
game_finish=False
score=0
pos_auto_j=59
auto_pos=3
old_pos_i=0
old_pos_j=0