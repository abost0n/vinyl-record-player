import pygame
import math
from tkinter import Tk, filedialog
from PIL import Image

pygame.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Interactive Vinyl Record Player")

clock = pygame.time.Clock()

# COLORS
BLACK = (10, 10, 10)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 100)

# VARIABLES
rotation = 0
playing = False
music_loaded = False
album_loaded = False

volume = 0.5

needle_angle = -40

album_cover_surface = None

record_center = (600, 350)

# Hide tkinter window
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

# BUTTONS
play_button = pygame.Rect(100, 680, 140, 50)

upload_music_button = pygame.Rect(280, 680, 220, 50)

upload_cover_button = pygame.Rect(540, 680, 220, 50)

# Volume slider
slider_rect = pygame.Rect(900, 700, 200, 10)

slider_x = 900 + int(volume * 200)

def load_music():

    global music_loaded

    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )

    if file_path:

        pygame.mixer.music.load(file_path)

        pygame.mixer.music.set_volume(volume)

        music_loaded = True

def load_album_cover():

    global album_cover_surface
    global album_loaded

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:

        image = Image.open(file_path)

        image = image.resize((200, 200))

        image = image.convert("RGBA")

        mode = image.mode
        size = image.size

        data = image.tobytes()

        album_cover_surface = pygame.image.fromstring(data, size, mode)

        album_loaded = True

def draw_record(angle):
    
    record_surface = pygame.Surface((500, 500), pygame.SRCALPHA)

    center = (250, 250)

    # Main vinyl
    pygame.draw.circle(record_surface, BLACK, center, 230)

    # Grooves
    # Grooves (enhanced visual depth)
for radius in range(70, 230, 8):

    pygame.draw.circle(
       
        (40, 40, 40),
        center,
        radius,
        1
    )

    # Center label
    pygame.draw.circle(record_surface, RED, center, 70)

    # Album cover
    if album_loaded and album_cover_surface:

        rect = album_cover_surface.get_rect(center=center)

        record_surface.blit(album_cover_surface, rect)

    # Rotate
    rotated = pygame.transform.rotate(record_surface, angle)

    rect = rotated.get_rect(center=record_center)

    screen.blit(rotated, rect)

def draw_buttons():

    font = pygame.font.SysFont("Arial", 28)

    # Buttons
    color = GREEN if playing else (120, 200, 120)

    pygame.draw.rect(screen, color, play_button, border_radius=10)

    pygame.draw.rect(screen, GRAY, upload_music_button, border_radius=10)

    pygame.draw.rect(screen, GRAY, upload_cover_button, border_radius=10)

    # Text
    if playing:
        play_text = font.render("Pause", True, BLACK)
    else:
        play_text = font.render("Play", True, BLACK)

    upload_text = font.render("Upload Music", True, BLACK)

    cover_text = font.render("Upload Cover", True, BLACK)

    screen.blit(play_text, (135, 690))

    screen.blit(upload_text, (315, 690))

    screen.blit(cover_text, (575, 690))

def draw_volume_slider():

    global slider_x

    # Slider line
    pygame.draw.rect(screen, WHITE, slider_rect)

    # Slider knob
    pygame.draw.circle(screen, RED, (slider_x, 705), 12)

    font = pygame.font.SysFont("Arial", 24)

    volume_text = font.render("Volume", True, WHITE)

    screen.blit(volume_text, (900, 660))

def handle_volume(mouse_x):

    global slider_x
    global volume

    slider_x = max(900, min(mouse_x, 1100))

    volume = (slider_x - 900) / 200

    pygame.mixer.music.set_volume(volume)

def draw_needle():

    global needle_angle

    base_x = 930
    base_y = 180

    length = 220

    if playing:
        target_angle = -15
    else:
        target_angle = -40

    needle_angle += (target_angle - needle_angle) * 0.05

    end_x = base_x + math.cos(math.radians(needle_angle)) * length

    end_y = base_y - math.sin(math.radians(needle_angle)) * length

    # Arm
    pygame.draw.line(
        screen,
        WHITE,
        (base_x, base_y),
        (end_x, end_y),
        8
    )

    # Base
    pygame.draw.circle(screen, WHITE, (base_x, base_y), 15)

def draw_title():

    font = pygame.font.SysFont("Arial", 42, bold=True)

    title = font.render(
        "Interactive Vinyl Record Player",
        True,
        WHITE
    )

    screen.blit(title, (320, 40))
def draw_button_outline(text, x, y, w, h):
    font = pygame.font.SysFont("Arial", 20)
    label = font.render(text, True, WHITE)

    pygame.draw.rect(screen, (80, 80, 80), (x, y, w, h), 2, border_radius=8)
    screen.blit(label, (x + 10, y + 12))
running = True

dragging_volume = False

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # Play
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

            # Upload music
            if upload_music_button.collidepoint(mouse_pos):

                load_music()

            # Upload cover
            if upload_cover_button.collidepoint(mouse_pos):

                load_album_cover()

            # Volume slider
            knob_rect = pygame.Rect(
                slider_x - 12,
                693,
                24,
                24
            )

            if knob_rect.collidepoint(mouse_pos):

                dragging_volume = True

        if event.type == pygame.MOUSEBUTTONUP:

            dragging_volume = False

        if event.type == pygame.MOUSEMOTION:

            if dragging_volume:

                handle_volume(event.pos[0])

    # Background
    screen.fill((25, 25, 30))

    # Spin
    if playing:

        rotation += 1

    draw_title()

    draw_record(rotation)

    draw_buttons()

    draw_volume_slider()

    draw_needle()

    pygame.display.update()

pygame.quit()