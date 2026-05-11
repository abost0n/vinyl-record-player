import pygame
from tkinter import Tk, filedialog

pygame.init()
pygame.mixer.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Vinyl Record Player")

clock = pygame.time.Clock()

rotation = 0
playing = False
music_loaded = False

# Hide tkinter window
root = Tk()
root.withdraw()

# Buttons
play_button = pygame.Rect(100, 600, 140, 50)

upload_button = pygame.Rect(300, 600, 220, 50)

def load_music():

    global music_loaded

    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )

    if file_path:

        pygame.mixer.music.load(file_path)

        music_loaded = True

def draw_record(angle):

    record_surface = pygame.Surface((400, 400), pygame.SRCALPHA)

    center = (200, 200)

    # Record
    pygame.draw.circle(record_surface, (10, 10, 10), center, 180)

    # Grooves
    for radius in range(80, 180, 8):
        pygame.draw.circle(record_surface, (40, 40, 40), center, radius, 1)

    # Center label
    pygame.draw.circle(record_surface, (200, 50, 50), center, 50)

    # Rotate
    rotated = pygame.transform.rotate(record_surface, angle)

    rect = rotated.get_rect(center=(500, 300))

    screen.blit(rotated, rect)

def draw_buttons():

    font = pygame.font.SysFont("Arial", 28)

    # Play button
    pygame.draw.rect(screen, (50, 200, 100), play_button)

    # Upload button
    pygame.draw.rect(screen, (120, 120, 120), upload_button)

    # Play text
    if playing:
        play_text = font.render("Pause", True, (0, 0, 0))
    else:
        play_text = font.render("Play", True, (0, 0, 0))

    upload_text = font.render("Upload Music", True, (0, 0, 0))

    screen.blit(play_text, (135, 610))

    screen.blit(upload_text, (325, 610))

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # Play button
            if play_button.collidepoint(mouse_pos):

                if music_loaded:

                    if playing:

                        pygame.mixer.music.pause()

                        playing = False

                    else:

                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.play()

                        playing = True

            # Upload button
            if upload_button.collidepoint(mouse_pos):

                load_music()

    screen.fill((25, 25, 30))

    # Spin record only when playing
    if playing:
        rotation += 1

    draw_record(rotation)

    draw_buttons()

    pygame.display.update()

pygame.quit()