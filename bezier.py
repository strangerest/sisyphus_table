import pygame
from pygame.locals import *
import numpy as np


class CubicBezier:
    """
    cubic_bezier contains 4 control nodes (pygame.math.Vector2) stored in .bezier array
    to create object use classmethod from_vector or from_array
    to access interpolated bezier curve version call to_linear_decart method.
    the result will be stored in linear_decart_array and returned as well
    """

    # init functions
    @classmethod
    def from_vector(cls, four_node_vector_array: list[pygame.math.Vector2]):
        if len(four_node_vector_array) == 4 and isinstance(four_node_vector_array[0], pygame.math.Vector2):
            return cls(four_node_vector_array)
        else:
            raise Exception("Cubic bezier defines by array of 4 pygame.math.Vector2")

    @classmethod
    def from_array(cls, eight_number_array: list[float, int]):

        if len(eight_number_array) == 8:
            regular_bezier = list(cls.divide_chunks_2vect(eight_number_array, 2, 0))
            return cls(regular_bezier)
        else:
            raise Exception("Cubic bezier defines by array of 8 float/int numbers")

    def __init__(self, four_node_vector_array):
        self.bezier = four_node_vector_array

    def __repr__(self):
        return '<Cubic_bezier{}>'.format(len(self.bezier))

    # math calculation functions
    def lerp(self, t):
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        x_coordinate = self.bezier[0].x * mt3 + 3 * self.bezier[1].x * mt2 * t + 3 * self.bezier[2].x * mt * t2 + \
                       self.bezier[3].x * t3
        y_coordinate = self.bezier[0].y * mt3 + 3 * self.bezier[1].y * mt2 * t + 3 * self.bezier[2].y * mt * t2 + \
                       self.bezier[3].y * t3
        return pygame.math.Vector2(x_coordinate, y_coordinate)

    def to_linear_decart(self, discret_step):
        t = 1.0 / discret_step
        linear_path = []
        for i in np.arange(0.0, 1.0, t):
            linear_path.append(self.lerp(i))
        linear_path.append(self.lerp(1))
        self.linear_decart_array = linear_path
        return linear_path

    # drawing functions
    def draw_points(self, surface: pygame.Surface, radius):
        for i in self.linear_decart_array:
            pygame.draw.circle(surface, Color('red'), i, radius)

    def draw_bezier(self, surface: pygame.Surface):
        pygame.gfxdraw.bezier(surface, self.bezier, 10, Color('red'))

    # service functions
    @staticmethod
    def divide_chunks_2vect(devided_list, n, starting_element):
        for i in range(starting_element, len(devided_list), n):
            yield pygame.math.Vector2(devided_list[i], devided_list[i + 1])


class RegularBezier():
    # init functions
    @classmethod
    def from_vector(cls, vector_array: list[pygame.math.Vector2]):
        if (len(vector_array) - 4) % 3 == 0 and isinstance(vector_array[0], pygame.math.Vector2):
            return cls(vector_array)
        else:
            raise Exception(
                "Regular bezier defines by array of pygame.math.Vector2 It could contain 4 7 10 13 16 and so ode nodes")

    @classmethod
    def from_array(cls, regular_number_array: list[float, int]):

        if (len(regular_number_array) - 8) % 3 == 0:
            regular_bezier = list(cls.divide_chunks_2vect(regular_number_array, 2, 0))
            return cls(regular_bezier)
        else:
            raise Exception("Cubic bezier defines by array of 8 float/int numbers")

    def __init__(self, vector_array):
        self.bezier = vector_array

    def __repr__(self):
        return '<Regular_bezier{}>'.format(len(self.bezier))

    # transform functions
    def to_cubic_bezier(self):
        # first for nodes is one cubic bezier curve
        # last mode of previous cubic bezier curve is first
        # node of following cubic bezier curve
        cubic_bezier_list = list()
        list_for_cubic_bezier = list(self.divide_chunks(self.bezier, 3, 1))
        for i, value in enumerate(self.bezier[:len(self.bezier) - 1:3]):
            list_for_cubic_bezier[i].insert(0, value)
        for i in list_for_cubic_bezier:
            cubic_bezier_list.append(CubicBezier.from_vector(i))
        return cubic_bezier_list

    # service functions
    @staticmethod
    def divide_chunks_2vect(devided_list, n, starting_element):
        for i in range(starting_element, len(devided_list), n):
            yield pygame.math.Vector2(devided_list[i], devided_list[i + 1])

    @staticmethod
    def divide_chunks(devided_list, n, starting_element):
        # looping till length l
        for i in range(starting_element, len(devided_list), n):
            yield devided_list[i:i + n]


# testing block
if __name__ == "__main__":
    test = RegularBezier.from_array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    print('Regular:', test)
    print(test.to_cubic_bezier())
    # print('regular', test.bezier)
    # print(test.to_cubic_bezier())
