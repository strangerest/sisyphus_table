import sys, pygame
from pygame.math import Vector2
from pygame.locals import *
import pygame.gfxdraw
import svg_parser
from bezier import RegularBezier, CubicBezier

# preparation
pygame.init()

def bezier_from_file(filename:str):
    data=list()
    with open(filename, 'r') as f:
        for i in f:
            data.append(Vector2([float(x) for x in i.split()]))
    return data


def quit_event_hendler(display_surface: pygame.surface):
    # quit service
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def display_ruler(display_surface: pygame.surface, origin: Vector2, font=pygame.font.Font(None, 30)):
    # Render the radius and angle (mouse is used as a ruler)
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.circle(display_surface, Color('BLUE'), origin, 5)
    pygame.draw.line(display_surface, Color('BLUE'), origin, mouse_pos, 3)

    r, phi = (mouse_pos - origin).as_polar()
    txt = font.render('r: {:.1f}'.format(r), True, Color('RED'))
    display_surface.blit(txt, (30, 30))
    txt = font.render('phi: {:.1f}'.format(phi), True, Color('RED'))
    display_surface.blit(txt, (30, 50))

def main():
    # constants for display

    SCREEN_SIZE = [800, 800]
    SCREEN_SENTER = Vector2(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    CLOCK = pygame.time.Clock()

    my_regular_bezier = RegularBezier.from_array(svg_parser.parce_xml('star.svg', True)[0],
                                                 True,10, True, Vector2(400,400))  # # array of bezies
    while True:
        quit_event_hendler(SCREEN)
        SCREEN.fill('aliceblue')

        my_regular_bezier.draw_bezier(SCREEN)
        my_regular_bezier.draw_points(SCREEN)

        display_ruler(SCREEN, SCREEN_SENTER)
        # service to control fps
        pygame.display.update()
        CLOCK.tick(60)


if __name__ == '__main__':
    main()
