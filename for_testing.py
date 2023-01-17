from pygame.math import Vector2

vec = Vector2()
# This updates the cartesian coordinates of vec.
vec.from_polar((90, 90))  # 90 pixels long, rotated 60 degrees.
print(vec)
