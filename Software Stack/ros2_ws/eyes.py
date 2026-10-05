import pygame
import sys
import math
from time import sleep

pygame.init()

# Set up the display with 800x480 resolution for the 7-inch screen
screen = pygame.display.set_mode((800, 480))  # 800x480 resolution for the 7-inch display
pygame.display.set_caption("Animated Eyes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)

# Eye parameters
EYE_RADIUS = 50
PUPIL_RADIUS = 20
EYE_X1, EYE_Y1 = 200, 240  # Left eye (adjust as needed)
EYE_X2, EYE_Y2 = 600, 240  # Right eye (adjust as needed)

# Create the clock object for controlling the frame rate
clock = pygame.time.Clock()

# Function to draw the eyes
def draw_eyes(pupil_x1, pupil_y1, pupil_x2, pupil_y2):
    screen.fill(BLACK)
    # Draw eyes
    pygame.draw.circle(screen, EYE_COLOR, (EYE_X1, EYE_Y1), EYE_RADIUS)
    pygame.draw.circle(screen, EYE_COLOR, (EYE_X2, EYE_Y2), EYE_RADIUS)

    # Draw pupils
    pygame.draw.circle(screen, PUPIL_COLOR, (pupil_x1, pupil_y1), PUPIL_RADIUS)
    pygame.draw.circle(screen, PUPIL_COLOR, (pupil_x2, pupil_y2), PUPIL_RADIUS)

    pygame.display.flip()

# Main loop for animation
running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate pupil positions based on angle
    try:
        pupil_x1 = int(EYE_X1 + EYE_RADIUS * 0.5 * pygame.math.cos(angle))
        pupil_y1 = int(EYE_Y1 + EYE_RADIUS * 0.5 * pygame.math.sin(angle))
        pupil_x2 = int(EYE_X2 + EYE_RADIUS * 0.5 * pygame.math.cos(angle + 3.14))  # Offset for right eye
        pupil_y2 = int(EYE_Y2 + EYE_RADIUS * 0.5 * pygame.math.sin(angle + 3.14))
    except AttributeError:
        # pygame.math has no cos/sin, so fall back to Python's math module
        pupil_x1 = int(EYE_X1 + EYE_RADIUS * 0.5 * math.cos(angle))
        pupil_y1 = int(EYE_Y1 + EYE_RADIUS * 0.5 * math.sin(angle))
        pupil_x2 = int(EYE_X2 + EYE_RADIUS * 0.5 * math.cos(angle + 3.14))  # Offset for right eye
        pupil_y2 = int(EYE_Y2 + EYE_RADIUS * 0.5 * math.sin(angle + 3.14))

    # Draw the eyes with moving pupils
    draw_eyes(pupil_x1, pupil_y1, pupil_x2, pupil_y2)

    angle += 0.1
    if angle > 2 * 3.14:
        angle = 0

    clock.tick(30)  # Control the speed of the animation (30 frames per second)

pygame.quit()
sys.exit()
