from pygame.math import Vector2

vec = Vector2()
# This updates the cartesian coordinates of vec.
vec.from_polar((90, 90))  # 90 pixels long, rotated 60 degrees.
print(vec)


def test_func():
    return 10,20
a,b=test_func()
print(b)