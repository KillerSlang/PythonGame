import pygame
import sys
import random
import time
import subprocess

# Initialize Pygame
pygame.init()

# Read character name from command-line arguments
if len(sys.argv) > 1:
    character_name = sys.argv[1]
else:
    character_name = "Unknown"

# Set up the display
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption(f"World Map, Character selected: - {character_name}")

# Grid setup
box_size = 25
cols = 1200 // box_size
rows = 700 // box_size

def starting_grid():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    start_x = (cols // 2) - 1
    start_y = rows - 3
    for y in range(start_y, start_y + 3):
        for x in range(start_x, start_x + 3):
            grid[y][x] = 1
    return grid

def random_field(grid, direction, dot_position):
    # Define possible larger shapes
    shapes = [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],  # Large Square
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Long Line
        [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)],  # Large T-shape
        [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],  # Large Z-shape
        [(0, 2), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]   # Large S-shape
    ]

    # Select a random shape
    shape = random.choice(shapes)

    # Determine attachment position based on direction
    dot_x, dot_y = dot_position
    if direction == "up":
        attach_x, attach_y = dot_x, dot_y - 1  # Attach above the dot
    elif direction == "down":
        attach_x, attach_y = dot_x, dot_y + 1  # Attach below the dot
    elif direction == "left":
        attach_x, attach_y = dot_x - 1, dot_y  # Attach to the left of the dot
    elif direction == "right":
        attach_x, attach_y = dot_x + 1, dot_y  # Attach to the right of the dot

    # Adjust shape position to ensure it connects to the existing field
    for dx, dy in shape:
        x = attach_x + dx
        y = attach_y + dy
        if 0 <= x < cols and 0 <= y < rows:
            grid[y][x] = 1

    return grid

# Define the color for the grid cells
grid_color = (255, 255, 255)  # White

def draw_grid(grid):
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, grid_color, (x * box_size, y * box_size, box_size, box_size), 1)

# Define the initial position of the red dot
dot_position = [cols // 2, rows - 2]

# Define the color for the red dot
dot_color = (255, 0, 0)  # Red

def draw_dot(position):
    pygame.draw.circle(screen, dot_color, (position[0] * box_size + box_size // 2, position[1] * box_size + box_size // 2), box_size // 4)

def can_move_to(position, grid):
    x, y = position
    if 0 <= x < cols and 0 <= y < rows:
        return grid[y][x] == 1
    return False

# Main game loop
running = True
grid = starting_grid()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            new_position = dot_position[:]
            direction = None
            if event.key == pygame.K_a:  # Move left
                new_position[0] -= 1
                direction = "left"
            elif event.key == pygame.K_d:  # Move right
                new_position[0] += 1
                direction = "right"
            elif event.key == pygame.K_w:  # Move up
                new_position[1] -= 1
                direction = "up"
            elif event.key == pygame.K_s:  # Move down
                new_position[1] += 1
                direction = "down"

            # Check if the new position is valid
            if can_move_to(new_position, grid):
                dot_position = new_position
            elif direction:
                # Generate a random field in the direction of the attempted move
                grid = random_field(grid, direction, dot_position)

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw the grid
    draw_grid(grid)

    # Draw the red dot
    draw_dot(dot_position)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
