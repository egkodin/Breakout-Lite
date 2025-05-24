import random
from settings import * # Imports all settings, including WIDTH, HEIGHT, etc.

# Calculate BRICK_WIDTH using constants from settings.py
# This makes BRICK_WIDTH available for import by game.py if needed, maintaining previous structure.
BRICK_WIDTH = (WIDTH - (BRICK_COLUMNS + 1) * BRICK_SPACING_X) / BRICK_COLUMNS

class Brick:
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.status = 'active'
        self.id = self.canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline='black')

    def destroy(self):
        self.status = 'destroyed'
        self.canvas.delete(self.id)

    def is_active(self):
        return self.status == 'active'

class Lives:
    def __init__(self, canvas, initial_lives=INITIAL_LIVES, color=LIVES_COLOR, 
                 pos_x=LIVES_TEXT_X, pos_y=LIVES_TEXT_Y, font_style=LIVES_FONT_STYLE):
        self.canvas = canvas
        # Use initial_lives from settings.py as the default
        self.initial_lives = initial_lives 
        self.current_lives = self.initial_lives
        # Use LIVES_TEXT_X, LIVES_TEXT_Y, LIVES_FONT_STYLE, LIVES_COLOR from settings.py as defaults
        self.id = canvas.create_text(pos_x, pos_y, text=f"Lives: {self.current_lives}", font=font_style, fill=color)

    def decrement(self):
        if self.current_lives > 0:
            self.current_lives -= 1
        self.update_display()

    def get_current_lives(self):
        return self.current_lives

    def is_game_over(self):
        return self.current_lives <= 0

    def update_display(self):
        self.canvas.itemconfig(self.id, text=f"Lives: {self.current_lives}")

class Ball:
    def __init__(self, canvas, paddle, score, lives_obj, bricks_list, color): # Added bricks_list
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.lives_obj = lives_obj
        self.bricks_list = bricks_list # Store list of bricks
        
        self.id = canvas.create_oval(BALL_SIZE, fill=color)
        self.initial_coords = BALL_COORDINATES
        self.canvas.move(self.id, *self.initial_coords)
        self.canvas_width = self.canvas.winfo_width()

        starts = [-2, -1, 1, 2]
        random.shuffle(starts)
        self.initial_x_speed = starts[0]
        self.initial_y_speed = -2

        self.x = self.initial_x_speed
        self.y = self.initial_y_speed

        self.canvas_height = self.canvas.winfo_height()
        # self.canvas_weight = self.canvas.winfo_width() # This was canvas_width, already defined

        self.lost_life = False

    def reset(self):
        # Move ball to its initial position
        current_pos = self.canvas.coords(self.id)
        dx = self.initial_coords[0] - current_pos[0]
        dy = self.initial_coords[1] - current_pos[1]
        self.canvas.move(self.id, dx, dy)
        
        # Reset speed
        starts = [-2, -1, 1, 2]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -self.score.speed_ball_depends_on_score() # Start moving up, speed based on score

        self.lost_life = False

    def hit_paddle(self, pos):
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

        if pos[3] >= self.canvas_height:
            self.lost_life = True
            
        if self.hit_paddle(pos) == True:
            self.y = -self.score.speed_ball_depends_on_score()

        if pos[0] <= 0:
            self.x = self.score.speed_ball_depends_on_score()

        if pos[2] >= self.canvas_width:
            self.x = -self.score.speed_ball_depends_on_score()

        # Brick collision detection
        for brick in self.bricks_list:
            if brick.is_active():
                brick_coords = self.canvas.coords(brick.id)
                # Check if brick_coords is valid (it might be empty if deleted improperly)
                if not brick_coords: 
                    continue

                # Ball coordinates: pos[0]=x1, pos[1]=y1, pos[2]=x2, pos[3]=y2
                # Brick coordinates: brick_coords[0]=x1, brick_coords[1]=y1, brick_coords[2]=x2, brick_coords[3]=y2
                
                # Check for overlap
                if pos[2] > brick_coords[0] and pos[0] < brick_coords[2] and \
                   pos[3] > brick_coords[1] and pos[1] < brick_coords[3]:
                    
                    brick.destroy()
                    self.score.add_point()
                    
                    # Determine hit side for more accurate rebound (optional enhancement)
                    # For now, simple Y rebound is fine.
                    # A more advanced check:
                    # Check if the collision is more horizontal or vertical
                    overlap_x1 = max(pos[0], brick_coords[0])
                    overlap_x2 = min(pos[2], brick_coords[2])
                    overlap_y1 = max(pos[1], brick_coords[1])
                    overlap_y2 = min(pos[3], brick_coords[3])
                    
                    overlap_width = overlap_x2 - overlap_x1
                    overlap_height = overlap_y2 - overlap_y1

                    # If the penetration depth in Y is smaller than in X, it's likely a top/bottom hit
                    # Also consider ball's direction
                    
                    # Simple Y rebound for now
                    self.y = -self.y 
                    
                    # More precise rebound:
                    # If (overlap_height < overlap_width) and (self.y > 0 and pos[3] - self.y <= brick_coords[1] or \
                    #    self.y < 0 and pos[1] - self.y >= brick_coords[3]):
                    #     self.y = -self.y # Hit top or bottom
                    # else:
                    #     self.x = -self.x # Hit side

                    break # Process only one brick collision per frame


class Paddle:

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(PADDLE_SIZE, fill=color)

        start_1 = [40, 60, 120, 150, 180, 200]
        random.shuffle(start_1)

        self.initial_x = start_1[0] # Store initial x position
        self.initial_y_offset = 450 # Store initial y offset
        self.canvas.move(self.id, self.initial_x, self.initial_y_offset)

        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        self.game_started = False

    def reset(self):
        current_pos = self.canvas.coords(self.id)
        # Calculate the required movement to go back to initial_x, initial_y_offset
        # Note: paddle moves horizontally, so y of top-left corner (current_pos[1]) should be initial_y_offset
        # And x of top-left corner (current_pos[0]) should be self.initial_x
        
        # Simplified reset: move to stored initial x, assuming y hasn't changed
        # A more robust way would be to calculate exact dx, dy based on current coords and target coords.
        # For paddle, its y position is fixed during move, so we only care about x.
        
        # Get current top-left x
        current_x = current_pos[0]
        # Calculate dx to move to initial_x
        dx = self.initial_x - current_x
        
        self.canvas.move(self.id, dx, 0) # Only move in x
        self.x = 0 # Stop any ongoing movement


        # движемся вправо 
    def turn_right(self, event):
            # будем смещаться правее на 2 пикселя по оси х 
            self.x = 4

    def turn_left(self, event):
            # будем смещаться левее на 2 пикселя по оси х
            self.x = -4


    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0

        elif pos[2] >= self.canvas_width:
            self.x = 0


class Score:

    def __init__(self, canvas, color):

        self.canvas = canvas
        self.score = 0
        # Adjusted placement for score to avoid overlap with lives
        self.id = canvas.create_text(PLACEMENT_SCORE[0] + 100, PLACEMENT_SCORE[1], text=self.score, font=COLOR_FONT_TEXT_SCORE, fill=color)


    def speed_ball_depends_on_score(self):
        if 1 < self.score < 3: # Corrected logic
            return 3.5
        elif 3 <= self.score < 6: # Corrected logic (was >3 <6, now >=3 <6)
            return 4.5
        # Consider adding a base speed for score 0 and 1
        elif self.score >= 6:
            return 5.5 # Added a speed for higher scores
        return 2 # Default speed

    def add_point(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)
        # self.speed_ball_depends_on_score() # Calling this here has no effect, it's called by Ball








