import sys, pygame
from pygame.math import Vector2
from pygame.locals import *
import pygame.gfxdraw
import svg_parser, bezier

# preparation
my_bezier_raw = svg_parser.parce_xml('Figure.svg', True)  # array of bezies
general_bezier = bezier.RegularBezier.from_array(my_bezier_raw[0])
cubic_bezier_sequence = general_bezier.to_cubic_bezier()

for i in cubic_bezier_sequence:
    i.to_linear_decart(20)


# constants
SCREEN_SIZE = [800, 800]
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
pygame.init()
font = pygame.font.Font(None, 30)


def servise_func():
    # quit service
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # colors
    SCREEN.fill('aliceblue')


angle = 0
while True:
    servise_func()

    # svg bezier
    cubic_bezier_sequence[0].draw_bezier(SCREEN)
    cubic_bezier_sequence[0].draw_points(SCREEN, 2)
    screen_rect = SCREEN.get_rect()

    # draw link
    origin = Vector2(screen_rect.center)

    r, phi = (cubic_bezier_sequence[0].linear_decart_array[1] - origin).as_polar()

    pygame.draw.line(SCREEN, Color('BLUE'), origin, cubic_bezier_sequence[0].linear_decart_array[1])

    # Render the radius and angle.
    txt = font.render('r: {:.1f}'.format(r), True, Color('RED'))
    SCREEN.blit(txt, (30, 30))
    txt = font.render('phi: {:.1f}'.format(phi), True, Color('RED'))
    SCREEN.blit(txt, (30, 50))

    # service to control fps
    pygame.display.update()
    CLOCK.tick(60)
