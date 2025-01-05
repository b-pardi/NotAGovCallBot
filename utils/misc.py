import time
import pygame

def convert_timestamps_to_seconds(timestamp):
    m, s = map(int, timestamp.split(':'))
    return m * 60 + s

def notify():
    # Initialize Pygame
    pygame.init()
    
    # Setup the display
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Alert")

    # Define colors
    red = (255, 0, 0)
    white = (255, 255, 255)

    # Load and play sound
    pygame.mixer.init()
    pygame.mixer.music.load("res/coffin_dance.mp3")
    pygame.mixer.music.play()

    # Set the font for the text
    font = pygame.font.Font(None, 36)
    text = font.render("Found EDD AGENT", True, white)
    text_rect = text.get_rect(center=(width/2, height/2))

    # Event loop flag
    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with red
        screen.fill(red)
        
        # Blit the text onto the screen
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()