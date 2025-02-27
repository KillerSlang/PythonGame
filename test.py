import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Enemy health properties
MAX_HEALTH = 100

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enemy Health Bar Example")

def draw_health_bar(screen, x, y, health, max_health, width=100, height=15):
    """Draws a health bar with color transitioning from green to red."""
    # Calculate health ratio
    health_ratio = max(health / max_health, 0)  # Ensure it doesn't go below 0
    
    # Interpolate color from green (0,255,0) to red (255,0,0)
    red = int((1 - health_ratio) * 255)
    green = int(health_ratio * 255)
    
    # Health bar background
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, width + 4, height + 4))  # Border
    pygame.draw.rect(screen, (red, green, 0), (x, y, int(width * health_ratio), height))  # Health

# Main loop
running = True
enemy_health = MAX_HEALTH
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press SPACE to deal damage
                enemy_health = max(enemy_health - 10, 0)

    # Draw the health bar at position (350, 250)
    draw_health_bar(screen, 350, 250, enemy_health, MAX_HEALTH)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
