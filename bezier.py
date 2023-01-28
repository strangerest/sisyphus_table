import pygame
from pygame.math import Vector2
from pygame.locals import *
import numpy as np


# TODO: add even distribution of points on regular_bezier_raw curve while linearization
# TODO: add adaptive linearization according to length of regular_bezier_raw curve

# TODO: inheritance research to separate math/draw/service function from regular bezier and cubic bezier
class CubicBezier:
    """
    class contains 4 control nodes (pygame.math.Vector2) stored in .regular_bezier_raw array
    to create object use classmethod .from_vector or .from_array
    to access interpolated regular_bezier_raw curve version call to_linear_decart method.
    the result will be stored in linear_decart_array and returned as well
    """
    # public variables
    bezier_raw = []
    linear_decart_array = []
    polar_array = list()

    # init functions
    def __init__(self, four_node_vector_array: list[Vector2],
                 create_linear_interpolation: bool = False, discrete_step: int = 10):
        """"
        appropriate way to use constructor is through classmethods below: .from_vector and .from_array
        :param four_node_vector_array: regular_bezier_raw curve control points in decart coordinates (up-left conner)
        :param create_linear_interpolation: fill linear_decart_array with Vector2() points
        :param discrete_step: nuber of line segments
        """
        self.bezier_raw = four_node_vector_array
        # self.linear_decart_array = []

        if create_linear_interpolation:
            self.to_linear_decart(discrete_step)

    @classmethod
    def from_vector(cls, four_node_vector_array: list[Vector2],
                    create_linear_interpolation: bool = False, discrete_step: int = 10):
        """
        Checks if data is valid and call constructor if user provide list of 4 pygame vector2 objects
        :param four_node_vector_array:
        :param create_linear_interpolation:
        :param discrete_step:
        :return:
        """
        if len(four_node_vector_array) == 4 and isinstance(four_node_vector_array[0], pygame.math.Vector2):
            return cls(four_node_vector_array, create_linear_interpolation, discrete_step)
        else:
            raise Exception("Cubic regular_bezier_raw defines by array of 4 pygame.math.Vector2")

    @classmethod
    def from_array(cls, eight_number_array: list[float, int]):
        """
        Checks if data is valid and call constructor if user provide list of 8 floats
        :param eight_number_array:
        :return:
        """
        if len(eight_number_array) == 8:
            regular_bezier = list(cls.divide_chunks_2vect(eight_number_array, 2, 0))
            return cls(regular_bezier)
        else:
            raise Exception("Cubic regular_bezier_raw defines by array of 8 float/int numbers")

    def __repr__(self):
        return '<Cubic_bezier{}>'.format(len(self.bezier_raw))

    # math calculation functions
    def lerp(self, t):
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        x_coordinate = self.bezier_raw[0].x * mt3 + 3 * self.bezier_raw[1].x * mt2 * t + 3 * self.bezier_raw[
            2].x * mt * t2 + self.bezier_raw[3].x * t3
        y_coordinate = self.bezier_raw[0].y * mt3 + 3 * self.bezier_raw[1].y * mt2 * t + 3 * self.bezier_raw[
            2].y * mt * t2 + self.bezier_raw[3].y * t3
        return pygame.math.Vector2(x_coordinate, y_coordinate)

    def to_linear_decart(self, discrete_step: int = 10):
        t = 1.0 / discrete_step
        linear_path = []
        for i in np.arange(0.0, 1.0, t):
            linear_path.append(self.lerp(i))
        linear_path.append(self.lerp(1))
        self.linear_decart_array = linear_path
        return self.linear_decart_array

    def to_polar_coord(self, origin: pygame.math.Vector2 = pygame.math.Vector2(0, 0)):
        """
        function returns a list of tuples (r, phi) of polar coordinates
        origin should be a Vector2 in same decart coordinate system
        """
        if len(self.linear_decart_array) == 0:
            self.to_linear_decart(20)

        for i in self.linear_decart_array:
            r_phi = (i - origin).as_polar()
            self.polar_array.append(r_phi)
        return self.polar_array

    # drawing functions
    def draw_points(self, surface: pygame.Surface, radius: int = 2):
        for i in self.linear_decart_array:
            pygame.draw.circle(surface, Color('red'), i, radius)

    def draw_bezier(self, surface: pygame.Surface):
        pygame.gfxdraw.bezier(surface, self.bezier_raw, 10, Color('red'))

    # service functions
    @staticmethod
    def divide_chunks_2vect(divided_list, n, starting_element):
        for i in range(starting_element, len(divided_list), n):
            yield pygame.math.Vector2(divided_list[i], divided_list[i + 1])


class RegularBezier:
    # public variables
    cubic_bezier_list = list()  # list of cubic_bezier class objects made from regular bezier division
    regular_bezier_raw = list()  # list of vector2 objects represent nodes of regular bezier
    linear_decart_array = list()

    # init functions
    def __init__(self, vector_array: list[Vector2]):
        """
        appropriate way to use constructor is through classmethods below: .from_vector and .from_array
        :param vector_array:
        """
        self.regular_bezier_raw = vector_array

    @classmethod
    def from_vector(cls, vector_array: list[Vector2]):
        if (len(vector_array) - 4) % 3 == 0 and isinstance(vector_array[0], pygame.math.Vector2):
            return cls(vector_array)
        else:
            raise Exception(
                "Regular regular_bezier_raw defines by array of pygame.math.Vector2"
                " It could contain 4 7 10 13 16 and so ode nodes")

    @classmethod
    def from_array(cls, regular_number_array: list[float, int]):

        if (len(regular_number_array) - 8) % 3 == 0:
            regular_bezier = list(cls.divide_chunks_2vect(regular_number_array, 2, 0))
            return cls(regular_bezier)
        else:
            raise Exception("Cubic regular_bezier_raw defines by array of 8 float/int numbers")

    def __repr__(self):
        return '<Regular_bezier{}>'.format(len(self.regular_bezier_raw))

    # transform functions
    def to_cubic_bezier(self):

        # first 4 nodes is one cubic regular_bezier_raw curve
        # last node of previous cubic regular_bezier_raw curve is first node of following cubic regular_bezier_raw curve
        self.cubic_bezier_list = list()
        list_for_cubic_bezier = list(self.divide_chunks(self.regular_bezier_raw, 3, 1))
        for i, value in enumerate(self.regular_bezier_raw[:len(self.regular_bezier_raw) - 1:3]):
            list_for_cubic_bezier[i].insert(0, value)
        for i in list_for_cubic_bezier:
            self.cubic_bezier_list.append(CubicBezier.from_vector(i))
        return self.cubic_bezier_list

    def to_linear_decart(self, discrete_step: int = 10):
        """
        if we convert regular regular_bezier_raw curve to cubic regular_bezier_raw list
        we could do .to_linear_decart method to each of this curves and concatenate linear points to one big list
        :param discrete_step:
        :return:
        """

        if not self.cubic_bezier_list:
            self.to_cubic_bezier()

        for i in self.cubic_bezier_list:
            self.linear_decart_array.extend(i.to_linear_decart(discrete_step))
            self.linear_decart_array.pop()
        self.linear_decart_array.append(self.cubic_bezier_list[-1].to_linear_decart(discrete_step)[-1])
        return self.linear_decart_array

    def to_polar_coord(self, origin: pygame.math.Vector2 = pygame.math.Vector2(0, 0)):
        if not self.linear_decart_array:
            self.to_linear_decart()
        for i in self.linear_decart_array:
            pass

    # service functions
    @staticmethod
    def divide_chunks_2vect(divided_list, n, starting_element):
        for i in range(starting_element, len(divided_list), n):
            yield pygame.math.Vector2(divided_list[i], divided_list[i + 1])

    @staticmethod
    def divide_chunks(divided_list, n, starting_element):
        # looping till length l
        for i in range(starting_element, len(divided_list), n):
            yield divided_list[i:i + n]


# testing block
if __name__ == "__main__":
    Vector = pygame.math.Vector2
    cubic_bezier = CubicBezier.from_vector([Vector(1, 2), Vector(3, 4), Vector(5, 6), Vector(7, 8)], True)
    print(cubic_bezier.bezier_raw)
    print(cubic_bezier.linear_decart_array)
    print('......')
    test = RegularBezier.from_array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    print('Regular:', test)
    test.to_cubic_bezier()
    print(test.to_linear_decart())
