"""
module for working with polar gcode.
could write formatted gcode to txt from  array of tuples
could convert absolute polar coordinates to relative shift
"""

# TODO: fix "z" at the end problem
def write_polar_gcode_to_txt(filename: str, gcode_array: list[tuple], make_relative=False):
    """
    main problem with polar coordinates - brake gap between 180 deg and -180 deg
    so, we could solve this problem in converting to relative coordinates
    by checking angular distance between 2 neighbour points with is Workaround for now
    in relative coordinates, positive value represents clockwise direction movement
    and negative - counter-clockwise direction movement. If value is zero - no move.
    :param filename: output file name where gcode will be writen
    :param gcode_array: list of polar coordinates(2-dimensional tuples) to write to file
    :param make_relative: flag for shift mode
    :return: None
    """
    if make_relative:
        with open(filename, 'w+') as f:
            for i, value in enumerate(gcode_array):
                r = gcode_array[i][0] - gcode_array[i - 1][0]
                phi = gcode_array[i][1] - gcode_array[i - 1][1]

                if i == 0:
                    f.write(str(round(value[0])) + ' ' + str(round(value[1])))
                else:
                    if abs(phi) > 180:
                        if phi < 0:  # clockwise direction
                            phi = 360 - abs(phi)
                        else:
                            phi = -(360 - abs(phi))
                    f.write('\n'+str(round(r, 2)) + ' ' + str(round(phi, 2))) # stupid WA to avoid blank line at the end
    else:
        with open(filename, 'w+') as f:
            for i in gcode_array:
                f.write(str(round(i[0], 2)) + ' ' + str(round(i[1], 2)) + '\n')


if __name__ == '__main__':
    import svg_parser
    from bezier import RegularBezier, CubicBezier
    from pygame.math import Vector2
    discretization_step = 20 # higher step - more accurate path

    my_bezier_raw = svg_parser.parce_xml('star.svg', True)  # array of bezies
    general_bezier = RegularBezier.from_array(my_bezier_raw[0])
    general_bezier.to_polar_coord(Vector2(75,75))
    print(general_bezier.polar_array)

    write_polar_gcode_to_txt("test.txt",general_bezier.polar_array, True)
