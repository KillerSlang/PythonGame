import pygame
import sys
import random
import subprocess
import time
import json

# Concept ideas:
# Enemies: Normal, Elite, Boss?
# Cheatcode/secret input?

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

enemycounter = 0 # used to adjust enemy difficulty
battle_result = None # used to decide the color of the cell after battle
cellGameWon = False # used to reload the map or finish the game after the correct cell has been found
gameWinCell = None
randomWinCell = 900 # Change to 900 when finished testing

items = {
    "Health Potion",
    "Damage Boost",
    "Weaken Potion",
    "Speed Potion",
    "Accuracy Potion"
}

inventory = [] # Initialize inventory as an empty list

# Add a global flag to track if a battle is in progress
battle_in_progress = False

# Function to run the battle and get the result
def run_battle(character_name, enemycounter):
    global battle_result, inventory, battle_in_progress
    battle_in_progress = True  # Set the flag to True when the battle starts
    # Serialize the inventory to a JSON string
    inventory_json = json.dumps(inventory)
    
    # Construct the command with arguments
    command = ["python", "EnemyEncounter.py", character_name, str(enemycounter), inventory_json]
    
    # Start the subprocess with Popen
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Read output and error as they are generated
    updated_inventory = None
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(f"File 1: Received -> {output.strip()}")
            if output.strip() == "Win":
                print(f"File 1: Received Final message -> Game won!")
                battle_result = "Win"
            elif output.strip() == "RunAway":
                print(f"File 1: Received Final message -> Run away!")
                battle_result = "RunAway"
            elif output.strip() == "Lose":
                print(f"File 1: Received Final message -> Game lost!")
                fight_lost()
            else:
                # Attempt to parse the updated inventory
                try:
                    updated_inventory = json.loads(output.strip())
                except json.JSONDecodeError:
                    pass
            
    # Capture any errors
    stderr_output = process.stderr.read().strip()
    if stderr_output:
        print(f"File 1: Error -> {stderr_output}")
    
    # Update the inventory if it was returned
    if updated_inventory is not None:
        inventory = updated_inventory
        print(f"Updated inventory: {inventory}")
    
    # Print the inventory after the battle
    print("Inventory after battle:", inventory)
    battle_in_progress = False  # Reset the flag when the battle ends

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
    global last_shape, cellGameWon, gameWinCell

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
            if 0 <= x < cols and 0 <= y < rows and grid[y][x] != 1 and grid[y][x] != "Enemy" and grid[y][x] != "Cleared" and grid[y][x] != "Runaway" and grid[y][x] != "Item":
                grid[y][x] = 2
            elif 0 <= x < cols and 0 <= y < rows and grid[y][x] != "Enemy" and grid[y][x] != "Cleared" and grid[y][x] != "Runaway" and grid[y][x] != "Item":
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
            
            if 0 <= x < cols and 0 <= y < rows and grid[y][x] != 2 and grid[y][x] != "Enemy":
                itembox = random.randint(0, 15)  # 1 in 15 chance of being an item
                if itembox == 15:
                    grid[y][x] = "Item"
                else:
                    grid[y][x] = 1

            # Ensure one cell is randomly selected and made yellow in each generation
            if not cellGameWon:
                global randomWinCell
                gameWinCell = random.randint(0, randomWinCell)
                print(gameWinCell)
                if gameWinCell == randomWinCell:
                    cellGameWon = True
                    grid[y][x] = "Win"
                else:
                    gameWinCell -= 1
                    randomWinCell -= 1  # Decrement randomWinCell after each roll
                    print("GameWinCell: ", randomWinCell)

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

# Function to obtain an item from a selection screen after which the item is randomly selected with more odds to the selected item and then added to the inventory
def obtain_item_selection():
    global inventory
    # Convert items to a list for consistent ordering
    items_list = list(items)

    # Set up the pop-up window dimensions
    popup_width, popup_height = 400, 400
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((50, 50, 50))  # Dark gray background

    # Define fonts and colors
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)  # White
    button_color = (100, 100, 255)  # Light blue
    button_hover_color = (150, 150, 255)  # Lighter blue
    button_width, button_height = 200, 50

    # Calculate button positions
    button_positions = []
    for i, item in enumerate(items_list):
        x = (popup_width - button_width) // 2
        y = 50 + i * (button_height + 20)
        button_positions.append((x, y, button_width, button_height))

    # Display the pop-up and handle selection
    selected_item = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, (x, y, w, h) in enumerate(button_positions):
                    if x <= mouse_x - (screen.get_width() - popup_width) // 2 <= x + w and \
                       y <= mouse_y - (screen.get_height() - popup_height) // 2 <= y + h:
                        selected_item = items_list[i]
                        running = False

        # Draw the pop-up
        popup.fill((50, 50, 50))  # Clear the pop-up background
        for i, (x, y, w, h) in enumerate(button_positions):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if x <= mouse_x - (screen.get_width() - popup_width) // 2 <= x + w and \
               y <= mouse_y - (screen.get_height() - popup_height) // 2 <= y + h:
                pygame.draw.rect(popup, button_hover_color, (x, y, w, h))
            else:
                pygame.draw.rect(popup, button_color, (x, y, w, h))
            text = font.render(items_list[i], True, text_color)
            popup.blit(text, (x + (w - text.get_width()) // 2, y + (h - text.get_height()) // 2))

        # Blit the pop-up onto the main screen
        screen.blit(popup, ((screen.get_width() - popup_width) // 2, (screen.get_height() - popup_height) // 2))
        pygame.display.flip()

    if selected_item:
        print(f"You selected: {selected_item}")
        # Randomly select an item with more odds to the selected item
        item = random.choices([selected_item] + items_list, weights=[3] + [1] * len(items_list), k=1)[0]
        inventory.append(item)
        print(f"Item obtained: {item}")
    else:
        print("No item selected. No item obtained.")

# Define the color for the walkable grid cells
grid_color = (255, 255, 255)  # White

# Function to draw the grid and give the corresponding color to the cells
def draw_grid(grid):
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1 or grid[y][x] == "Enemy" or grid[y][x] == "Item":
                pygame.draw.rect(screen, grid_color, (x * box_size, y * box_size, box_size, box_size), 1)
            elif grid[y][x] == 2:
                pygame.draw.rect(screen, (255, 0, 0), (x * box_size, y * box_size, box_size, box_size))  # Red for non-colliding positions
            elif grid[y][x] == "Cleared":
                pygame.draw.rect(screen, (0, 255, 0), (x * box_size, y * box_size, box_size, box_size))
            elif grid[y][x] == "Runaway":
                pygame.draw.rect(screen, (0, 0, 255), (x * box_size, y * box_size, box_size, box_size))
            elif grid[y][x] == "Win":
                pygame.draw.rect(screen, (255, 255, 0), (x * box_size, y * box_size, box_size, box_size), 1)  # Yellow for the winning cell

# Function to reload the map after the correct cell has been found
def reload_map():
    global grid, dot_position, randomWinCell, gameWinCell
    gameWinCell = None
    randomWinCell = 20
    screen.fill((0, 0, 0))  # Fill the screen with a black background
    grid = starting_grid()  # Generate a new starting grid
    draw_grid(grid)  # Draw the grid on the screen
    pygame.display.flip()  # Update the display
    print("Screen cleared.")

# Define the initial position of the red dot
dot_position = [cols // 2, rows - 2]

# Define the color for the red dot
dot_color = (255, 0, 0)

# Function to draw the red dot/player
def draw_dot(position):
    if position is not None:  # Only draw the dot if the position is not None
        pygame.draw.circle(screen, dot_color, (position[0] * box_size + box_size // 2, position[1] * box_size + box_size // 2), box_size // 4)
    else:
        # Clear the screen or redraw the grid to remove the dot
        screen.fill((0, 0, 0))  # Fill the screen with a black background

# Function to check what cell the player is trying to move to and if it's a valid move
def can_move_to(position, grid):
    global cellGameWon
    if position != None:
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
        elif grid[y][x] == "Win":
            print("Win cell reached. Reloading map...")
            reload_map()
            position[0] = 24
            position[1] = 26
            cellGameWon = False
            return grid[y][x] == "Win"
        elif grid[y][x] == "Cleared":
            return True
        elif grid[y][x] == "Item":  # Allow movement onto "Item" cells
            obtain_item_selection()  # Call the item selection function
            print("Item collected!")
            print("Inventory:", inventory)  # Print the inventory after collecting the item
            grid[y][x] = "Cleared"  # Mark the cell as cleared after collecting the item
            return True
        else:
            return grid[y][x] == 1
    return False

# Main game loop
running = True
grid = starting_grid()
while running:
    if dot_position is None:
        print("Dot position is None")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not battle_in_progress:  # Disable input during battle
            if dot_position != None:  # Only process movement if the dot exists
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

    # Draw the red dot only if dot_position is not None
    if dot_position is not None:
        draw_dot(dot_position)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
