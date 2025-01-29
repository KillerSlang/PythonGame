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

last_shape = None

def rotate_shape_left(shape):
    return [(-y, x) for x, y in shape]

def rotate_shape_right(shape):
    return [(y, x) for x, y in shape]

def rotate_shape_down(shape):
    return [(x, y) for x, y in shape]

def rotate_shape_up(shape):
    return [(x, -y) for x, y in shape]

def random_field(grid, direction, dot_position):
    global last_shape

    # Define possible shapes with names
    shapes = {
        "Large Square": [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
        "Long Line": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
        "Large T-shape": [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1)],
        "Large Z-shape": [(0, 0), (1, 1), (0, 1), (2, 2), (1, 2), (0, 2)],
        "Large S-shape": [(2, 0), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
        "Small Line": [(0, 0), (0, 1), (0, 2)],
        "O shape": [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
        "Large Plus": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
        "Small U-shape": [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)],
        "J-shape": [(0, 0), (0, 1), (0, 2), (1, 2)],
        "SnakeLeft": [(2, 0), (2, 1), (1, 1), (1, 2), (0, 2), (0, 3)],
        "SnakeRight": [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
    }

    # Select a random shape that is different from the last one
    new_shape_name, new_shape_coords = random.choice(list(shapes.items()))
    while new_shape_coords == last_shape:
        new_shape_name, new_shape_coords = random.choice(list(shapes.items()))

    last_shape = new_shape_coords

    # You can now use new_shape_name and new_shape_coords as needed

    # Print the shape to the console
    print("Shape to be placed:" + new_shape_name)
    for dx, dy in new_shape_coords:
        print(f"({dx}, {dy})")

    # Rotate shape based on direction
    if direction == "left":
        shape = rotate_shape_left(new_shape_coords)
    elif direction == "right":
        shape = rotate_shape_right(new_shape_coords)
    elif direction == "down":
        shape = rotate_shape_down(new_shape_coords)
    elif direction == "up":
        shape = rotate_shape_up(new_shape_coords)  # This rotation flips the shape upside-down
    else:
        shape = new_shape_coords  # No rotation if direction is not specified

    # Print the rotated shape to the console
    print("Rotated shape:")
    for dx, dy in shape:
        print(f"({dx}, {dy})")

    # Adjust shape position to ensure it connects to the desired position
    attach_x, attach_y = dot_position  # Use the desired position as the reference

    # Check if the shape can be placed without overlapping existing boxes
    can_place = True
    for dx, dy in shape:
        if direction == "up":
            x = attach_x + dx
            y = attach_y + dy  # Keep dy consistent with the shape's natural orientation
        else:
            x = attach_x + dx
            y = attach_y + dy

        if not (0 <= x < cols and 0 <= y < rows) or grid[y][x] == 1:
            can_place = False
            print(f"Error: Shape cannot be placed at ({attach_x}, {attach_y}) due to collision or out-of-bounds.")
            break

    if can_place:
        # Place the shape onto the grid
        for dx, dy in shape:
            if direction == "up":
                if new_shape_name == "O shape" or new_shape_name == "Large Square" or new_shape_name == "Small U-shape" or new_shape_name == "Large Plus":
                    x = attach_x + dx - 1
                    y = attach_y - abs(dy)
                elif new_shape_name == "Large S-shape" or new_shape_name == "SnakeLeft":
                    x = attach_x + dx -2
                    y = attach_y - abs(dy)
                else:
                    x = attach_x + dx
                    y = attach_y - abs(dy)
            elif direction == "left" or direction == "right":
                if new_shape_name == "O shape" or new_shape_name == "Large Square" or new_shape_name == "Small U-shape" or new_shape_name == "Large Plus":
                    x = attach_x + dx
                    y = attach_y - abs(dy) + 1
                elif new_shape_name == "Large S-shape" or new_shape_name == "SnakeLeft":
                    x = attach_x + dx
                    y = attach_y - abs(dy) + 2
                else:
                    x = attach_x + dx
                    y = attach_y - abs(dy)
            elif direction == "down":
                if new_shape_name == "O shape" or new_shape_name == "Large Square" or new_shape_name == "Large Plus":
                    x = attach_x + dx - 1
                    y = attach_y - abs(dy) + 2
                elif new_shape_name ==  "Long Line":
                    x = attach_x + dx
                    y = attach_y - abs(dy) + 4

                elif new_shape_name == "SnakeLeft" or new_shape_name == "SnakeRight":
                    x = attach_x + dx
                    y = attach_y - abs(dy) + 3
                elif new_shape_name == "Small Line" or new_shape_name == "Large S-shape" or new_shape_name == "Large Z-shape" or new_shape_name == "J-shape":
                    x = attach_x + dx 
                    y = attach_y - abs(dy) + 2
                else:
                    x = attach_x + dx 
                    y = attach_y - abs(dy)

            if 0 <= x < cols and 0 <= y < rows:
                grid[y][x] = 1
    else:
        print("Shape placement failed due to collision or being out of bounds.")

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
                grid = random_field(grid, direction, new_position)  # Pass the new position

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
