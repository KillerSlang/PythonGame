import pygame
import sys
import random
import subprocess
import time

# Concepts: 
# Herlaad de game als een bepaalde cel is bereikt, met de pop-up to clear the map.

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

enemycounter = 0
battle_result = None

# Function to run the battle and get the result
def run_battle(character_name, enemycounter):
    global battle_result
    # Construct the command with arguments
    command = ["python", "EnemyEncounter.py", character_name, str(enemycounter)]
    
    # Start the subprocess with Popen
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Read output and error as they are generated
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(f"File 1: Received -> {output.strip()}")
            if output.strip() == "Win":
                print(f"File 1: Received Final message -> Game won!")
                battle_result = "Win"
            if output.strip() == "RunAway":
                print(f"File 1: Received Final message -> Run away!")
                battle_result = "RunAway"
            if output.strip() == "Lose":
                print(f"File 1: Received Final message -> Game lost!")
                fight_lost()
            
    # Capture any errors
    stderr_output = process.stderr.read().strip()
    if stderr_output:
        print(f"File 1: Error -> {stderr_output}")

# Function to generate the starting grid
def starting_grid():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    start_x = (cols // 2) - 1
    start_y = rows - 3
    for y in range(start_y, start_y + 3):
        for x in range(start_x, start_x + 3):
            grid[y][x] = 1
    return grid

last_shape = None

# Functions to rotate a shape depending on the direction
def rotate_shape_left(shape):
    return [(-y, x) for x, y in shape]

def rotate_shape_right(shape):
    return [(y, x) for x, y in shape]

def rotate_shape_down(shape):
    return [(x, y) for x, y in shape]

def rotate_shape_up(shape):
    return [(x, -y) for x, y in shape]

# Function to generate a random field for the player to walk on
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

    # Define blockade shapes to replace the original shapes if they can't be placed
    blockade_shapes = {
        "Block Long Line": [(0, 0), (0, 1), (0, 2)],
        "Block Line": [(0, 0), (0, 1)],
        "Block Dot": [(0, 0)]
    }

    # Select a random shape that is different from the last one
    new_shape_name, new_shape_coords = random.choice(list(shapes.items()))
    while new_shape_coords == last_shape:
        new_shape_name, new_shape_coords = random.choice(list(shapes.items()))

    last_shape = new_shape_coords

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

    attach_x, attach_y = dot_position  # Use the desired position as the reference

    # Check if the shape can be placed without overlapping existing boxes
    can_place = True
    colliding_positions = []
    non_colliding_positions = []

    # Correction so shape is placed correctly with the dot as center indication
    for dx, dy in shape:
        if direction == "up":
            if new_shape_name in ["O shape", "Large Square", "Small U-shape", "Large Plus"]:
                x = attach_x + dx - 1
                y = attach_y - abs(dy)
            elif new_shape_name in ["Large S-shape", "SnakeLeft"]:
                x = attach_x + dx - 2
                y = attach_y - abs(dy)
            else:
                x = attach_x + dx
                y = attach_y - abs(dy)
        elif direction in ["left", "right"]:
            if new_shape_name in ["O shape", "Large Square", "Small U-shape", "Large Plus"]:
                x = attach_x + dx
                y = attach_y - abs(dy) + 1
            elif new_shape_name in ["Large S-shape", "SnakeLeft"]:
                x = attach_x + dx
                y = attach_y - abs(dy) + 2
            else:
                x = attach_x + dx
                y = attach_y - abs(dy)
        elif direction == "down":
            if new_shape_name in ["O shape", "Large Square", "Large Plus"]:
                x = attach_x + dx - 1
                y = attach_y - abs(dy) + 2
            elif new_shape_name == "Long Line":
                x = attach_x + dx
                y = attach_y - abs(dy) + 4
            elif new_shape_name in ["SnakeLeft", "SnakeRight"]:
                x = attach_x + dx - 2
                y = attach_y - abs(dy) + 3
            elif new_shape_name in ["Small Line", "Large S-shape", "Large Z-shape", "J-shape"]:
                x = attach_x + dx
                y = attach_y - abs(dy) + 2
            elif new_shape_name == "Small U-shape":
                x = attach_x + dx
                y = attach_y - abs(dy) + 1
            else:
                x = attach_x + dx
                y = attach_y - abs(dy)
        else:
            x = attach_x + dx
            y = attach_y + dy  # Default behavior for other cases (failsafe)
        
        if not (0 <= x < cols and 0 <= y < rows) or grid[y][x] == 1 or grid[y][x] == "Enemy" or grid[y][x] == "Cleared" or grid[y][x] == "Runaway":
            can_place = False
            colliding_positions.append((x, y))  # Store colliding positions
        else:
            non_colliding_positions.append((x, y))  # Store valid positions

    if not can_place:
        print(f"Error: {new_shape_name} cannot be placed at ({attach_x}, {attach_y}) due to collision or out-of-bounds.")
        print("Colliding positions:", colliding_positions)
        print("Valid positions:", non_colliding_positions)
        
        # If the shape can't be placed, replace it with a blockade shape
        if new_shape_name in ["Large Square", "Small U-shape", "O shape"]:
            print(f"Shape {new_shape_name} is replaced with Block Long Line.")
            new_shape_name = "Block Long Line"  # Replace shape with Block Long Line
            shape = blockade_shapes[new_shape_name]  # Get Block Long Line shape
        elif new_shape_name in ["Long Line"]:
            print(f"Shape {new_shape_name} is replaced with Block Line.")
            new_shape_name = "Block Line"  # Replace shape with Block Line
            shape = blockade_shapes[new_shape_name]  # Get Block Line shape
        elif new_shape_name in ["Small Line", "Large T-shape", "Large S-shape", "Large Z-shape", "J-shape", "SnakeLeft", "SnakeRight", "Large Plus"]:
            print(f"Shape {new_shape_name} is replaced with Block Dot.")
            new_shape_name = "Block Dot"
            shape = blockade_shapes[new_shape_name]
        
        # Now process the positions using the updated blockade shape
        for dx, dy in shape:
            x = attach_x + dx
            y = attach_y + dy
            if 0 <= x < cols and 0 <= y < rows and grid[y][x] != 1 and grid[y][x] != "Enemy" and grid[y][x] != "Cleared" and grid[y][x] != "Runaway":
                grid[y][x] = 2
            elif 0 <= x < cols and 0 <= y < rows and grid[y][x] != "Enemy" and grid[y][x] != "Cleared" and grid[y][x] != "Runaway":
                grid[y][x] = 1


    if can_place:
        # Place the shape onto the grid
        for dx, dy in shape:
            # Correction so shape is placed correctly with the dot as center indication
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
                elif new_shape_name == "SnakeRight":
                    x = attach_x + dx -2
                    y = attach_y - abs(dy) + 3
                elif new_shape_name == "SnakeLeft":
                    x = attach_x + dx
                    y = attach_y - abs(dy) + 3
                elif new_shape_name == "Small Line" or new_shape_name == "Large S-shape" or new_shape_name == "Large Z-shape" or new_shape_name == "J-shape":
                    x = attach_x + dx 
                    y = attach_y - abs(dy) + 2
                elif new_shape_name == "Small U-shape":
                    x = attach_x + dx
                    y = attach_y - abs(dy) + 1
                else:
                    x = attach_x + dx 
                    y = attach_y - abs(dy)

            # Generate a chance of an enemy appearing in a cell in the newly generated shape
            if 0 <= x < cols and 0 <= y < rows and grid[y][x] != 2:
                enemyBox = random.randint(0, 20)  # 1 in 20 chance of being an enemy
                if enemyBox == 20:
                    grid[y][x] = "Enemy"
                else:
                    grid[y][x] = 1
    else:
        print("Shape placement failed due to collision or being out of bounds.")

    return grid

# Function to change value of cell to "Cleared" after winning a battle
def fight_won():
    global grid, dot_position, battle_result
    x, y = dot_position
    if 0 <= x < cols and 0 <= y < rows:
        grid[y][x] = "Cleared"
    battle_result = None  # Reset battle_result

# Function to change value of cell to "Runaway" after running away from a battle
def Runaway():
    global grid, dot_position, battle_result
    x, y = dot_position
    if 0 <= x < cols and 0 <= y < rows:
        grid[y][x] = "Runaway"
    battle_result = None  # Reset battle_result

# Function to close the game if the player loses a battle
def fight_lost():
    print("Closing window...")
    pygame.quit()
    sys.exit()

# Define the color for the walkable grid cells
grid_color = (255, 255, 255)  # White

# Function to draw the grid and give the corrisponding color to the cells
def draw_grid(grid):
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1 or grid[y][x] == "Enemy":
                pygame.draw.rect(screen, grid_color, (x * box_size, y * box_size, box_size, box_size), 1)
            elif grid[y][x] == 2:
                pygame.draw.rect(screen, (255, 0, 0), (x * box_size, y * box_size, box_size, box_size))  # Red for non-colliding positions
            elif grid[y][x] == "Cleared":
                pygame.draw.rect(screen, (0, 255, 0), (x * box_size, y * box_size, box_size, box_size))
            elif grid[y][x] == "Runaway":
                pygame.draw.rect(screen, (0, 0, 255), (x * box_size, y * box_size, box_size, box_size))

# Define the initial position of the red dot
dot_position = [cols // 2, rows - 2]

# Define the color for the red dot
dot_color = (255, 0, 0)  # Red

# Function to draw the red dot/player
def draw_dot(position):
    pygame.draw.circle(screen, dot_color, (position[0] * box_size + box_size // 2, position[1] * box_size + box_size // 2), box_size // 4)

# Function to check what cell the player is trying to move to and if it's a valid move
def can_move_to(position, grid):
    x, y = position
    if 0 <= x < cols and 0 <= y < rows:
        if grid[y][x] == "Enemy":
            print("Enemy Detected!")
            global enemycounter
            enemycounter += 1
            run_battle(character_name, enemycounter)
            return grid[y][x] == "Enemy"
        elif grid[y][x] == "Runaway":
            print("Old Enemy Detected!")
            run_battle(character_name, enemycounter)
            return grid[y][x] == "Runaway"
        elif grid[y][x] == "Cleared":
            return True
        else:
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
                if battle_result == "Win":
                    fight_won()
                elif battle_result == "RunAway":
                    Runaway()
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
