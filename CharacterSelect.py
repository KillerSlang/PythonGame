import pygame
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Character Selection")

button_sword_x = (WINDOW_WIDTH - 300) // 2
button_sword_y = (WINDOW_HEIGHT - 600) // 2

button_gun_x = button_sword_x - 400
button_gun_y = button_sword_y

button_warlock_x = button_sword_x + 400
button_warlock_y = button_sword_y

character_stats = {
    "Gunner": "Health: 100\nAttack: 55\nDefense: 35",
    "Swordman": "Health: 120\nAttack: 40\nDefense: 40",
    "Warlock": "Health: 80\nAttack: 70\nDefense: 20"
}

def show_character_dialog(character_name):
    def on_select():
        root.destroy()
        pygame.quit()
        subprocess.run(["python", "Game.py", character_name])
        sys.exit()

    def on_back():
        root.destroy()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    stats = character_stats.get(character_name, "No stats available")
    
    dialog = tk.Toplevel(root)
    dialog.title(f"{character_name} Stats")
    label = tk.Label(dialog, text=stats)
    label.pack(pady=10)
    
    button_frame = tk.Frame(dialog)
    button_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    back_button = tk.Button(button_frame, text="Back", command=on_back)
    back_button.pack(side=tk.LEFT, anchor='sw', padx=5, pady=5)
    
    select_button = tk.Button(button_frame, text="Select", command=on_select)
    select_button.pack(side=tk.RIGHT, anchor='se', padx=5, pady=5)
    
    # Set the size of the dialog window
    dialog_width = 400
    dialog_height = 300
    
    # Center the dialog on the screen
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')
    
    dialog.deiconify()  # Show the dialog window
    root.mainloop()

def gun():
    show_character_dialog("Gunner")

def sword():
    show_character_dialog("Swordman")

def warlock():
    show_character_dialog("Warlock")

def draw_button():
    pygame.draw.rect(window, "white", (button_gun_x, button_gun_y, 300, 600))
    pygame.draw.rect(window, "blue", (button_sword_x, button_sword_y, 300, 600))
    pygame.draw.rect(window, "purple", (button_warlock_x, button_warlock_y, 300, 600))
    font = pygame.font.Font(None, 36)
    text_gun = font.render("Gunner", True, (255, 0, 0))
    text_rect_gun = text_gun.get_rect(center=(button_gun_x + 150, button_gun_y + 300))
    window.blit(text_gun, text_rect_gun)
    text_sword = font.render("Swordman", True, (255, 0, 0))
    text_rect_sword = text_sword.get_rect(center=(button_sword_x + 150, button_sword_y + 300))
    window.blit(text_sword, text_rect_sword)
    text_warlock = font.render("Warlock", True, (255, 0, 0))
    text_rect_warlock = text_warlock.get_rect(center=(button_warlock_x + 150, button_warlock_y + 300))
    window.blit(text_warlock, text_rect_warlock)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_gun_x <= mouse_pos[0] <= button_gun_x + 300 and button_gun_y <= mouse_pos[1] <= button_gun_y + 600:
                gun()
            elif button_sword_x <= mouse_pos[0] <= button_sword_x + 300 and button_sword_y <= mouse_pos[1] <= button_sword_y + 600:
                sword()
            elif button_warlock_x <= mouse_pos[0] <= button_warlock_x + 300 and button_warlock_y <= mouse_pos[1] <= button_warlock_y + 600:
                warlock()

    window.fill((0, 0, 0))

    draw_button()

    pygame.display.flip()

pygame.quit()
sys.exit()