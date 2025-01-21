import pygame
import sys
import subprocess
import time
import random

# Initialize Pygame
pygame.init()

# Read character name from command-line arguments
if len(sys.argv) > 1:
    character_name = sys.argv[1]
else:
    character_name = "Unknown"

# Set up the display
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption(f"Simple Pygame Window - {character_name}")

character_stats = {
    "Gunner": "Health: 100\nAttack: 55\nDefense: 35",
    "Swordman": "Health: 120\nAttack: 40\nDefense: 40",
    "Warlock": "Health: 80\nAttack: 70\nDefense: 20"
}

box_size = 25
cols = 1200 // box_size
rows = 700 // box_size

# Initialize the grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]
red_boxes = set()  # Set to keep track of red boxes

# Directions for moving in the grid
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def is_valid(x, y):
    return 0 <= x < cols and 0 <= y < rows

def generate_random_grid(start_x, start_y):
    width = random.randint(2, 5)
    height = random.randint(2, 5)
    for y in range(start_y, start_y + height):
        for x in range(start_x, start_x + width):
            if is_valid(x, y):
                grid[y][x] = 1

def move_dot(x, y, direction):
    if direction == 'w' and is_valid(x, y - 1):
        if grid[y - 1][x] == 1:
            y -= 1
        else:
            if not check_existing_box(x, y - 1, 'w'):
                generate_new_grid(x, y - 1, 'w')
                y -= 1
            else:
                shake_dot()
                mark_box_red(x, y - 1)
    elif direction == 's' and is_valid(x, y + 1):
        if grid[y + 1][x] == 1:
            y += 1
        else:
            if not check_existing_box(x, y + 1, 's'):
                generate_new_grid(x, y + 1, 's')
                y += 1
            else:
                shake_dot()
                mark_box_red(x, y + 1)
    elif direction == 'a' and is_valid(x - 1, y):
        if grid[y][x - 1] == 1:
            x -= 1
        else:
            if not check_existing_box(x - 1, y, 'a'):
                generate_new_grid(x - 1, y, 'a')
                x -= 1
            else:
                shake_dot()
                mark_box_red(x - 1, y)
    elif direction == 'd' and is_valid(x + 1, y):
        if grid[y][x + 1] == 1:
            x += 1
        else:
            if not check_existing_box(x + 1, y, 'd'):
                generate_new_grid(x + 1, y, 'd')
                x += 1
            else:
                shake_dot()
                mark_box_red(x + 1, y)
    return x, y

def check_existing_box(x, y, direction):
    if direction == 'w':
        start_x = x - 1
        start_y = y - 2
    elif direction == 's':
        start_x = x - 1
        start_y = y + 1
    elif direction == 'a':
        start_x = x - 2
        start_y = y - 1
    elif direction == 'd':
        start_x = x + 1
        start_y = y - 1

    width = random.randint(2, 5)
    height = random.randint(2, 5)
    for y in range(start_y, start_y + height):
        for x in range(start_x, start_x + width):
            if is_valid(x, y) and grid[y][x] == 1:
                return True
    return False

def generate_new_grid(dot_x, dot_y, direction):
    if direction == 'w':
        start_x = dot_x - 1
        start_y = dot_y - 2
    elif direction == 's':
        start_x = dot_x - 1
        start_y = dot_y + 1
    elif direction == 'a':
        start_x = dot_x - 2
        start_y = dot_y - 1
    elif direction == 'd':
        start_x = dot_x + 1
        start_y = dot_y - 1

    generate_random_grid(start_x, start_y)
    grid[dot_y][dot_x] = 1  # Ensure the box with the dot always has borders

def shake_dot():
    global shake_offset_x, shake_offset_y
    shake_offset_x = random.randint(-2, 2)
    shake_offset_y = random.randint(-2, 2)

def mark_box_red(x, y):
    global red_boxes
    red_boxes.add((x, y))

# Main loop
running = True
generate_random_grid(cols // 2 - 1, rows - 3)  # Call the function to generate the initial random grid
dot_x, dot_y = cols // 2, rows - 2  # Start the dot in the middle of the initial grid
grid[dot_y][dot_x] = 1  # Ensure the initial box with the dot has borders
shake_offset_x, shake_offset_y = 0, 0  # Initialize shake offsets

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dot_x, dot_y = move_dot(dot_x, dot_y, 'w')
            elif event.key == pygame.K_s:
                dot_x, dot_y = move_dot(dot_x, dot_y, 's')
            elif event.key == pygame.K_a:
                dot_x, dot_y = move_dot(dot_x, dot_y, 'a')
            elif event.key == pygame.K_d:
                dot_x, dot_y = move_dot(dot_x, dot_y, 'd')

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw the grid with white borders
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1:
                color = (255, 0, 0) if (x, y) in red_boxes else (255, 255, 255)
                pygame.draw.rect(screen, color, pygame.Rect(x * box_size, y * box_size, box_size, box_size), 1)

    # Draw the dot with a small random offset to make it shake
    pygame.draw.circle(screen, (255, 0, 0), (dot_x * box_size + box_size // 2 + shake_offset_x, dot_y * box_size + box_size // 2 + shake_offset_y), box_size // 4)

    # Reset shake offsets
    shake_offset_x, shake_offset_y = 0, 0

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
