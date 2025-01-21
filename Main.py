import pygame
import sys
import subprocess

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake's Game")

button_x = (WINDOW_WIDTH - 300) // 2
button_y = (WINDOW_HEIGHT - 50) // 2

def draw_button():
    pygame.draw.rect(window, "white", (button_x, button_y, 300, 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Start Game", True, (255, 0, 0))
    text_rect = text.get_rect(center=(button_x + 150, button_y + 25))
    window.blit(text, text_rect)

def run_char():
    pygame.quit()
    subprocess.run(["python", "CharacterSelect.py"])
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + 300 and button_y <= mouse_pos[1] <= button_y + 50:
                run_char()
                running = False

    window.fill((0, 0, 0))

    draw_button()

    pygame.display.flip()

pygame.quit()
sys.exit()