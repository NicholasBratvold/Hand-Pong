# Hand-Pong Game

A simple Pong game implemented with pygame, openCV, and MediaPipe. 

The camera is used to detect hand movements and translate them into paddle movements. There are two modes available:

1. One Player Mode: In this mode, the goal is to strike the balls on the opposite side using the paddle controlled by hand movements.

2. Two Player Mode: In this mode, two paddles are controlled by two hands, either your own or with another person. The goal is to strike the balls on the opposite side using the paddles.
 
The game difficulty increases by spawning additional balls as the score increases. The balls can collide with each other for some chaotic effects.

As a fun effect the balls movements are used to seed live cells for Conway's Game of Life. https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life


## Installation
### Step 1: Install Python
If you don't have Python installed, download and install it from the official website:

https://www.python.org/downloads/

This game requires Python 3.6 or later.

### Step 2: Install Required Python Packages
Once you have Python and pip installed, you can install the required packages. Open a terminal or command prompt and run the following commands:


```
    pip3 install scipy

    pip3 install opencv-python

    pip3 install mediapipe=0.10.9

    pip3 install pygame
```

These commands will download and install the required packages and their dependencies.

### Step 3: Clone and Run the Game
Clone or download the repository and navigate to the folder and in your terminal. Run either:

```
    python3 src/main.py
    or
    python src/main.py
```

## Physics

 ### Motion
The components in the game all have a position and velocity. The position is updated by its velocity at each time step.

 ### Collisions
When two objects collide, we use the principle of conservation of momentum to calculate their velocities after the collision. The formula used is:

where:

v1f = ((m1 - m2) * v1i + 2 * m2 * v2i) / (m1 + m2)

v2f = ((m2 - m1) * v2i + 2 * m_1 * v1i) / (m1 + m2)

v1f and v2f are the final velocities of the objects.

v1i and v2i are the initial velocities of the objects.

m1 and m2 are the masses of the objects.

This formula assumes that the collisions are perfectly elastic, meaning that the total kinetic energy is conserved.



