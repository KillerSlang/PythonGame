import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window size
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Fighting Tutorial")

# Button dimensions
button_width, button_height = 460, 80
button_margin = 20

# Buttons list
buttonsList = [
    pygame.Rect(button_margin + j * (button_width + button_margin),
                window_size[1] - (2 * button_height + button_margin) + i * (button_height + button_margin),
                button_width, button_height)
    for i in range(2) for j in range(2)
]

# Escape button
bottom_right_button_rect = pygame.Rect(
    window_size[0] - 300, window_size[1] - 180, 280, 180
)

show_stats = False  # Track if Tab is held

def draw_buttons():
    """Draws all the buttons and stats if TAB is held."""
    font = pygame.font.Font(None, 36)

    for button_rect in buttonsList:
        pygame.draw.rect(screen, (255, 0, 0), button_rect)  # Red button
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # White border

        button_text = font.render("Attack", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        
        if show_stats:
            text_rect.move_ip(0, -20)  # Move text up when stats are shown
            stats_surface = font.render("Stats: DMG 10, ACC 80%", True, (255, 255, 255))
            stats_rect = stats_surface.get_rect(center=button_rect.center)
            screen.blit(stats_surface, stats_rect.move(0, 20))  # Adjust position of stats text

        screen.blit(button_text, text_rect)

    # Draw bottom-right button (Exit)
    pygame.draw.rect(screen, (0, 255, 0), bottom_right_button_rect)  # Green
    pygame.draw.rect(screen, (255, 255, 255), bottom_right_button_rect, 2)  # White border

    exit_text = font.render("Escape", True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=bottom_right_button_rect.center)
    screen.blit(exit_text, exit_rect)

    # Check for escape button click
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bottom_right_button_rect.collidepoint(event.pos):
                tutorial_escape()

def show_tutorial_message(message, next_function):
    """Displays a tutorial message box above the buttons."""
    running_tutorial = True
    while running_tutorial:
        screen.fill((0, 0, 0))  # Clear screen
        draw_buttons()  # Keep buttons visible

        # Position tutorial box above buttons
        tutorial_box_y = buttonsList[0].top - 150
        stats_box = pygame.Rect(20, tutorial_box_y, 1240, 130)
        pygame.draw.rect(screen, (0, 0, 0), stats_box)
        pygame.draw.rect(screen, (255, 255, 255), stats_box, 2)

        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))
        screen.blit(text, (40, tutorial_box_y + 20))

        # Continue button
        continue_button = pygame.Rect(560, tutorial_box_y + 80, 200, 50)
        pygame.draw.rect(screen, (255, 50, 200), continue_button)
        continue_text = font.render("Continue", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        screen.blit(continue_text, continue_text_rect)

        pygame.display.flip()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    running_tutorial = False  # Exit message
                    next_function()  # Call next function

def tutorial_tab():
    """Displays TAB tutorial while allowing the TAB key to show stats."""
    global show_stats
    running_tutorial = True

    while running_tutorial:
        screen.fill((0, 0, 0))  # Clear screen
        draw_buttons()  # Keep buttons visible

        # Move tutorial box above buttons
        tutorial_box_y = buttonsList[0].top - 150
        stats_box = pygame.Rect(20, tutorial_box_y, 1240, 130)
        pygame.draw.rect(screen, (0, 0, 0), stats_box)
        pygame.draw.rect(screen, (255, 255, 255), stats_box, 2)

        font = pygame.font.Font(None, 36)
        text = font.render("Holding TAB shows attack stats like damage & hit chance.", True, (255, 255, 255))
        bottom_text = font.render("Try it out by holding TAB", True, (255, 255, 255))

        screen.blit(text, (40, tutorial_box_y + 20))
        screen.blit(bottom_text, (40, tutorial_box_y + 60))

        # Continue button
        continue_button = pygame.Rect(560, tutorial_box_y + 80, 200, 50)
        pygame.draw.rect(screen, (255, 50, 200), continue_button)
        continue_text = font.render("Continue", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        screen.blit(continue_text, continue_text_rect)

        pygame.display.flip()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    show_stats = True  # Enable stats display
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    show_stats = False  # Disable stats display
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    running_tutorial = False  # Exit tutorial
                    tutorial_healthbar()  # Call tutorial_healthbar after clicking Continue

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

def tutorial_healthbar():
    """Displays a health bar tutorial."""
    running_tutorial = True
    health = 100
    max_health = 100

    while running_tutorial:
        screen.fill((0, 0, 0))  # Clear screen
        draw_buttons()  # Keep buttons visible

        # Draw health bar
        health_bar_x = screen.get_width() // 2 - 50
        health_bar_y = 50
        draw_health_bar(screen, health_bar_x, health_bar_y, health, max_health)

        # Position tutorial box underneath the health bar
        tutorial_box_y = health_bar_y + 50 + 20  # 20 pixels below the health bar
        stats_box = pygame.Rect(20, tutorial_box_y, 1240, 130)
        pygame.draw.rect(screen, (0, 0, 0), stats_box)
        pygame.draw.rect(screen, (255, 255, 255), stats_box, 2)

        font = pygame.font.Font(None, 36)
        text = font.render("This is the enemy health bar. It shows your enemy's current health.", True, (255, 255, 255))
        bottom_text = font.render("Enemies will die if their health reaches 0, however they can recover health each turn.", True, (255, 255, 255))

        screen.blit(text, (40, tutorial_box_y + 20))
        screen.blit(bottom_text, (40, tutorial_box_y + 60))

        # Continue button
        continue_button = pygame.Rect(560, tutorial_box_y + 350, 200, 50)
        pygame.draw.rect(screen, (255, 50, 200), continue_button)
        continue_text = font.render("Continue", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        screen.blit(continue_text, continue_text_rect)

        pygame.display.flip()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    running_tutorial = False  # Exit tutorial
                    tutorial_escape()  # Call tutorial_escape after clicking Continue

        # Decrease health over time
        health -= 2  # Adjust the decrement value as needed
        if health < 0:
            health = 100  # Ensure health doesn't go below 0

        pygame.time.delay(100)  # Add a delay to control the speed of health decrease

def tutorial_escape():
    """Displays a message explaining the escape button and closes the window when clicked."""
    running_tutorial = True
    while running_tutorial:
        screen.fill((0, 0, 0))  # Clear screen
        draw_buttons()  # Keep buttons visible

        # Position tutorial box above buttons
        tutorial_box_y = buttonsList[0].top - 150
        stats_box = pygame.Rect(20, tutorial_box_y, 1240, 130)
        pygame.draw.rect(screen, (0, 0, 0), stats_box)
        pygame.draw.rect(screen, (255, 255, 255), stats_box, 2)

        font = pygame.font.Font(None, 36)
        text = font.render("Click the Escape button to close the window.", True, (255, 255, 255))
        screen.blit(text, (40, tutorial_box_y + 20))

        pygame.display.flip()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bottom_right_button_rect.collidepoint(event.pos):
                    running_tutorial = False  # Exit tutorial
                    pygame.quit()
                    sys.exit()

# Start tutorial with welcome message, then go to TAB tutorial
show_tutorial_message("Welcome to the fighting tutorial! Here you'll learn the mechanics.", tutorial_tab)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen
    draw_buttons()  # Keep buttons visible

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                show_stats = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                show_stats = False

    pygame.display.flip()  # Update the display

# Quit Pygame
pygame.quit()
sys.exit()
