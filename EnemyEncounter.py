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

def enemy_accuracy(enemycounter):
    accuracy = 10 * enemycounter
    if 80 < accuracy < 150:
        accuracy = 80
    elif accuracy < 40:
        accuracy = 40
    elif accuracy > 150:
        accuracy = 90
    return accuracy

def enemy_damage(enemycounter):
    damage = 10 * (enemycounter / 2)
    if damage < 5:
        damage = 5
    elif damage > 40:
        damage = 40
    return damage

def make_enemy():
    return {"health": enemy_health(enemycounter), "damage": enemy_damage(enemycounter), "accuracy": enemy_accuracy(enemycounter)}

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
    root.withdraw()
    messagebox.showinfo("Enemy Encounter", "An enemy has appeared!")
    root.destroy()

# Character stats dictionary
character_stats = {
    "Gunner": {"health": 100, "attack": 55, "defense": 35},
    "Swordman": {"health": 120, "attack": 40, "defense": 40},
    "Warlock": {"health": 80, "attack": 70, "defense": 20}
}

# Attack stats dictionary
attack_stats = {
    "Fireball": {"damage": 30, "accuracy": 80},
    "Shadow Bolt": {"damage": 60, "accuracy": 55},
    "Drain Life": {"damage": 20, "accuracy": 90},
    "Cloak": {"damage": 0, "accuracy": 100},
    "Shoot": {"damage": 40, "accuracy": 75},
    "Stab": {"damage": 30, "accuracy": 85},
    "Grenade": {"damage": 50, "accuracy": 60},
    "Dodge": {"damage": 0, "accuracy": 100},
    "Slash": {"damage": 30, "accuracy": 85},
    "Strike": {"damage": 35, "accuracy": 80},
    "Charge": {"damage": 45, "accuracy": 70},
    "Block": {"damage": 0, "accuracy": 100},
    "Attack 1": {"damage": 10, "accuracy": 90},
    "Attack 2": {"damage": 15, "accuracy": 85},
    "Attack 3": {"damage": 20, "accuracy": 80},
    "Attack 4": {"damage": 25, "accuracy": 75}
}

def make_character(character_name):
    return {"health": character_stats[character_name]["health"], "attack": character_stats[character_name]["attack"], "defense": character_stats[character_name]["defense"]}

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
    return [(attack, attack_stats[attack]) for attack in attacks]

character = make_character(character_name)
enemy = make_enemy()
# Function to handle attack selection
def attack(attack_name, stats):
    print(f"{character_name} used {attack_name}! Damage: {stats['damage']}, Accuracy: {stats['accuracy']}%")
    hitOrMiss = random.randint(1, 100)
    if hitOrMiss <= stats["accuracy"]:
        print("You hit!")
        enemy["health"] -= stats["damage"]
        print(f"Enemy health: {enemy['health']}")
        if enemy["health"] <= 0:
            print("You won!")
            pygame.quit()
            sys.exit()
        else :
            enemy_attack()
    else:
        print("You missed!")
        enemy_attack()

def enemy_attack():
    hitOrMiss = random.randint(1, 100)
    if hitOrMiss <= enemy["accuracy"]:
        print("Enemy hit!")
        print(f"Enemy dealt {enemy['damage']} damage!")
        character["health"] -= enemy["damage"]
        print(f"Character health: {character['health']}")
        if character["health"] <= 0:
            print("You lost!")
            pygame.quit()
            sys.exit()
    else:
        print("Enemy missed!")

# Function to handle escape attempt
def escape():
    if random.choice([0, 3]) == 0:
        print("Escaped!")
        pygame.quit()
        sys.exit()
    else:
        print("You failed to escape!")

show_stats = False
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                show_stats = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                show_stats = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bottom_right_button_rect.collidepoint(event.pos):
                escape()
            for button_rect, (attack_name, stats) in zip(buttonsList, chosen_attacks()):
                if button_rect.collidepoint(event.pos):
                    attack(attack_name, stats)

    screen.fill((0, 0, 0))
    attacks_with_stats = chosen_attacks()

    # Draw attack buttons
    for i, (button_rect, (attack_name, stats)) in enumerate(zip(buttonsList, attacks_with_stats)):
        pygame.draw.rect(screen, button_color, button_rect)
        attack_name_y_offset = -10 if show_stats else 0
        text_surface = font.render(f"{attack_name}", True, button_text_color)
        text_rect = text_surface.get_rect(center=(button_rect.centerx, button_rect.centery + attack_name_y_offset))
        screen.blit(text_surface, text_rect)
        if show_stats:
            stats_text = f"Dmg: {stats['damage']} Acc: {stats['accuracy']}%"
            stats_surface = font.render(stats_text, True, button_text_color)
            stats_rect = stats_surface.get_rect(center=(button_rect.centerx, button_rect.centery + 20))
            screen.blit(stats_surface, stats_rect)

    pygame.draw.rect(screen, button_color, bottom_right_button_rect)
    escape_text_surface = font.render("Escape", True, button_text_color)
    escape_text_rect = escape_text_surface.get_rect(center=bottom_right_button_rect.center)
    screen.blit(escape_text_surface, escape_text_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
