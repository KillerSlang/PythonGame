import pygame
import sys
import random

pygame.init()

if len(sys.argv) > 1:
    character_name = sys.argv[1]
else:
    character_name = "Unknown"

if len(sys.argv) > 2:
    enemycounter = int(sys.argv[2])
else:
    enemycounter = 0

print(f"Enemy counter: {enemycounter}")

# Set up the display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption(f"Battle Time - {character_name}")

# Define button properties
button_width = 460
button_height = 80
button_margin = 20
button_color = (0, 128, 255)
button_text_color = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Create button rects
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

# Create another button rect for the bottom right
bottom_right_button_rect = pygame.Rect(
    screen.get_width() - 300,
    screen.get_height() - 180,
    280, # Width
    180  # Height
)

def escape():
    can_escape = random.choice([0, 3])
    if can_escape == 0:
        print("Escaped!")
        pygame.quit()
        sys.exit()
    else:
        print("You failed to escape!")

def chosen_attacks():
    if character_name == "Warlock":
        attacks = ["Fireball", "Shadow Bolt", "Drain Life", "Cloak"]
    elif character_name == "Gunner":
        attacks = ["Shoot", "Stab",  "Grenade", "Dodge"]
    elif character_name == "Swordman":
        attacks = ["Slash", "Strike", "Charge", "Block"]
    else:
        attacks = ["Attack 1", "Attack 2", "Attack 3", "Attack 4"]
    return attacks
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bottom_right_button_rect.collidepoint(event.pos):
                escape()

    screen.fill((0, 0, 0))

    # Get the list of attacks based on the character
    attacks = chosen_attacks()

    # Draw buttonsList
    for i, button_rect in enumerate(buttonsList):
        pygame.draw.rect(screen, button_color, button_rect)
        text_surface = font.render(attacks[i], True, button_text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    # Draw the bottom right button separately
    pygame.draw.rect(screen, button_color, bottom_right_button_rect)
    text_surface = font.render("Escape", True, button_text_color)
    text_rect = text_surface.get_rect(center=bottom_right_button_rect.center)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()