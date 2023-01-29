# this module is looking for regular_bezier_raw object in svg file (xml representation)
# element we need called "path"
# additionally we have "xmlns" attribute which defines namespace for all elements including "path"
#  example of "path": <path class="fil0 str0" d="M0.98 3.68c4652.25,1242.55 5742.15,9509.38 9991.86,9991.86"/>
import xml.etree.ElementTree as ET

def parce_xml(filename, make_nodes_absolute: bool = False, round_to: int = 0) -> list[list]:
    """
    some things you need to know about bezier svg representation: bezier is made of nodes.
    The most useful type of bezier is cubic one (it has 4 nodes: 2 for the ends and 2 controls)
    In svg bezier object is placed in path element, which is a set of nodes (4, 7, 10, 13 etc)
    each node is shared between two neighbour cubic curves (4th 7th 10th 13th etc).
    svg curve coordinates are relative to first node (started from M (moveto) command)
    additionally coordinates of cubic bezier are relative to shared node
    so svg bezier basically set of cubic beziers, end of each is the start of relative coordinates of following cubic bezier

    :param filename: file you want to parce
    :param make_nodes_absolute: read description, if flag is False it is simple strin2array function
    :param round_to: precision parameter, expect nuber of digits after point
    :return: each list is one parsed "path" object representing x y coordinates without any grouping
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    # parse namespace
    svg_namespace = str(root.tag)
    svg_namespace = '{' + svg_namespace[svg_namespace.find("{") + 1:svg_namespace.find("}")] + '}'
    # get regular_bezier_raw coordinates

    bezier_raw = list()
    for path in root.iter(svg_namespace + 'path'):
        # formatting initial string
        temp_str = path.attrib['d']
        temp_str = temp_str.replace('M', '')
        temp_str = temp_str.replace('c', ' ')
        temp_str = temp_str.replace(',', ' ')
        # writing points to vector
        temp_points = [round(float(x), 0) for x in temp_str.split()]
        if make_nodes_absolute is True:
            # in svg nodes are relative to the first node
            # we will convert in to absolute value

            for i in range(0,len(temp_points)-6,6):

                temp_points[i+2] += temp_points[i]
                temp_points[i+4] += temp_points[i]
                temp_points[i+6] += temp_points[i]

                temp_points[i+3] += temp_points[i+1]
                temp_points[i+5] += temp_points[i+1]
                temp_points[i+7] += temp_points[i+1]

            # for n, value in enumerate(temp_points):
            #     if (n % 2 == 0) and n > 0:
            #         temp_points[n] += temp_points[0]
            #     elif (n % 2 == 1) and n > 1:
            #         temp_points[n] += temp_points[1] # y coordinates are inverted but pygame do it under the hood


        bezier_raw.append(temp_points)
    return bezier_raw


if __name__ == '__main__':
    def divide_chunks(divided_list, n, starting_element):
        # looping till length l
        for i in range(starting_element, len(divided_list), n):
            yield divided_list[i:i + n]


    raw_svg = parce_xml('star.svg', True)
    svg_array = list(divide_chunks(raw_svg[0], 2, 0))

    print(svg_array)

    with open('parsed_svg.txt', 'w') as f:
        for i in svg_array:
            f.write(str(round(i[0], 2)) + ' ' + str(round(i[1], 2)) + '\n')

