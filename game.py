from tkinter import *
import time

from settings import *
from objects import *


class Game:
    def __init__(self, tk, canvas):
        self.tk = Tk() #объект ткинтера, наше игровое поле
        self.canvas = canvas

        self.paddle = Paddle(self.canvas, PADDLE_COLOR)
        self.score = Score(self.canvas, COLOR_SCORE)
        self.ball = Ball(self.canvas, self.paddle, self.score, COLOR_BALL)
 

        self.canvas.bind_all("<KeyPress-Right>", self.paddle.turn_right) 
        self.canvas.bind_all("<KeyPress-Left>", self.paddle.turn_left)  
        self.canvas.bind_all("<KeyPress-Return>", self.start_game) 
    
        self.game_started = False

    def start_game(self, event):
        self.game_started = True

    def run_game(self):
        while not self.ball.hit_bottom:
            if self.start_game:
                self.ball.draw() 
                self.paddle.draw()

            self.tk.update_idletasks() #дорисовка
            self.tk.update() #обновление самого окна
            
            time.sleep(0.01) #плавность движений, с небольшой задержкой

        time.sleep(3)