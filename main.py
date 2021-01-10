from tkinter import *
import time

from settings import *
from objects import *
from game import *
from PIL import Image, ImageTk

tk = Tk() #объект ткинтера, наше игровое поле

tk.title(GAME_NAME)
tk.resizable(0,0) # чтобы окно не дивгалось
tk.wm_attributes('-topmost', 1) #чтобы ничего не перекрывалось, был поверх всех форм

canvas = Canvas(tk, width=WIDTH, height=HEIGHT, highlightthickness=0) #высота, ширина обводка в рамке
#canvas.pack() # указываем, что есть координаты

img = Image.open('2.gif') # Открываем картинку
img = img.resize((WIDTH, HEIGHT)) # Изменяем размер картинки
img_tk = ImageTk.PhotoImage(img) # Создаём PhotoImage
canvas.create_image(WIDTH // 2, HEIGHT // 2, image=img_tk) # Рисуем картинку


canvas.pack()

tk.update() #обновление после отрисовки


game = Game(tk, canvas)

if __name__ == '__main__':
    game.run_game()





