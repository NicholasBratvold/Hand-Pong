import random
import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math


class Animation:
    """
    A class that handles the animation and drawing of game components in Pong.

    Attributes:
    - height (int): The height of the animation screen.
    - width (int): The width of the animation screen.
    - screen (pygame.Surface): The main surface for rendering the animation.
    - arena_surf (pygame.Surface): The surface for drawing the arena.
    - draw_surf (pygame.Surface): The surface for drawing the game components.
    - font (pygame.font.Font): The font used for rendering text.
    - menu_surf (pygame.Surface): The surface for drawing the menu overlay.

    Methods:
    - __init__(self, height, width): Initializes the Animation object.
    - draw(self, components): Draws the game components on the draw_surf.
    - render(self): Renders the draw_surf and arena_surf on the screen.
    - draw_component(self, component): Draws a specific game component.
    - draw_hand_landmarks(self, landmarks, arena): Draws hand landmarks on the draw_surf.
    - draw_face_landmarks(self, landmarks, arena): Draws face landmarks on the draw_surf.
    - draw_fps(self, fps): Draws the frames per second (FPS) on the draw_surf.
    - draw_menu(self, menu_items, selected_item): Draws the menu on the draw_surf.
    - resize(self, w, h, components): Resizes the animation and game components.
    - draw_ball(self, ball): Draws the ball component.
    - draw_paddle(self, paddle): Draws the paddle component.
    - draw_arena(self, arena): Draws the arena component.
    - draw_scorer(self, scorer): Draws the scorer component.
    """

    def __init__(self, height, width):
        """
        Initializes the Animation object.

        Parameters:
        - height (int): The height of the animation screen.
        - width (int): The width of the animation screen.
        """
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.arena_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.display.set_caption("Hand-Pong")

    def draw(self, components):
        """
        Draws the game components on the draw_surf.

        Parameters:
        - components (list): A list of game components to be drawn.
        """

        # Draw the background slightly transparent for smoothing effect
        self.draw_surf.fill((0, 0, 0, 220))
        for component in components:
            self.draw_component(component)

    def render(self):
        """
        Renders the draw_surf and arena_surf on the screen.
        """
        self.screen.blit(self.arena_surf, (0, 0))
        self.screen.blit(self.draw_surf, (0, 0))
        pygame.display.flip()

    def draw_component(self, component):
        """
        Draws a specific game component.

        Parameters:
        - component (object): The game component to be drawn.
        """
        if type(component) is Ball:
            self.draw_ball(component)
        elif type(component) is Paddle:
            self.draw_paddle(component)
        elif type(component) is Arena:
            self.draw_arena(component)
        elif type(component) is Scorer:
            self.draw_scorer(component)
        else:
            print("No draw method for class: ", type(component))

    def draw_hand_landmarks(self, landmarks, arena):
        """
        Draws hand landmarks on the draw_surf.
        The hands are scaled fit nicely on the screen with respect to the arena.

        Parameters:
        - landmarks (list): A list of hand landmarks.
        - arena (object): The arena component.
        """
        scale = 0.2
        if landmarks:
            for hand in landmarks:
                x_0, y_0 = (
                    hand.landmark[0].x * self.width,
                    hand.landmark[0].y * arena.height,
                )
                for landmark in hand.landmark:
                    x, y = int(landmark.x * arena.width * scale), int(
                        landmark.y * arena.height * scale
                    )
                    pygame.draw.circle(
                        self.draw_surf, (100, 0, 0), (x + x_0, y + y_0), 3
                    )

    def draw_face_landmarks(self, landmarks, arena):
        """
        Draws face landmarks on the draw_surf.
        The face landmarks are scaled to fit nicely on the screen with respect to the arena.

        Parameters:
        - landmarks (list): A list of face landmarks.
        - arena (object): The arena component.
        """
        scale = 0.2
        if landmarks:
            for detection in landmarks:
                x_0, y_0 = (
                    detection.location_data.relative_keypoints[0].x * self.width,
                    detection.location_data.relative_keypoints[0].y * arena.height
                    - arena.height // 2,
                )
                for index, landmark in enumerate(
                    detection.location_data.relative_keypoints
                ):
                    x, y = int(landmark.x * self.width * scale), int(
                        landmark.y * self.height * scale
                    )

                    # Eyes
                    if index in [0, 1]:  # indices for left and right eye center
                        pygame.draw.circle(
                            self.draw_surf, (0, 100, 0), (x + x_0, y + y_0), 10, 2
                        )
                        pygame.draw.circle(
                            self.draw_surf,
                            (0, 255, 0),
                            (x + x_0 + 10 * math.sin(math.pi / x_0), y + y_0 + 3),
                            3,
                        )

                    # Nose
                    elif index == 2:
                        pygame.draw.ellipse(
                            self.draw_surf,
                            (0, 100, 0),
                            (x + x_0 - 2.5, y + y_0 - 15, 5, 15),
                        )

                    # Mouth
                    elif index == 3:
                        pygame.draw.arc(
                            self.draw_surf,
                            (0, 100, 0),
                            (x + x_0 - 15, y + y_0, 30, 20),
                            0,
                            math.pi,
                            2,
                        )

                    # Ears
                    else:
                        pygame.draw.ellipse(
                            self.draw_surf,
                            (0, 100, 0),
                            (x + x_0 - 2.5, y + y_0 - 15, 5, 15),
                        )

    def draw_fps(self, fps):
        """
        Draws the frames per second (FPS) on the draw_surf.

        Parameters:
        - fps (float): The frames per second.
        """
        fps_text = f"FPS: {math.floor(fps)}"
        self.font = pygame.font.SysFont(None, 24)

        text_render = self.font.render(fps_text, True, (255, 255, 255))
        text_rect = text_render.get_rect()
        text_rect.topleft = (10, 20)
        self.draw_surf.blit(text_render, text_rect)

    def draw_menu(self, menu_items, selected_item):
        """
        Draws the menu on the draw_surf.

        Parameters:
        - menu_items (list): A list of menu items.
        - selected_item (int): The index of the selected menu item.
        """
        self.menu_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu_surf.fill((0, 0, 0, 100))

        font = pygame.font.SysFont(None, 36)
        for i, item in enumerate(menu_items):
            if i == selected_item:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            text = font.render(item, True, color)
            text_rect = text.get_rect(
                center=(self.width // 2, self.height // 2 + i * 50)
            )
            self.menu_surf.blit(text, text_rect)
            self.draw_surf.blit(self.menu_surf, (0, 0))

    def resize(self, w, h, components):
        """
        Resizes the animation and game components.

        Parameters:
        - w (int): The new width of the animation screen.
        - h (int): The new height of the animation screen.
        - components (list): A list of game components to be resized.
        """
        width_ratio = w / self.width
        height_ratio = h / self.height
        self.width = w
        self.height = h
        for component in components:
            component.resize(width_ratio, height_ratio)
        self.arena_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        # fill screen with black and render to erase previous drawings.
        self.screen.fill((0, 0, 0))
        self.render()

    def draw_ball(self, ball):
        """
        Draws the ball component.

        It has a tail that wiggles as the ball moves and turns red when it hits another ball.

        Parameters:
        - ball (object): The ball component.
        """
        tail_length = len(ball.tail_positions)
        tail_factor = 255 // tail_length
        for i, (x, y) in enumerate(reversed(ball.tail_positions)):
            if i >= tail_length:
                break
            wiggle = 5
            x += math.cos(x * 0.1) * wiggle
            y += math.sin(y * 0.1) * wiggle

            tail_color = (
                max(20 - tail_factor * i, 0),
                255 - tail_factor * i,
                max(100 - tail_factor * i, 0),
            )
            pygame.draw.circle(
                self.draw_surf,
                tail_color,
                (x, y),
                ball.radius * (i + 1) / tail_length,
                1,
            )
        if ball.hit:
            ball_color = (255 - ball.hit_time, 10 * ball.hit_time, 0)
        else:
            ball_color = (20, 255, 90)
        pygame.draw.circle(self.draw_surf, ball_color, (ball.x, ball.y), ball.radius)

    def draw_paddle(self, paddle):
        """
        Draws the paddle component.

        It turns red and bounces when it is hit by a ball.

        Parameters:
        - paddle (object): The paddle component.
        """
        paddle_color = (255, 255, 255)
        offset = 0
        if paddle.hit:
            paddle_color = (255, 0, 0)
            offset = math.sin(paddle.hit_time / 5 * math.pi) * 10
        if paddle.left:
            pygame.draw.rect(
                self.draw_surf,
                paddle_color,
                (paddle.x, paddle.y, paddle.width - offset, paddle.height),
            )
        else:
            pygame.draw.rect(
                self.draw_surf,
                paddle_color,
                (paddle.x + offset, paddle.y, paddle.width - offset, paddle.height),
            )

    def draw_arena(self, arena):
        """
        Draws the arena component.

        It draws the current state of the Conway's Game of Life and the border of the arena.

        Parameters:
        - arena (object): The arena component.
        """
        ALIVE_C = (20, 255, 90)
        DEAD_C = (0, 0, 0)
        draw_surf = self.arena_surf
        cell_size = arena.cell_size

        for row, col in arena.dirty_cells:
            color = ALIVE_C if arena.grid[row][col] else DEAD_C
            x = arena.x + col * cell_size[0]
            y = arena.y + row * cell_size[1]
            pygame.draw.ellipse(draw_surf, color, (x, y, cell_size[0], cell_size[1]))

        arena.dirty_cells.clear()

        pygame.draw.rect(
            draw_surf, ALIVE_C, (arena.x, arena.y, arena.width, arena.height), 2
        )

    def draw_scorer(self, scorer):
        """
        Draws the scorer component.

        Parameters:
        - scorer (object): The scorer component.
        """
        score_text = f"{scorer.score_left} - {scorer.score_right}"
        text_render = scorer.font.render(score_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=(self.width // 2, 20))
        self.draw_surf.blit(text_render, text_rect)
