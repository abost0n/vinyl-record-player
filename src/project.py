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
PINK = (255, 105, 180)

# VARIABLES
rotation = 0
playing = False
music_loaded = False
album_loaded = False
volume = 0.5

needle_angle = -40

# SCRATCH FEATURE VARIABLES
dragging_record = False
last_mouse_angle = 0

album_cover_surface = None

record_center = (600, 350)

# TKINTER FILE PICKER
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

# BUTTONS
play_button = pygame.Rect(100, 680, 140, 50)
upload_music_button = pygame.Rect(280, 680, 220, 50)
upload_cover_button = pygame.Rect(540, 680, 220, 50)

# VOLUME SLIDER
slider_rect = pygame.Rect(900, 700, 200, 10)
slider_x = 900 + int(volume * 200)


# -----------------------
# LOAD MUSIC
# -----------------------
def load_music():
    global music_loaded

    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )

    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        music_loaded = True


# -----------------------
# LOAD IMAGE
# -----------------------
def load_album_cover():
    global album_cover_surface, album_loaded

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:
        image = Image.open(file_path)
        image = image.resize((260, 260))
        image = image.convert("RGBA")

        album_cover_surface = pygame.image.fromstring(
            image.tobytes(),
            image.size,
            image.mode
        )

        album_loaded = True


# -----------------------
# SCRATCH HELPERS
# -----------------------
def get_mouse_angle(mouse_pos):
    dx = mouse_pos[0] - record_center[0]
    dy = mouse_pos[1] - record_center[1]
    return math.degrees(math.atan2(dy, dx))


def is_on_record(mouse_pos):
    dx = mouse_pos[0] - record_center[0]
    dy = mouse_pos[1] - record_center[1]
    return math.sqrt(dx*dx + dy*dy) < 230


# -----------------------
# DRAW RECORD
# -----------------------
def draw_record(angle):

    record_surface = pygame.Surface((500, 500), pygame.SRCALPHA)
    center = (250, 250)

    pygame.draw.circle(record_surface, BLACK, center, 230)

    for radius in range(70, 230, 10):
        pygame.draw.circle(record_surface, (40, 40, 40), center, radius, 1)

    pygame.draw.circle(record_surface, RED, center, 70)

    if album_loaded and album_cover_surface:
        rect = album_cover_surface.get_rect(center=center)
        record_surface.blit(album_cover_surface, rect)

    rotated = pygame.transform.rotate(record_surface, angle)
    rect = rotated.get_rect(center=record_center)
    screen.blit(rotated, rect)


# -----------------------
# BUTTONS
# -----------------------
def draw_buttons():
    font = pygame.font.SysFont("Arial", 28)

    pygame.draw.rect(screen, PINK if playing else GRAY, play_button, border_radius=10)
    pygame.draw.rect(screen, GRAY, upload_music_button, border_radius=10)
    pygame.draw.rect(screen, GRAY, upload_cover_button, border_radius=10)

    play_text = font.render("Pause" if playing else "Play", True, BLACK)
    music_text = font.render("Upload Music", True, BLACK)
    cover_text = font.render("Upload Cover", True, BLACK)

    screen.blit(play_text, (135, 690))
    screen.blit(music_text, (315, 690))
    screen.blit(cover_text, (575, 690))


# -----------------------
# VOLUME
# -----------------------
def draw_volume_slider():
    pygame.draw.rect(screen, WHITE, slider_rect)
    pygame.draw.circle(screen, RED, (slider_x, 705), 12)

    font = pygame.font.SysFont("Arial", 24)
    text = font.render("Volume", True, WHITE)
    screen.blit(text, (900, 660))


def handle_volume(mouse_x):
    global slider_x, volume

    slider_x = max(900, min(mouse_x, 1100))
    volume = (slider_x - 900) / 200
    pygame.mixer.music.set_volume(volume)


# -----------------------
# NEEDLE
# -----------------------
def draw_needle():
    global needle_angle

    base_x = 930
    base_y = 180
    length = 220

    target_angle = -15 if playing else -40
    needle_angle += (target_angle - needle_angle) * 0.05

    end_x = base_x + math.cos(math.radians(needle_angle)) * length
    end_y = base_y - math.sin(math.radians(needle_angle)) * length

    pygame.draw.line(screen, WHITE, (base_x, base_y), (end_x, end_y), 8)
    pygame.draw.circle(screen, WHITE, (base_x, base_y), 15)


# -----------------------
# TITLE
# -----------------------
def draw_title():
    font = pygame.font.SysFont("Arial", 42, bold=True)
    text = font.render("Interactive Vinyl Record Player", True, WHITE)
    screen.blit(text, (320, 40))


# -----------------------
# MAIN LOOP
# -----------------------
running = True
dragging_volume = False

while running:

    clock.tick(60)
    screen.fill((25, 25, 30))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if play_button.collidepoint(mouse):
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

            if upload_music_button.collidepoint(mouse):
                load_music()

            if upload_cover_button.collidepoint(mouse):
                load_album_cover()

            knob_rect = pygame.Rect(slider_x - 12, 693, 24, 24)
            if knob_rect.collidepoint(mouse):
                dragging_volume = True

            if is_on_record(mouse):
                dragging_record = True
                last_mouse_angle = get_mouse_angle(mouse)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_volume = False
            dragging_record = False

        if event.type == pygame.MOUSEMOTION:

            if dragging_volume:
                handle_volume(event.pos[0])

            if dragging_record:
                current_angle = get_mouse_angle(event.pos)
                delta = current_angle - last_mouse_angle
                rotation += delta * 2
                last_mouse_angle = current_angle

    if playing:
        rotation += 1

    draw_title()
    draw_record(rotation)
    draw_buttons()
    draw_volume_slider()
    draw_needle()

    pygame.display.update()

pygame.quit()