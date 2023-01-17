def write_polar_gcode_to_txt(filename: str, gcode_array: list[tuple]):
    with open(filename, 'w+') as f:
        for i in gcode_array:
            f.write(str(round(i[0],2))+' '+str(round(i[1],2))+'\n')
