from pygame.math import Vector2


class BasicParent:
    def __init__(self):
        pass

    @staticmethod
    def return_sum(vec2: Vector2 = Vector2(0, 0), vec1: Vector2 = Vector2(0, 0)):
        return vec1 + vec2


myObj = BasicParent()
print(Vector2(10, 20) + Vector2(30, 40))
print(myObj.return_sum(Vector2(10, 20), Vector2(30, 40)))
