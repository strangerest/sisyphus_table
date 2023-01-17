import sys, pygame
import numpy as np
from pygame.locals import *
import pygame.gfxdraw
import svg_parser, bezier

# preparation
my_bezier_raw = svg_parser.parce_xml('Figure.svg', True)  # array of bezies
general_bezier = bezier.RegularBezier.from_array(my_bezier_raw[0])
cubic_bezier_sequence = general_bezier.to_cubic_bezier()

for i in cubic_bezier_sequence:
    i.to_linear_decart(5)

# constants
SCREEN_SIZE = (800, 800)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
main_surface = pygame.Surface(SCREEN_SIZE)
rotation_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
CLOCK = pygame.time.Clock()
pygame.init()


# rotation experiment
surface = pygame.Surface((50, 50), pygame.SRCALPHA)
surface.fill((0, 0, 0))
rotated_surface = surface
rect = surface.get_rect()
angle = 10


def servise_func():
    # quit service
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # colors
    SCREEN.fill('aliceblue')
    main_surface.fill('aliceblue')

def center_origin(surf, p):
    return (p[0] + surf.get_width() // 2, p[1] + surf.get_height() // 2)

while True:
    servise_func()

    cubic_bezier_sequence[0].draw_bezier(main_surface)
    cubic_bezier_sequence[0].draw_points(main_surface,2)
    SCREEN.blit(main_surface, (200, 200))

    test_vector = pygame.math.Vector2(200, 0)
    pygame.draw.line(main_surface,Color('RED'),(0,0),(test_vector.x,test_vector.y),3)
    test_vector = test_vector.rotate(-45)   
    print(test_vector.x,test_vector.y)
    pygame.draw.line(main_surface,Color('RED'),(0,0),(-10,-10),3)

    pygame.draw.line(rotation_surface, Color('RED'),(0,0),(300,0),3)


    # rotation experiment
    # rotated_surface = pygame.transform.rotate(surface, angle)
    # rect = rotated_surface.get_rect(center=(100, 100))
    # # draw service
    # # SCREEN.blit(main_surface, (0, 0))
    # # SCREEN.blit(rotated_surface, (rect.x, rect.y))
    # myRect = pygame.Rect(0, 0, 200, 200)
    # myRect.center = (0, 0)
    # pygame.draw.rect(main_surface, Color('RED'), myRect)
    # SCREEN.blit(main_surface, center_origin(main_surface,(0, 0)))
    # SCREEN.blit(main_surface, (0,0))

    # service to control fps
    pygame.display.update()
    CLOCK.tick(60)


# old backup

def bezier_lerp(self, t, cubic_bezie):
    t2 = t * t
    t3 = t2 * t
    mt = 1 - t
    mt2 = mt * mt
    mt3 = mt2 * mt
    x_coordinate = cubic_bezie[0].x * mt3 + 3 * cubic_bezie[1].x * mt2 * t + 3 * cubic_bezie[2].x * mt * t2 + \
                   cubic_bezie[3].x * t3
    y_coordinate = cubic_bezie[0].y * mt3 + 3 * cubic_bezie[1].y * mt2 * t + 3 * cubic_bezie[2].y * mt * t2 + \
                   cubic_bezie[3].y * t3
    return pygame.math.Vector2(x_coordinate, y_coordinate)


def bezier_to_linear_decart(cubic_bezier_curve, descretisation_step):
    # bezier_to_3d_order_bezier(bezier_curve)
    linear_path = []
    for i in np.arange(0.0, 1.0, 1.0 / descretisation_step):
        linear_path.append(bezier_lerp(i, cubic_bezier_curve))
    return linear_path
