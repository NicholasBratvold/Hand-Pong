# Hand-Pong Game

This is a simple Pong game implemented with pygame, openCV, MediaPipe, and scipy. 

The game uses a camera to detect hand movements and translate them into paddle movements. It offers two modes:

1. One Player Mode: In this mode, your goal is to hit the balls on the opposite side using the paddle, which is controlled by your hand movements.

2. Two Player Mode: In this mode, two paddles are controlled by two hands. These could be your own hands or those of another person. The goal is to hit the balls on the opposite side using the paddles.
 
The game's difficulty increases by spawning additional balls as the score increases. These balls can collide with each other, creating chaotic effects.

For a fun twist, the ball's movements are used to seed live cells for Conway's Game of Life. You can learn more about this here: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Note: For best results, use bright light and keep your hands close to the camera.

### Controls
ESC: Enter pause menu.

Arrow keys: Select game mode

Enter / Return: Start game

## Installation
### Step 1: Install Python
If you don't have Python installed, download and install it from the official website:

https://www.python.org/downloads/

This game requires Python 3.6 or later.

### Step 2: Install Required Python Packages
Once you have Python and pip installed, you can install the required packages. Open a terminal or command prompt and run the following commands:

```
pip install scipy

pip install opencv-python

pip install mediapipe==0.10.9

pip install pygame
```
You may have to use pip3 instead of pip depending on your Python configuration.

### Step 3: Clone and Run the Game
Clone or download the repository, navigate to the folder, and in your terminal run either:

```
    python3 src/main.py

    python src/main.py
```

## Physics

 ### Motion
The components in the game all have a position and velocity. The position is updated by its velocity at each time step.

 ### Collisions
Balls have their velocities reflected when they hit a paddle or a wall.

When two balls collide, we use the principle of conservation of momentum to calculate their velocities after the collision. The formula used is:

where:

v1f = ((m1 - m2) * v1i + 2 * m2 * v2i) / (m1 + m2)

v2f = ((m2 - m1) * v2i + 2 * m_1 * v1i) / (m1 + m2)

v1f and v2f are the final velocities of the objects.

v1i and v2i are the initial velocities of the objects.

m1 and m2 are the masses of the objects.

This formula assumes that the collisions are perfectly elastic.



## Demo

See the data folder for a demo video. 

## Resources

Pygame:
    https://www.pygame.org/docs/

MediaPipe:
    https://developers.google.com/mediapipe/solutions

Conway' Game of Life:
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Collision:
    https://en.wikipedia.org/wiki/Elastic_collision

AI:
    ChatGPT, Copilot
