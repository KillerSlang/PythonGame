import pygame
import sys
import random

pygame.init()

if len(sys.argv) > 1:
    character_name = sys.argv[1]
else:
    character_name = "Unknown"

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
buttons = []
for i in range(2):
    for j in range(2):
        button_rect = pygame.Rect(
            button_margin + j * (button_width + button_margin),
            screen.get_height() - (2 * button_height + button_margin) + i * (button_height + button_margin),
            button_width,
            button_height
        )
        buttons.append(button_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw buttons
    for i, button_rect in enumerate(buttons):
        pygame.draw.rect(screen, button_color, button_rect)
        text_surface = font.render(f"Button {i+1}", True, button_text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()