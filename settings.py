#base
GAME_NAME = 'Breakout Lite'
WIDTH = 500
HEIGHT = 500
#ball
BALL_SIZE = 10, 10, 25, 25
BALL_COORDINATES = 250, 100
COLOR_BALL = 'pink'
COLOR_BALL_2 = 'green'

# paddle
PADDLE_SIZE = 0, 0, 100, 10
PADDLE_COLOR = 'blue'
# score
COLOR_SCORE = 'black'
COLOR_FONT_TEXT_SCORE = ('Courier', 50)
PLACEMENT_SCORE = 250, 30
# game over
PLACEMENT_GAME_OVER_TEXT = 250, 120 # Consider making this (WIDTH / 2, HEIGHT / 3) or similar
GAME_OVER_TEXT = 'Game over :('
COLOR_FONT_TEXT_GAME_OVER = ('Courier', 30)
COLOR_GAME_OVER_TEXT = 'red'

# Lives Settings
INITIAL_LIVES = 3
LIVES_COLOR = 'red'
LIVES_TEXT_X = 70
LIVES_TEXT_Y = 30
LIVES_FONT_STYLE = ('Courier', 20)

# Brick Settings
BRICK_COLUMNS = 10
BRICK_ROWS = 4
# BRICK_WIDTH is calculated in objects.py using WIDTH, BRICK_COLUMNS, BRICK_SPACING_X from settings.py
BRICK_HEIGHT = 15
BRICK_SPACING_X = 5 # Spacing between bricks horizontally
BRICK_SPACING_Y = 5 # Spacing between bricks vertically
BRICKS_START_Y_OFFSET = 70 # Starting Y position for the first row of bricks from the top
BRICK_COLORS = ["red", "orange", "yellow", "green"] # Colors for different rows

# Win Message Settings
YOU_WIN_MESSAGE_TEXT = "YOU WIN!"
YOU_WIN_TEXT_PLACEMENT_X = WIDTH / 2
YOU_WIN_TEXT_PLACEMENT_Y = HEIGHT / 2
YOU_WIN_TEXT_FONT = ('Courier', 40, 'bold')
YOU_WIN_TEXT_COLOR = 'blue'