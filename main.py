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

with open('test.txt','r') as f:
    data=f.read()
polar=[]
for i in data.split('\n'):
    polar.append((float(i.split()[0]),float(i.split()[1])))
print(polar)

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
iter =0
while True:
    servise_func()

    # svg bezier_raw
    cubic_bezier_sequence[0].draw_bezier(SCREEN)
    cubic_bezier_sequence[0].draw_points(SCREEN, 2)
    screen_rect = SCREEN.get_rect()

    # draw link
    origin = Vector2(screen_rect.center)

    r, phi = (cubic_bezier_sequence[0].linear_decart_array[1] - origin).as_polar()
    disp_vector = Vector2()
    disp_vector.from_polar(polar[0])

    disp_vector = disp_vector.rotate(polar[1][1])
    pygame.draw.line(SCREEN, Color('BLUE'), origin, disp_vector+origin)

    # Render the radius and angle.
    txt = font.render('r: {:.1f}'.format(r), True, Color('RED'))
    SCREEN.blit(txt, (30, 30))
    txt = font.render('phi: {:.1f}'.format(phi), True, Color('RED'))
    SCREEN.blit(txt, (30, 50))

    # service to control fps
    pygame.display.update()
    CLOCK.tick(1)

