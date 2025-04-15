import pygame
import sys
import subprocess

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake's Game")

button_width = 200  # Set the new button width
button_height = 50  # Keep the height the same
button_x = (WINDOW_WIDTH - button_width) // 2  # Recalculate x to center the button
button_y = (WINDOW_HEIGHT - button_height) // 2 + 100  # Keep the y position the same

# Function to draw the button to run the character selection
def draw_button():
    button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)  # Adjust surface size
    button_surface.fill((0, 0, 0, 0))  # Make the surface fully transparent

    # Draw a rounded rectangle on the button surface
    pygame.draw.rect(button_surface, (255, 255, 255, 64), (0, 0, button_width, button_height), border_radius=50)

    window.blit(button_surface, (button_x, button_y))  # Blit the transparent surface onto the window

    font = pygame.font.Font(None, 36)
    text = font.render("Start Game", True, (255, 0, 0))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))  # Adjust text position
    window.blit(text, text_rect)

# Function to run the character selection
def run_char():
    pygame.quit()
    subprocess.run(["python", "CharacterSelect.py"])
    sys.exit()

# Load the background image and scale it to fit the window
background = pygame.image.load("Images/MainMenu.png")
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                run_char()
                running = False

    # Draw the background image
    window.blit(background, (0, 0))

    draw_button()

    pygame.display.flip()

pygame.quit()
sys.exit()