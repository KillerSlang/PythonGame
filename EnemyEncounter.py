import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
import time

pygame.init()

# Healthbars
# Return value of win or run away from battle to main game

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
    halfDamage = damage / 2
    damage = random.randint(int(halfDamage), int(damage))

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

attack_enemy_list = ["Tackle", "Scratch", "Block", "Recovery"]

last_enemy_attack = None

last_player_attack = None

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
    global last_player_attack
    print(f"{character_name} used {attack_name}! Damage: {stats['damage']}, Accuracy: {stats['accuracy']}%")
    player_action()
    if attack_name != "Block" and attack_name != "Dodge" and attack_name != "Cloak":
        hitOrMiss = random.randint(1, 100)
        if hitOrMiss <= stats["accuracy"]:
            print("You hit!")
            print("last attack: ", f"{last_enemy_attack}")
            if attack_name == "Drain Life": # Not fully functional
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
            else :
                enemy_attack()
        else:
            print("You missed!")
            player_miss()
            enemy_attack()
    elif attack_name == "Block" or attack_name == "Dodge" or attack_name == "Cloak":
        last_player_attack = attack_name
        print("You blocked!")
        enemy_attack()

def enemy_attack():
    global last_enemy_attack
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
            print("Enemy hit!")
            red_screen_overlay(screen)
            if last_player_attack == "Block":
                enemy["damage"] = enemy["damage"] // 2
                print(f"Enemy dealt {enemy['damage']} damage!")
                character["health"] -= enemy["damage"]
            else:
                print(f"Enemy dealt {enemy['damage']} damage!")
                character["health"] -= enemy["damage"]
            print(f"Character health: {character['health']}")
            if character["health"] <= 0:
                print("You lost!")
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
    
    # Draw centered image above the buttons
    screen.blit(enemy_image, (enemy_x, enemy_y))

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
