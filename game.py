from tkinter import *
import time

from settings import * # This will import all settings, including newly added ones
from objects import Ball, Paddle, Score, Lives, Brick, BRICK_WIDTH # BRICK_WIDTH is calculated in objects.py

# Note: PLACEMENT_GAME_OVER_TEXT, GAME_OVER_TEXT, COLOR_FONT_TEXT_GAME_OVER, COLOR_GAME_OVER_TEXT
# are already expected to be in settings.py from previous structure.
# YOU_WIN_TEXT_PLACEMENT_X, YOU_WIN_TEXT_PLACEMENT_Y, YOU_WIN_MESSAGE_TEXT, 
# YOU_WIN_TEXT_FONT, YOU_WIN_TEXT_COLOR are now directly in settings.py.
# BRICK_ROWS, BRICK_COLUMNS, BRICK_HEIGHT, BRICK_SPACING_X, BRICK_SPACING_Y, 
# BRICKS_START_Y_OFFSET, BRICK_COLORS are also directly in settings.py.

class Game:
    def __init__(self, tk, canvas):
        self.tk = tk
        self.canvas = canvas

        self.paddle = Paddle(self.canvas, PADDLE_COLOR)
        self.score = Score(self.canvas, COLOR_SCORE)
        self.lives = Lives(self.canvas)
        
        self.bricks = []
        self._create_bricks() # Initialize bricks

        # Pass the list of bricks to the Ball object
        self.ball = Ball(self.canvas, self.paddle, self.score, self.lives, self.bricks, COLOR_BALL)
 
        self.canvas.bind_all("<KeyPress-Right>", self.paddle.turn_right) 
        self.canvas.bind_all("<KeyPress-Left>", self.paddle.turn_left)  
        self.canvas.bind_all("<KeyPress-Return>", self.start_game_event)
    
        self.game_actually_started = False
        self.game_over_flag = False
        self.win_message_id = None # To store ID of win/game over message

    def _create_bricks(self):
        # BRICK_WIDTH is imported from objects.py (where it's calculated using settings)
        # Other brick constants (BRICK_ROWS, etc.) are directly from settings.py
        for row in range(BRICK_ROWS): 
            for col in range(BRICK_COLUMNS):
                x1 = col * (BRICK_WIDTH + BRICK_SPACING_X) + BRICK_SPACING_X
                y1 = row * (BRICK_HEIGHT + BRICK_SPACING_Y) + BRICKS_START_Y_OFFSET
                color_index = row % len(BRICK_COLORS)
                brick = Brick(self.canvas, x1, y1, BRICK_WIDTH, BRICK_HEIGHT, BRICK_COLORS[color_index])
                self.bricks.append(brick)

    def start_game_event(self, event):
        if not self.game_actually_started and not self.game_over_flag : # Allow restart with Enter if game was over
             if self.game_over_flag : # Reset game state if restarting after game over
                # Clear old win/game over message
                if self.win_message_id:
                    self.canvas.delete(self.win_message_id)
                    self.win_message_id = None
                
                # Reset score, lives, ball, paddle, bricks
                self.score = Score(self.canvas, COLOR_SCORE) # Re-create to reset score display
                self.lives = Lives(self.canvas) # Re-create to reset lives display
                
                # Clear old bricks and create new ones
                for brick in self.bricks:
                    if brick.id: # Check if canvas item exists
                         try:
                            self.canvas.delete(brick.id)
                         except TclError: # Catch error if item already deleted
                            pass
                self.bricks = []
                self._create_bricks()

                self.paddle.reset()
                # Re-initialize ball with new score, lives, bricks
                self.ball = Ball(self.canvas, self.paddle, self.score, self.lives, self.bricks, COLOR_BALL)
                self.ball.reset() # Ensure ball is in starting state
                
                self.game_over_flag = False

             self.game_actually_started = True


    def run_game(self):
        while True: # Main loop runs continuously; game_over_flag controls active play
            if self.game_actually_started and not self.game_over_flag:
                self.ball.draw() 
                self.paddle.draw()

                # Check for win condition
                all_bricks_destroyed = True # Assume all are destroyed
                if not self.bricks: # Should not happen if _create_bricks was called
                    all_bricks_destroyed = False
                else:
                    for brick in self.bricks:
                        if brick.is_active():
                            all_bricks_destroyed = False
                            break
                
                if all_bricks_destroyed and self.bricks:
                    self.game_over_flag = True
                    self.game_actually_started = False
                    # Use new constants from settings.py for "You Win" message
                    self.win_message_id = self.canvas.create_text(
                        YOU_WIN_TEXT_PLACEMENT_X, 
                        YOU_WIN_TEXT_PLACEMENT_Y, 
                        text=YOU_WIN_MESSAGE_TEXT, 
                        font=YOU_WIN_TEXT_FONT, 
                        fill=YOU_WIN_TEXT_COLOR
                    )

                if self.ball.lost_life:
                    self.lives.decrement()
                    self.ball.lost_life = False

                    if self.lives.is_game_over():
                        self.game_over_flag = True
                        self.game_actually_started = False # Stop game actions
                        if self.win_message_id: # Clear any win message if lost on same turn
                            self.canvas.delete(self.win_message_id)
                        self.win_message_id = self.canvas.create_text(PLACEMENT_GAME_OVER_TEXT, text=GAME_OVER_TEXT, font=COLOR_FONT_TEXT_GAME_OVER, fill=COLOR_GAME_OVER_TEXT)
                    elif not self.game_over_flag: # Only reset if not already game over (e.g. by winning)
                        self.paddle.reset() 
                        self.ball.reset()
                        self.tk.update_idletasks()
                        self.tk.update()
                        time.sleep(1)
            
            # Always update tk
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

            # If game is over (win or lose), and we want to exit after a delay
            # This part might need adjustment based on how main.py handles the Game loop
            # For now, this loop will just keep the window open.
            # If main.py calls run_game and expects it to terminate, this needs change.
            # Assuming run_game is the main loop controlled by Tkinter's mainloop in main.py eventually.
            # The break condition for this outer 'while True' is not explicitly defined here,
            # implying the window close button would be the way to exit.
            # If we want to auto-close or offer restart:
            if self.game_over_flag and not self.game_actually_started:
                # Wait for a key press (e.g. Enter) to restart or just sit in this state
                # The start_game_event handles restart on Enter press
                pass # Just keep updating, waiting for Enter or window close