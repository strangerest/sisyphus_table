# this module is looking for bezier object in svg file (xml representation)
# element we need called "path"
# additionally we have "xmlns" attribute which defines namespace for all elements including "path"
#  example of "path": <path class="fil0 str0" d="M0.98 3.68c4652.25,1242.55 5742.15,9509.38 9991.86,9991.86"/>
import xml.etree.ElementTree as ET
import pygame
import bezier


def parce_xml(filename, make_nodes_absolute: bool = False) -> list[list]:
    """
    function will return list of lists representing x y coordinates
    of bezier curves. Without any changes.
    Important!!! bezier coordinates are relative to first node
    to make it absolute use make_absolute_flag
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    # parse namespace
    svg_namespace = str(root.tag)
    svg_namespace = '{' + svg_namespace[svg_namespace.find("{") + 1:svg_namespace.find("}")] + '}'
    # get bezier coordinates

    bezier_raw = list()
    for path in root.iter(svg_namespace + 'path'):
        # formatting initial string
        temp_str = path.attrib['d']
        temp_str = temp_str.replace('M', '')
        temp_str = temp_str.replace('c', ' ')
        temp_str = temp_str.replace(',', ' ')
        # writing points to vector
        temp_points = [round(float(x)) for x in temp_str.split()]
        if make_nodes_absolute is True:
            # in svg nodes are relative to the first node
            # we will convert in to absolute value
            for n, value in enumerate(temp_points):
                if (n % 2 == 0) and n > 0:
                    temp_points[n] += temp_points[0]
                elif (n % 2 == 1) and n > 1:
                    temp_points[n] += temp_points[1]
        bezier_raw.append(temp_points)
    return bezier_raw


if __name__ == '__main__':
    print('this is new', parce_xml('Figure.svg', True))


    # old backup

    def parce_xml_old(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        # parse namespace
        svg_namespace = str(root.tag)
        svg_namespace = '{' + svg_namespace[svg_namespace.find("{") + 1:svg_namespace.find("}")] + '}'
        # get bezier coordinates
        for path in root.iter(svg_namespace + 'path'):
            # formatting initial string
            temp_str = path.attrib['d']
            temp_str = temp_str.replace('M', '')
            temp_str = temp_str.replace('c', ' ')
            temp_str = temp_str.replace(',', ' ')
            # writing points to vector
            temp_points = [float(x) for x in temp_str.split()]
            # in svg nodes are relative to the first node
            # we will convert in to absolute value
            for n, value in enumerate(temp_points):
                if (n % 2 == 0) and n > 0:
                    temp_points[n] += temp_points[0]
                elif (n % 2 == 1) and n > 1:
                    temp_points[n] += temp_points[1]

            regular_bezier = list(divide_chunks_2vect(temp_points, 2, 0))
        # print(temp_points)
        return regular_bezier


    def bezier_to_cubic_bezier(regular_bezier):
        """ function shrink any bezier curve to cubic curve by dividing it into 4 points (8 numbered array) """
        # first for nodes is one cubic bezier curve
        # last mode of previous cubic bezier curve is first node of following cubic bezier curve
        cubic_bezier_list = list(divide_chunks(regular_bezier, 3, 1))
        print(cubic_bezier_list)
        for i, value in enumerate(regular_bezier[:len(regular_bezier) - 1:3]):
            cubic_bezier_list[i].insert(0, value)
        print()
        print(cubic_bezier_list)
        my_bezier = bezier.CubicBezier(cubic_bezier_list)
        return my_bezier


    def divide_chunks(l, n, starting_element):
        # looping till length l
        for i in range(starting_element, len(l), n):
            yield l[i:i + n]


    def divide_chunks_2vect(l, n, starting_element):
        for i in range(starting_element, len(l), n):
            yield pygame.math.Vector2(l[i], l[i + 1])
