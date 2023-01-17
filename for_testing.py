from math import atan2, degrees, pi
import pygame

test_vector = pygame.math.Vector2(10,0)
test_vector.rotate(45)

x1=0
x2=10
y1 =0
y2 =20

dx = x2 - x1
dy = y2 - y1
rads = atan2(-dy,dx)
rads %= 2*pi
degs = degrees(rads)
print(degs)

def get_distance