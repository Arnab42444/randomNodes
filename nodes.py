import pygame
import random
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BALL_SIZE = 5
NUM_BALLS = 30
LINE_NUM = 3


class Ball:
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)

    # Speed and direction of rectangle
    ball.change_x = random.randrange(-2, 2)
    ball.change_y = random.randrange(-2, 2)

    return ball


def closest_node(node, nodes, num=1):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argsort(dist_2)[:num]


def main():
    """
    This is our main program.
    """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing Balls")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    ball_list = []
    ball_points = []

    for i in range(NUM_BALLS):
        ball_list.append(make_ball())

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_q:
                    done = True
                if event.key == pygame.K_SPACE:
                    ball_list.append(make_ball())
                if event.key == pygame.K_c:
                    if len(ball_list) > 1:
                        ball_list.pop()

        # --- Logic
        ball_points = []
        for ball in ball_list:
            if abs(ball.change_x) > 9:
                ball.change_x = random.choice([-1, 1])
            if abs(ball.change_y) > 9:
                ball.change_y = random.choice([-1, 1])
            ball_points.append([int(ball.x), int(ball.y)])
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y

            # Bounce the ball if needed
            if ball.y >= SCREEN_HEIGHT - BALL_SIZE or ball.y <= BALL_SIZE:
                ball.change_y *= -1
            if ball.x >= SCREEN_WIDTH - BALL_SIZE or ball.x <= BALL_SIZE:
                ball.change_x *= -1
            if ball.y > SCREEN_HEIGHT + BALL_SIZE or ball.y < -BALL_SIZE or ball.x > SCREEN_WIDTH + BALL_SIZE or ball.x < -BALL_SIZE:
                ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
                ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)

        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)

        # Draw the balls
        for ball in ball_list:
            pnts = closest_node(
                (int(ball.x), int(ball.y)), ball_points, LINE_NUM+1)
            pygame.draw.circle(
                screen, WHITE, [int(ball.x), int(ball.y)], BALL_SIZE)

            for line in range(0, len(pnts)):
                pygame.draw.line(screen, ball.color, ball_points[pnts[line]], [
                    int(ball.x), int(ball.y)], 1)



        for _ in range(2):
            random.choice(ball_list).change_x += random.random() * \
                random.choice([-1, 1])
            random.choice(ball_list).change_y += random.random() * \
                random.choice([-1, 1])
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()

    # Close everything down
    pygame.quit()


if __name__ == "__main__":
    main()