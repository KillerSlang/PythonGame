import pygame
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load Image
image_path = "Images/Slash.png"

# Check if the image exists
if not os.path.exists(image_path):
    print(f"Error: {image_path} not found.")
    pygame.quit()
    exit()

image = pygame.image.load(image_path)  # Replace with your image path
image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Animation Variables
mask_width = image_rect.width  # Start fully visible
speed = 10  # Speed of transition
revealing = False  # Start by hiding

running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update mask width
    if revealing:
        mask_width += speed  # Increase mask width (reveal)
        if mask_width >= image_rect.width:
            revealing = False  # Switch to hiding
    else:
        mask_width -= speed  # Decrease mask width (hide from right)
        if mask_width <= 0:
            revealing = True  # Reset to reveal

    # Draw Image with Mask (Shift left to reveal from right)
    screen.blit(image, (image_rect.x + (image_rect.width - mask_width), image_rect.y), (image_rect.width - mask_width, 0, mask_width, image_rect.height))

    pygame.display.flip()  # Update display
    clock.tick(30)  # Control frame rate

pygame.quit()
