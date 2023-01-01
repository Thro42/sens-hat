import sense_hat
from sense_hat import SenseHat
from time import sleep
from random import randint
import asyncio
import Gamepad
import _thread
import threading
from threading import Thread

r=(255,0,0)
b=(0,0,0)
g=(0,255,0)
e=(0,0,255)

class Game():
    bullets = []
    enemys = []
    tokill = []
    score = 0

    def __init__(self):
        self.sense = SenseHat()
        self.game_over=False
        self.sense.clear(b)
        self.game_exit=False
        # Gamepad settings
        gamepadType = Gamepad.PS4
        # Wait for a connection
        if not Gamepad.available():
            print('Please connect your gamepad...')
            while not Gamepad.available():
                sleep(1.0)
        self.gamepad = gamepadType()
        # Start the background updating
        self.gamepad.startBackgroundUpdates()

    def addToKill(self,task):
        self.tokill.append(task)

    def removeTask(self,task):
        self.tokill.remove(task)

    def setPlayer(self, player):
        self.player = player
    def addBullet(self, bullet):
        self.bullets.append(bullet)
#        print(len(self.bullets))
    def deleteBullet(self, bullet):
        self.bullets.remove(bullet)
#        print(len(self.bullets))
        self.addToKill(bullet)
    def addEnemy(self, enemy):
        self.enemys.append(enemy)
#        print("enemys:",len(self.enemys))
    def killEnemy(self, enemy):
        enemy.life = False
        try:
            if enemy in self.enemys:
                self.enemys.remove(enemy)
        finally:
            enemy.kill()
        self.addToKill(enemy)
        print("Kill E:",len(self.enemys))
        self.score += 1
    def checkHit(self, bullet):
        for e in self.enemys:
            if bullet.xPos == e.xPos and bullet.yPos == e.yPos:
                self.killEnemy(e)
                e.kill()
                bullet.kill()
    def enemyHit(self,enemy):
        for b in self.bullets:
            if b.xPos == enemy.xPos and b.yPos == enemy.yPos:
                self.killEnemy(enemy)
                enemy.kill()
                b.kill()

class GameLoop(Thread):
    def __init__ (self, game):
        Thread.__init__(self)
        self.game = game
        self.sense = game.sense
        self.gamepad = game.gamepad

    def run(self):
        while self.game.game_exit == False:
            self.game.score = 0
            newPlayer = Player(game)
            game.setPlayer(newPlayer) 
            newPlayer.start()
            self.gameLoop()
            newPlayer.join()
            self.gameEnd()

    def gameLoop(self):
        enemyWait = 10
        while self.game.game_over == False:
            enemyWait -= 1
            for b in self.game.bullets:
                if b.life == False:
                    self.game.deleteBullet(b)
            for e in self.game.enemys:
                if e.life == False:
                    self.game.killEnemy(e)
            for t in self.game.tokill:
                t.join
                self.game.removeTask(t)
            if len(self.game.enemys) < 4 and enemyWait > 0:
                enemyWait = 100
                newEnemy = Enemy(self.game)
                self.game.addEnemy(newEnemy)
                newEnemy.start()
            sleep(0.1)

    def gameEnd(self):
        for e in self.game.enemys:
            e.kill()
            self.game.killEnemy(e)
        for b in self.game.bullets:
            b.kill()
            self.game.deleteBullet(b)
        for t in self.game.tokill:
            t.join
            self.game.removeTask(t)
        self.sense.show_message("GAME OVER", scroll_speed=0.04)
        msg = "SCORE " + str(self.game.score) + " pts!"
        print(msg)
        self.sense.show_message(msg, scroll_speed=0.04)
        while self.game.game_over == True and self.game.game_exit == False:
            if self.gamepad.isPressed('CIRCLE'):
                self.game.game_exit = True
            if self.gamepad.isPressed('CROSS'):
                self.game.game_over = False


class Enemy(Thread):
    def __init__ (self, game):
        Thread.__init__(self)
        self.xPos = randint(0, 7)
        self.yPos = 0
        self.game = game
        self.sense = game.sense
        self.life = True

    def kill(self):
        print("Kill Me", self.ident)
        self.life = False
    def run(self):
        while self.game.game_over == False and self.yPos < 7 and self.life == True:
            self.sense.set_pixel(self.xPos, self.yPos, b)
            if self.life == True:
                self.yPos += 1
#            print("Feint an:",self.yPos)
            if self.yPos >= 7 and self.life == True:
                self.game.addToKill(self)
                self.game.game_over = True
            else:
                self.sense.set_pixel(self.xPos, self.yPos, e)
            if self.life == True and self.game.game_over == False:
                sleep(1)
            print("Runn Enemy",self.ident)
            self.game.enemyHit(self)
        print("Stop Enemy")

class Bullet(Thread):
    def __init__ (self, game):
        Thread.__init__(self)
        self.xPos = game.player.position
        self.yPos = 6
        self.game = game
        self.sense = game.sense
        self.life = True
    def kill(self):
        print("Kill Bullet", self.ident)
        self.life = False
    def run(self):
        while self.game.game_over == False and self.yPos >= 0 and self.life == True:
            self.sense.set_pixel(self.xPos, self.yPos, b)
            self.yPos -= 1
            if self.yPos < 0:
                self.game.deleteBullet(self)
                #Thread.stop_thread(self)
            else:
                self.sense.set_pixel(self.xPos, self.yPos, r)
                self.game.checkHit(self)
            sleep(0.5)
        print("Stop Bullet")

class Player(Thread):

    def __init__ (self, game):
        Thread.__init__(self)
        self.position = 3
        self.game = game
        self.sense = game.sense
        self.gamepad = game.gamepad
    
    def paint_player(self, new_pos):
        self.sense.set_pixel(self.position, 6, b)
        self.sense.set_pixel(self.position, 7, b)
        self.position = new_pos
        self.sense.set_pixel(self.position, 6, g)
        self.sense.set_pixel(self.position, 7, g)

    def run(self):
        while self.game.game_over == False:
            dirX = int(self.gamepad.axis('DPAD-X'))
            new_pos = self.position + dirX
            if new_pos < 0:
                new_pos = 0
            if new_pos > 7:
                new_pos = 7
            self.paint_player(new_pos)
            if self.gamepad.isPressed('CIRCLE'):
                self.game.game_over = True
            if self.gamepad.isPressed('R1'):
#                print("BUMM")
                bullet = Bullet(self.game)
                self.game.addBullet(bullet)
                bullet.start()
            sleep(0.2)
        print("Stop Payer")
#        Thread.stop_thread(self)



game = Game()
#newPlayer = Player(game)
#game.setPlayer(newPlayer)
#newPlayer.start()    

gameloop = GameLoop(game)
gameloop.start()
gameloop.join()
#newPlayer.join()