# this module is looking for bezier_raw object in svg file (xml representation)
# element we need called "path"
# additionally we have "xmlns" attribute which defines namespace for all elements including "path"
#  example of "path": <path class="fil0 str0" d="M0.98 3.68c4652.25,1242.55 5742.15,9509.38 9991.86,9991.86"/>
import xml.etree.ElementTree as ET


def parce_xml(filename, make_nodes_absolute: bool = False, round_to: int = 0) -> list[list]:
    """
    function will return list of lists representing x y coordinates
    of bezier_raw curves, rounding it (whole number by default)
    Important!!! bezier_raw coordinates are relative to first node
    to make it absolute use make_absolute_flag
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    # parse namespace
    svg_namespace = str(root.tag)
    svg_namespace = '{' + svg_namespace[svg_namespace.find("{") + 1:svg_namespace.find("}")] + '}'
    # get bezier_raw coordinates

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
            for n, value in enumerate(temp_points):
                if (n % 2 == 0) and n > 0:
                    temp_points[n] += temp_points[0]
                elif (n % 2 == 1) and n > 1:
                    temp_points[n] += temp_points[1]
        bezier_raw.append(temp_points)
    return bezier_raw


if __name__ == '__main__':
    print('this is new svg beziers:')
    for i in parce_xml('Figure.svg',True):
        print('beaier coordinates ', i)
