import pygame
import sys
import subprocess
import random
import tkinter as tk
from tkinter import messagebox
import time
import json  # Add this import for JSON deserialization

pygame.init()

# Healthbar for player?

# Get character name from command line arguments
character_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"

# Get enemy counter
enemycounter = int(sys.argv[2]) if len(sys.argv) > 2 else 0
print(f"Enemy counter: {enemycounter}")

# Parse the inventory from command-line arguments
inventory = json.loads(sys.argv[3]) if len(sys.argv) > 3 else []

# Function to calculate enemy health depending on enemy counter
def enemy_health(enemycounter):
    return 100 * enemycounter

# Function to calculate enemy accuracy depending on enemy counter
def enemy_accuracy(enemycounter):
    accuracy = 10 * enemycounter
    if 80 < accuracy < 150:
        accuracy = 80
    elif accuracy < 40:
        accuracy = 40
    elif accuracy > 150:
        accuracy = 90
    return accuracy

# Function to calculate enemy damage depending on enemy counter
def enemy_damage(enemycounter):
    damage = 10 * (enemycounter / 2)
    halfDamage = damage / 2
    damage = random.randint(int(halfDamage), int(damage))
    if damage < 5:
        damage = 5
    elif damage > 40:
        damage = 40
    return damage

# Function to make enemy
def make_enemy():
    return {"health": enemy_health(enemycounter), "accuracy": enemy_accuracy(enemycounter)}

# Initialize screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption(f"Battle Time - {character_name}")

# Button properties
button_width, button_height = 460, 80
button_margin = 20
button_color, button_text_color = (0, 128, 255), (255, 255, 255)
font = pygame.font.Font(None, 36)

# Load enemy image
enemy_image = pygame.image.load("Images/hive_thrall.webp")

# Load slash image
slash_image = pygame.image.load("Images/Slash.png")

# Set desired width and height for the enemy image
enemy_width, enemy_height = 1200, 500

# Scale the enemy image to the desired size
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

enemy_rect = enemy_image.get_rect()

# Calculate position to center the image above the buttons
enemy_x = (screen.get_width() - enemy_rect.width) // 2
enemy_y = screen.get_height() - (2 * button_height + button_margin) - enemy_rect.height - 20

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
    screen.get_height() - 80,
    280,
    80
)

# Define the "Items" button rectangle
items_button_rect = pygame.Rect(
    screen.get_width() - 300,
    screen.get_height() - 180,
    280,
    80
)

# Give tutorial pop-up message if first fight
if enemycounter == 1:
    subprocess.run(["python", "Tutorial.py"])

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

attack_enemy_list = ["Tackle", "Scratch", "Block", "Recovery"]

last_items_used = []

last_enemy_attack = None

last_player_attack = None

# Function to make character
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
    global last_player_attack, last_items_used
    print(f"Last item used: {last_items_used}")
    print(f"{character_name} used {attack_name}! Damage: {stats['damage']}, Accuracy: {stats['accuracy']}%")
    player_action()
    if attack_name != "Block" and attack_name != "Dodge" and attack_name != "Cloak":
        hitOrMiss = random.randint(1, 100)
        if "Accuracy Potion" in last_items_used:
            stats["accuracy"] += 20
            print(f"Accuracy increased to {stats['accuracy']}%")
        if hitOrMiss <= stats["accuracy"]:
            print("You hit!")
            print("last attack: ", f"{last_enemy_attack}")
            if "Damage Boost" in last_items_used:
                stats["damage"] *= 2
                print(f"Damage increased to {stats['damage']}")
            if attack_name == "Drain Life":
                character["health"] += 10
                print(f"Character health: {character['health']}")
                if last_enemy_attack == "Block":
                    print("Block detected while Drain Life")
                    original_damage = stats["damage"]
                    stats["damage"] = stats["damage"] // 2
                    enemy["health"] -= stats["damage"]
                    print(f"Enemy health: {enemy['health']}")
                    slash_animation()
                    shake_image(enemy_image, enemy_x, enemy_y, screen, character_name, attack_name)
                    stats["damage"] = original_damage
                else:
                    enemy["health"] -= stats["damage"]
                    print(f"Enemy health: {enemy['health']}")
                    slash_animation()
                    shake_image(enemy_image, enemy_x, enemy_y, screen, character_name, attack_name)
            else:
                if last_enemy_attack == "Block":
                    print("Block detected")
                    original_damage = stats["damage"]
                    stats["damage"] = stats["damage"] // 2
                    enemy["health"] -= stats["damage"]
                    print(f"Enemy health: {enemy['health']}")
                    slash_animation()
                    shake_image(enemy_image, enemy_x, enemy_y, screen, character_name, attack_name)
                    stats["damage"] = original_damage
                else:
                    enemy["health"] -= stats["damage"]
                    print(f"Enemy health: {enemy['health']}")
                    slash_animation()
                    shake_image(enemy_image, enemy_x, enemy_y, screen, character_name, attack_name)
            last_player_attack = attack_name
            if enemy["health"] <= 0:
                print("Win condition met")
                game_won()
                sys.stdout.flush()
                time.sleep(1)
                result = "Win"
                print(result)
                sys.stdout.flush()
                pygame.quit()
                sys.exit()
            else:
                if "Speed Boost" in last_items_used:
                    print("Speed Boost detected")
                enemy_attack()
        else:
            print("You missed!")
            player_miss()
            enemy_attack()
    elif attack_name == "Block" or attack_name == "Dodge" or attack_name == "Cloak":
        last_player_attack = attack_name
        print("You blocked!")
        enemy_attack()

    # Clear the last_items_used list but keep "Weaken Potion"
    last_items_used = [item for item in last_items_used if item == "Weaken Potion"]

# Function to handle enemy attack
def enemy_attack():
    global last_enemy_attack, last_items_used
    print(f"Items used by player: {last_items_used}")
    
    # Prevent enemy attack if "Speed Boost" is in last_items_used
    if "Speed Potion" in last_items_used:
        print("Speed Boost active, skipping enemy attack.")
        return

    Start_time = time.time()
    while time.time() - Start_time < 0.5:
        pass
    hitOrMiss = random.randint(1, 100)
    attack_enemy = random.choice(attack_enemy_list)
    print(f"Enemy used {attack_enemy}!")
    enemy_action(attack_enemy)
    if attack_enemy == "Tackle" or attack_enemy == "Scratch":
        last_enemy_attack = attack_enemy
        if hitOrMiss <= enemy["accuracy"]:
            EnemyHitDamage = enemy_damage(enemycounter)
            if "Weaken Potion" in last_items_used:
                previous_attack = EnemyHitDamage
                EnemyHitDamage /= 2
                print(f"Enemy attack decreased from {previous_attack} to {EnemyHitDamage}")
            print("Enemy hit!")
            print("Enemy hit damage: ", EnemyHitDamage)
            print("last player attack: ", f"{last_player_attack}")
            red_screen_overlay(screen)
            if last_player_attack == "Block":
                EnemyHitDamage = EnemyHitDamage // 2
                print(f"Enemy dealt {EnemyHitDamage} damage!")
                character["health"] -= EnemyHitDamage
                enemy_hit(EnemyHitDamage)
                player_health_check()
            else:
                print(f"Enemy dealt {EnemyHitDamage} damage!")
                character["health"] -= EnemyHitDamage
                enemy_hit(EnemyHitDamage)
                player_health_check()
            
            # Remove "Weaken Potion" from last_items_used after the enemy attack hits
            if "Weaken Potion" in last_items_used:
                last_items_used.remove("Weaken Potion")
            
            print(f"Character health: {character['health']}")
            if character["health"] <= 0:
                print("You lost!")
                sys.stdout.flush()
                time.sleep(1)
                result = "Lose"
                print(result)
                sys.stdout.flush()
                pygame.quit()
                sys.exit()
        else:
            enemy_miss()
            print("Enemy missed!")
    elif attack_enemy == "Block":
        last_enemy_attack = attack_enemy
        print("Enemy blocked!")
        enemy_action(attack_enemy)
    elif attack_enemy == "Recovery":
        last_enemy_attack = attack_enemy
        print("Enemy recovered health!")
        enemy["health"] += 10
        print(f"Enemy health: {enemy['health']}")
        enemy_action(attack_enemy)

# function to tell the player what the enemy does
def enemy_action(attack_enemy_name):
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    if attack_enemy_name != "Recovery":
        text_surface = font.render(f"Enemy used {attack_enemy_name}!", True, (255, 255, 255))
    elif attack_enemy_name == "Recovery":
        text_surface = font.render(f"Enemy used {attack_enemy_name} and has recovered 10 health!", True, (255, 255, 255))

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to handle escape attempt
def escape():
    escape_attempt()
    if random.choice([0, 3]) == 0:
        escape_success()
        print("Escaped!")
        sys.stdout.flush()
        time.sleep(1)
        result = "RunAway"
        print(result)
        sys.stdout.flush()
        pygame.quit()
        sys.exit()
    else:
        print("You failed to escape!")
        escape_failed()
        enemy_attack()

def slash_animation():
    start_time = time.time()
    image_width = slash_image.get_width()
    image_height = slash_image.get_height()

    # Initially the image is completely hidden
    visible_width = 0  # Initially 0 width to hide the image

    # Animate the slash appearing from right to left
    while time.time() - start_time < 0.5:  # 0.5 seconds for the reveal

        # Increase the visible width to reveal the image from right to left
        visible_width = int(image_width * (time.time() - start_time) / 0.5)

        # Draw only the visible portion of the slash image (reveal from right to left)
        visible_image = slash_image.subsurface(0, 0, visible_width, image_height)
        screen.blit(visible_image, (enemy_x, enemy_y))

        pygame.display.flip()
        pygame.time.delay(10)  # Adding a small delay for smoother animation

    # Hold the image fully visible for a short time (optional)
    pygame.time.delay(300)  # Pause for 0.3 seconds before disappearing
# Function to show the player they got hit
def red_screen_overlay(screen, alpha=20):
    """
    Creates a semi-transparent red overlay on the entire screen.
    
    :param screen: The pygame display surface.
    :param alpha: The transparency level (0 = fully transparent, 255 = fully opaque).
    """
    start_time = time.time()
    while time.time() - start_time < 0.5:
        red_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # Create transparent surface
        red_overlay.fill((255, 0, 0, alpha))  # Fill with red (RGBA format)
        screen.blit(red_overlay, (0, 0))  # Draw overlay onto the screen
        pygame.display.flip()  # Update display

# Function to tell the player their action
def player_action():
    """
    Display an action message in a black box with a white border.
    
    :param action_text: The text to display inside the box.
    """
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name} used {attack_name}!", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to show the player how much damage they took
def enemy_hit(damage):
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name} took {damage} damage!", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

def player_health_check():
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name} has {character['health']} health left", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to shake the enemy to show hit
def shake_image(image, x, y, screen, character, attack, duration=500):
    """
    Shake the image horizontally to indicate it has been hit.

    :param image: The image to shake.
    :param x: The x-coordinate where the image is drawn.
    :param y: The y-coordinate where the image is drawn.
    :param screen: The screen to draw the image on.
    :param character: The character whose intensity will be used.
    :param attack: The type of attack made.
    :param duration: The duration of the shake in milliseconds.
    """
    # Define intensity based on character and attack
    intensity_map = {
        'Swordman': {'Slash': 10, 'Strike': 15, 'Charge': 20, 'Block': 0},
        'Warlock': {'Fireball': 15, 'Shadow Bolt': 20, 'Drain Life': 10, 'Cloak': 0},
        'Gunner': {'Shoot': 15, 'Stab': 10, 'Grenade': 20, 'Dodge': 0}
    }
    intensity = intensity_map.get(character, {}).get(attack, 10)  # Default intensity is 10

    original_x = x  # Store original x position
    elapsed_time = 0
    clock = pygame.time.Clock()

    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = x + (image.get_width() // 2) - (box_width // 2)
    box_y = y + (image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"Enemy took {stats['damage']} damage!", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while elapsed_time < duration:
        offset_x = random.randint(-intensity, intensity)  # Horizontal shake

        # Redraw enemy image in new position (shaken)
        screen.blit(image, (original_x + offset_x, y))

        # Show the black box with a white border
        if time.time() - start_time < 5.0:  # Show for 1.0 seconds (extended from 0.5 seconds)
            pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
            # Blit the text onto the screen
            text_x = box_x + (box_width - text_surface.get_width()) // 2
            text_y = box_y + (box_height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()
        elapsed_time += clock.tick(60)  # Update elapsed time

    # Clear the box after duration
    screen.fill((0, 0, 0))
    screen.blit(image, (original_x, y))
    pygame.display.flip()

# Function to tell the player they missed
def player_miss():
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name}'s attack missed....", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to tell the player the enemy missed
def enemy_miss():
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"Enemy's attack missed", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to show the player they won
def game_won():
    """
    Display an action message in a black box with a white border.
    
    :param action_text: The text to display inside the box.
    """
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render("Enemy has been slain, you have won!!", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 1.0:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_wait = font.render("Please wait....", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 1.0:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_wait.get_width()) // 2
        text_y = box_y + (box_height - text_wait.get_height()) // 2
        screen.blit(text_wait, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to show the player they tried to escape
def escape_attempt():
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name} attempts to escape", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to show the player they failed to escape
def escape_failed():
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name}'s escape failed....", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to show the player they successfully escaped
def escape_success():
    # Box position (in front of the enemy)
    box_width, box_height = 1200, 100
    box_x = enemy_x + (enemy_image.get_width() // 2) - (box_width // 2)
    box_y = enemy_y + (enemy_image.get_height() - box_height)

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_surface = font.render(f"{character_name} escaped successfully", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = box_y + (box_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    font = pygame.font.SysFont('Arial', 30)  # Choose font and size
    text_wait = font.render("Please wait....", True, (255, 255, 255))  # Render text

    start_time = time.time()

    while time.time() - start_time < 1.0:
        # Show the black box with a white border
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 5)  # White border
        
        # Blit the text onto the screen
        text_x = box_x + (box_width - text_wait.get_width()) // 2
        text_y = box_y + (box_height - text_wait.get_height()) // 2
        screen.blit(text_wait, (text_x, text_y))

        pygame.display.flip()

    screen.fill((0, 0, 0))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    pygame.display.flip()

# Function to show the enemy's healthbar
def draw_health_bar(screen, x, y, health, max_health, width=100, height=15):
    """Draws a health bar with color transitioning from green to red."""
    # Calculate health ratio
    health_ratio = max(health / max_health, 0)  # Ensure it doesn't go below 0
    
    # Interpolate color from green (0,255,0) to red (255,0,0)
    # Ensure red and green values are clamped between 0 and 255
    red = max(0, min(255, int((1 - health_ratio) * 255)))
    green = max(0, min(255, int(health_ratio * 255)))

    
    # Health bar background
    pygame.draw.rect(screen, (0,0,0), (x - 2, y - 2, width + 4, height + 4))  # Border
    pygame.draw.rect(screen, (red, green, 0), (x, y, int(width * health_ratio), height))  # Health


# Function to show inventory in a pop-up
def show_inventory(inventory):
    """
    Displays the inventory in a pop-up window and allows the player to use items.
    """
    def on_use_item():
        selected_item = listbox.get(tk.ACTIVE)
        if selected_item:
            use_item(selected_item)
            listbox.delete(tk.ACTIVE)  # Remove the item from the listbox
            root.destroy()  # Close the inventory window

    root = tk.Tk()
    root.title("Inventory")
    root.geometry("250x375")

    # Add a label for the inventory title
    label = tk.Label(root, text="Your Inventory", font=("Arial", 14))
    label.pack(pady=10)

    # Add a listbox to display the items
    listbox = tk.Listbox(root, font=("Arial", 12))
    for item in inventory:
        listbox.insert(tk.END, item)
    listbox.pack(pady=10)

    # Add a "Use Item" button
    use_button = tk.Button(root, text="Use Item", command=on_use_item, font=("Arial", 12))
    use_button.pack(pady=10)

    # Add a close button
    close_button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12))
    close_button.pack(pady=10)

    # Run the tkinter main loop
    root.mainloop()

def use_item(item_name):
    """
    Handles the usage of an item from the inventory.
    Removes the item from the inventory after use.
    """
    global inventory, last_items_used
    if item_name == "Health Potion":
        character["health"] += 20
        last_items_used.append(item_name)
        print(f"{character_name} used {item_name} and recovered 20 health!")
        print(f"Character health: {character['health']}")
    elif item_name == "Damage Boost":
        last_items_used.append(item_name)
        print(f"{character_name} used {item_name} and gained double damage!")
    elif item_name == "Weaken Potion":
        last_items_used.append(item_name)
        print(f"{character_name} used {item_name} and enemy is weakened!")
    elif item_name == "Speed Potion":
        last_items_used.append(item_name)
        print(f"{character_name} used {item_name} and gained another turn!")
    elif item_name == "Accuracy Potion":
        last_items_used.append(item_name)
        print(f"{character_name} used {item_name} and increased accuracy!")
    else:
        print(f"{item_name} has no effect.")

    # Remove the used item from the inventory
    inventory.remove(item_name)
    print(f"Remaining inventory: {inventory}")

    # Send the updated inventory back to the parent process
    print(json.dumps(inventory))
    sys.stdout.flush()

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
            elif items_button_rect.collidepoint(event.pos):
                show_inventory(inventory)  # Show inventory when items button is clicked
            for button_rect, (attack_name, stats) in zip(buttonsList, chosen_attacks()):
                if button_rect.collidepoint(event.pos):
                    attack(attack_name, stats)

    screen.fill((0, 0, 0))
    
    # Draw centered image above the buttons
    screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw the health bar at a fixed position relative to the window
    draw_health_bar(screen, screen.get_width() // 2 - 50, 50, enemy["health"], enemy_health(enemycounter))

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

    # Draw the "Items" button
    pygame.draw.rect(screen, button_color, items_button_rect)
    items_text_surface = font.render("Items", True, button_text_color)
    items_text_rect = items_text_surface.get_rect(center=items_button_rect.center)
    screen.blit(items_text_surface, items_text_rect)

    # Draw the "Escape" button
    pygame.draw.rect(screen, button_color, bottom_right_button_rect)
    escape_text_surface = font.render("Escape", True, button_text_color)
    escape_text_rect = escape_text_surface.get_rect(center=bottom_right_button_rect.center)
    screen.blit(escape_text_surface, escape_text_rect)

    pygame.display.flip()

import json

# At the end of the script, before exiting
# Serialize the updated inventory and print it
print(json.dumps(inventory))
sys.stdout.flush()

pygame.quit()
sys.exit()
