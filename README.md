# Breakout Lite - Enhanced

Breakout Lite is an enhanced version of the classic arcade game, now featuring a lives system, destructible bricks, and a win condition! Control the paddle to keep the ball in play, destroy all the bricks to clear the level, and manage your lives to achieve the highest score.

## How to Play

The game is launched by running the `main.py` file:
```bash
python main.py
```

## Features

*   **Classic Gameplay:** Control a paddle at the bottom of the screen to bounce a ball upwards.
*   **Destructible Bricks:** A wall of colorful bricks is arranged at the top.
    *   Hit bricks with the ball to destroy them and score points.
    *   Clearing all bricks results in a "YOU WIN!" message, and the game will await your next action.
*   **Lives System:**
    *   You start with a set number of lives (currently 3, as configured in `settings.py`).
    *   If the ball hits the bottom of the screen, you lose a life, and the ball and paddle reset.
    *   The game ends ("Game Over") when all lives are lost.
*   **Scoring:**
    *   Points are awarded for hitting the paddle and for destroying bricks.
    *   The ball's speed may increase as your score gets higher!
*   **Dynamic Configuration:** Many game parameters (like initial lives, brick layout, colors, speeds) are configurable in the `settings.py` file.

## Controls

*   **Move Paddle Left:** Left Arrow Key (`<KeyPress-Left>`)
*   **Move Paddle Right:** Right Arrow Key (`<KeyPress-Right>`)
*   **Start Game / Restart Game:** Enter Key (`<KeyPress-Return>`)
    *   Press Enter to start the game initially.
    *   After a "Game Over" or "YOU WIN!" message, press Enter to restart the game from the beginning.

## Game Files

*   `main.py`: The main script to run the game.
*   `game.py`: Contains the main `Game` class orchestrating the gameplay.
*   `objects.py`: Defines game objects like `Ball`, `Paddle`, `Brick`, `Score`, and `Lives`.
*   `settings.py`: Contains configurable parameters for the game.
