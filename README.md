# Hand-Pong Game

A simple Pong game implemented with pygame, openCV, and MediaPipe. 

The camera is used to detect hand movements and translate them into paddle movements.
There are two modes available:

1. One Player Mode: In this mode, the goal is to strike the balls on the opposite side using the paddle controlled by hand movements.

2. Two Player Mode: In this mode, two paddles are controlled by two hands, either your own or with another person. The goal is to strike the balls on the opposite side using the paddles.
 
The game difficulty increases by spawning additional balls as the score increases. The balls can collide with each other for some chaotic effects

## Installation
### Step 1: Install Python
If you don't have Python installed, download and install it from the official website:

https://www.python.org/downloads/

This game requires Python 3.6 or later.

### Step 2: Install Pip
Pip is a package manager for Python. It's used to install and manage Python packages. If you installed Python from the official website, you should already have pip. If not, you can install it following the instructions here:

https://pip.pypa.io/en/stable/installation/

### Step 3: Install Required Python Packages
Once you have Python and pip installed, you can install the required packages. Open a terminal or command prompt and run the following commands:

``
    pip install scipy

    pip install opencv-python

    pip install mediapipe

    pip install pygame
``
These commands will download and install the required packages and their dependencies.

### Step 4: Clone and Run the Game
Now you're ready to download the game and run it. Clone the repository, navigate to the game directory, and run the main script.

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



