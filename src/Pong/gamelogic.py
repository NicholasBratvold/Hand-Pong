class GameLogic:
    def __init__(self, ball, scorer, arena):
        self.ball = ball
        self.scorer = scorer
        self.arena = arena

    def update(self):
        # Check if the ball passes the left boundary
        if self.ball.x - self.ball.radius <= self.arena.x:
            # Increment the score for the right player
            self.scorer.score_right += 1
            # Reset the ball's position
            self.reset_ball()

        # Check if the ball passes the right boundary
        if self.ball.x + self.ball.radius >= self.arena.x + self.arena.width:
            # Increment the score for the left player
            self.scorer.score_left += 1
            # Reset the ball's position
            self.reset_ball()

    def reset_ball(self):
        self.ball.x = self.arena.x + self.arena.width // 2
        self.ball.y = self.arena.y + self.arena.height // 2
        # Reset the ball's velocity (you may adjust this based on your game's rules)
        self.ball.vel_x *= -1
        self.ball.vel_y *= -1
