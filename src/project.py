import pygame
import math

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Vinyl Record Player")

clock = pygame.time.Clock()

rotation = 0

def draw_record(angle):

    record_surface = pygame.Surface((400, 400), pygame.SRCALPHA)

    center = (200, 200)

    # Main record
    pygame.draw.circle(record_surface, (10, 10, 10), center, 180)

    # Record grooves
    for radius in range(80, 180, 8):
        pygame.draw.circle(record_surface, (40, 40, 40), center, radius, 1)

    # Center label
    pygame.draw.circle(record_surface, (200, 50, 50), center, 50)

    # Rotate record
    rotated = pygame.transform.rotate(record_surface, angle)

    rect = rotated.get_rect(center=(500, 350))

    screen.blit(rotated, rect)

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((25, 25, 30))

    rotation += 1

    draw_record(rotation)

    pygame.display.update()

pygame.quit()