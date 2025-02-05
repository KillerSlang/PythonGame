import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()

# Get character name from command line arguments
character_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"

# Get enemy counter
enemycounter = int(sys.argv[2]) if len(sys.argv) > 2 else 0
print(f"Enemy counter: {enemycounter}")

# Function to calculate enemy health
def enemy_health(enemycounter):
    return 100 * enemycounter

# Initialize screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption(f"Battle Time - {character_name}")

# Button properties
button_width, button_height = 460, 80
button_margin = 20
button_color, button_text_color = (0, 128, 255), (255, 255, 255)
font = pygame.font.Font(None, 36)

# Button list
buttonsList = []
for i in range(2):
    for j in range(2):
        button_rect = pygame.Rect(
            button_margin + j * (button_width + button_margin),
            screen.get_height() - (2 * button_height + button_margin) + i * (button_height + button_margin),
            button_width,
            button_height
        )
        buttonsList.append(button_rect)

# Escape button
bottom_right_button_rect = pygame.Rect(
    screen.get_width() - 300,
    screen.get_height() - 180,
    280,
    180
)

# Give tutorial pop-up message if first fight
if enemycounter == 1:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Enemy Encounter", "An enemy has appeared!")
    root.destroy()


# Attack stats dictionary (no cooldowns)
attack_stats = {
    "Fireball": {"damage": 30, "accuracy": 80},
    "Shadow Bolt": {"damage": 25, "accuracy": 85},
    "Drain Life": {"damage": 20, "accuracy": 90},
    "Cloak": {"damage": 0, "accuracy": 100},

    "Shoot": {"damage": 35, "accuracy": 75},
    "Stab": {"damage": 40, "accuracy": 70},
    "Grenade": {"damage": 50, "accuracy": 60},
    "Dodge": {"damage": 0, "accuracy": 100},

    "Slash": {"damage": 30, "accuracy": 85},
    "Strike": {"damage": 35, "accuracy": 80},
    "Charge": {"damage": 45, "accuracy": 65},
    "Block": {"damage": 0, "accuracy": 100},

    "Attack 1": {"damage": 10, "accuracy": 90},
    "Attack 2": {"damage": 15, "accuracy": 85},
    "Attack 3": {"damage": 20, "accuracy": 80},
    "Attack 4": {"damage": 25, "accuracy": 75}
}

# Function to get character-specific attacks
def chosen_attacks():
    if character_name == "Warlock":
        attacks = ["Fireball", "Shadow Bolt", "Drain Life", "Cloak"]
    elif character_name == "Gunner":
        attacks = ["Shoot", "Stab", "Grenade", "Dodge"]
    elif character_name == "Swordman":
        attacks = ["Slash", "Strike", "Charge", "Block"]
    else:
        attacks = ["Attack 1", "Attack 2", "Attack 3", "Attack 4"]

    # Return attack names and their stats
    return [(attack, attack_stats[attack]) for attack in attacks]

# Function to handle escape attempt
def escape():
    if random.choice([0, 3]) == 0:
        print("Escaped!")
        pygame.quit()
        sys.exit()
    else:
        print("You failed to escape!")

# Flag for showing attack stats
show_stats = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:  # When Tab is pressed, show stats
                show_stats = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:  # When Tab is released, hide stats
                show_stats = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bottom_right_button_rect.collidepoint(event.pos):
                escape()

    screen.fill((0, 0, 0))

    # Get character's attacks and stats
    attacks_with_stats = chosen_attacks()

    # Draw attack buttons
    for i, (button_rect, (attack_name, stats)) in enumerate(zip(buttonsList, attacks_with_stats)):
        pygame.draw.rect(screen, button_color, button_rect)

        # Adjust attack name position based on Tab key state
        attack_name_y_offset = -10 if show_stats else 0  # Move up if stats are shown

        # Render attack name (moves up when Tab is held)
        text_surface = font.render(f"{attack_name}", True, button_text_color)
        text_rect = text_surface.get_rect(center=(button_rect.centerx, button_rect.centery + attack_name_y_offset))
        screen.blit(text_surface, text_rect)

        # Render attack stats **only if Tab is held**
        if show_stats:
            stats_text = f"Dmg: {stats['damage']} Acc: {stats['accuracy']}%"
            stats_surface = font.render(stats_text, True, button_text_color)
            stats_rect = stats_surface.get_rect(center=(button_rect.centerx, button_rect.centery + 20))
            screen.blit(stats_surface, stats_rect)

    # Draw the escape button
    pygame.draw.rect(screen, button_color, bottom_right_button_rect)
    escape_text_surface = font.render("Escape", True, button_text_color)
    escape_text_rect = escape_text_surface.get_rect(center=bottom_right_button_rect.center)
    screen.blit(escape_text_surface, escape_text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
