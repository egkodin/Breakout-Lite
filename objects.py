import random
from settings import *

class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        
        self.id = canvas.create_oval(BALL_SIZE, fill=color) #отрисовка шарика
        self.canvas.move(self.id, *BALL_COORDINATES) #координаты перемещения
        self.canvas_width = self.canvas.winfo_width()

        starts = [-2, -1, 1, 2] # задаём список возможных направлений для старта

        random.shuffle(starts) #перемешали рандомно позиции

        self.x = starts[0] #горизонтально
        self.y = -2 # вертикально

        self.canvas_height = self.canvas.winfo_height() #изменение координат, обозначение высоты, определение по у
        self.canvas_weight = self.canvas.winfo_width() # ширина

        self.hit_bottom = False # узнать не коснулся ли мяч


    def hit_paddle(self, pos): # определяем когда коснется платформы
        paddle_pos = self.canvas.coords(self.paddle.id)
        # условия касания
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:

                self.score.add_point()
                return True

        return False

    def draw(self): # сама отрисовка шарика и платформы
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id) # координаты шарика
        # если шарик падает сверху
        if pos[1] <= 0: # не падает ли вниз
            self.y = self.score.speed_ball_depends_on_score()  # низ

        if pos[3] >= self.canvas_height: # платформа за пределами шарика
            self.hit_bottom = True #игра завершает действие
            self.canvas.create_text(PLACEMENT_GAME_OVER_TEXT, text=GAME_OVER_TEXT, font=COLOR_FONT_TEXT_GAME_OVER, fill=COLOR_GAME_OVER_TEXT) #font шрифт
            
        if self.hit_paddle(pos) == True: #если шарик коснулся платформы
            self.y = -self.score.speed_ball_depends_on_score() # вверх

        if pos[0] <= 0:
            self.x = self.score.speed_ball_depends_on_score() # левая стенка

        if pos[2] >= self.canvas_width: #если будет касаться правой стенки
            self.x = -self.score.speed_ball_depends_on_score()


class Paddle:

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(PADDLE_SIZE, fill=color)

        start_1 = [40, 60, 120, 150, 180, 200]
        random.shuffle(start_1)

        self.start_pos_x = start_1[0]
        self.canvas.move(self.id, self.start_pos_x, 450) #стартовая позиция, всегда сверху 300 px

        self.x = 0 # пока платформа никуда не движется, поэтому изменений по оси х нет
        self.canvas_width = self.canvas.winfo_width() # платформа узнаёт свою ширину

        self.game_started = False

        # движемся вправо 
    def turn_right(self, event):
            # будем смещаться правее на 2 пикселя по оси х 
            self.x = 4

    def turn_left(self, event):
            # будем смещаться левее на 2 пикселя по оси х
            self.x = -4


    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id) #получаем стартовые позиции

        if pos[0] <= 0:
            self.x = 0

        elif pos[2] >= self.canvas_width: # если зашла за границы правого края - stop
            self.x = 0


class Score:

    def __init__(self, canvas, color):

        self.canvas = canvas
        self.score = 0
        self.id = canvas.create_text(PLACEMENT_SCORE, text=self.score, font=COLOR_FONT_TEXT_SCORE, fill=color)

    def speed_ball_depends_on_score(self):
        if self.score > 1 < 3:
            return 3.5
        elif self.score > 3 < 6:
            return 4.5
        else:
            return 2

    def add_point(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score) # пишем новое значение счёта
        self.speed_ball_depends_on_score()








