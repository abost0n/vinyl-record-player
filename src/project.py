import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Vinyl Record Player")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 20))

    pygame.display.update()

pygame.quit()