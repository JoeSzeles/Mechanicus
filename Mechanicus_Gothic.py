from datetime import datetime as dt
import importlib
import config3
import time
# Modify these variables as needed
Z_line_start = 5.0  # Initial Z position when a line starts
Z_line_center = 2.0  # Z position in the middle of a line
Z_line_end = 0.0  # Z position at the end of a line
Z_line_speed = 400.0  # Initial feed rate for Z movement

# Other existing variables
feed_rate = 100.0  # Default feed rate for XY movement
draw_speed = 100.0  # Default feed rate for drawing
zDraw = 1.0  # Z position for drawing
zTravel = 5.0  # Z position for non-drawing travel
zLift = 10.0  # Z position for lifting the tool

def g_string(x, y, z=False, prefix="G1", p=3, feed_rate=None):
    if z is not False:
        if feed_rate is not None:
            return f"{prefix} X{format(x, '.'+str(p)+'f')} Y{format(y, '.'+str(p)+'f')} Z{format(z, '.'+str(p)+'f')} F{feed_rate:.2f}"
        else:
            return f"{prefix} X{format(x, '.'+str(p)+'f')} Y{format(y, '.'+str(p)+'f')} Z{format(z, '.'+str(p)+'f')}"
    else:
        if feed_rate is not None:
            return f"{prefix} X{format(x, '.'+str(p)+'f')} Y{format(y, '.'+str(p)+'f')} F{feed_rate:.2f}"
        else:
            return f"{prefix} X{format(x, '.'+str(p)+'f')} Y{format(y, '.'+str(p)+'f')}"

def shapes_2_gcode(shapes):
    t1 = dt.now()
    with open("header.txt") as h:
        header = h.read()
    commands = [f"{header}", f'F{feed_rate}']
    commands.append(shape_preamble)
    for i, shape in enumerate(shapes):
        start = shape[0]
        end = shape[-1]
        if i < len(shapes) - 1:
            next_start = shapes[i+1][0]
            if end == next_start:
                for j in shape:
                    z_progress = (j[2] - Z_line_start) / (Z_line_end - Z_line_start)
                    current_z = Z_line_start + z_progress * (Z_line_center - Z_line_start)
                    feed_rate = 100 + (1 - z_progress) * (Z_line_speed - 100)  # Adjust the formula as needed
                    commands.append(g_string(j[0], j[1], current_z, f'G1', draw_speed, feed_rate=feed_rate))
            else:
                commands.append(g_string(start[0], start[1], Z_line_start, "G0"))
                for j in shape:
                    z_progress = (j[2] - Z_line_start) / (Z_line_end - Z_line_start)
                    current_z = Z_line_start + z_progress * (Z_line_center - Z_line_start)
                    feed_rate = 100 + (1 - z_progress) * (Z_line_speed - 100)  # Adjust the formula as needed
                    commands.append(g_string(j[0], j[1], current_z, f'G1', draw_speed, feed_rate=feed_rate))
                commands.append(g_string(end[0], end[1], Z_line_end, "G0"))
        else:
            commands.append(g_string(start[0], start[1], Z_line_start, "G0"))
            for j in shape:
                z_progress = (j[2] - Z_line_start) / (Z_line_end - Z_line_start)
                current_z = Z_line_start + z_progress * (Z_line_center - Z_line_start)
                feed_rate = 100 + (1 - z_progress) * (Z_line_speed - 100)  # Adjust the formula as needed
                commands.append(g_string(j[0], j[1], current_z, f'G1', draw_speed, feed_rate=feed_rate))
            commands.append(g_string(end[0], end[1], Z_line_end, "G0"))
            
    commands += ["(home)", f"G0 Z{Z_line_start}", f"G0 X0 Y0"]

    timer(t1, "shapes_2_gcode   ")
    importlib.reload(config3)
    return commands

# Rest of your code here

def generate_gcode(svg_path, gcode_path):
    shapes = get_shapes(svg_path, scale_factor=scaleF, offset_x=0, offset_y=0)

    if optimise:
        pre_distance = get_total_distance(shapes)

        print("unoptimized distance: ", get_total_distance(shapes))

        new_order = optimise_path(shapes)

        post_distance = get_total_distance(new_order)

        print("optimized distance: ", post_distance)
        print("factor: ", post_distance / pre_distance)

        commands = shapes_2_gcode(new_order)
    else:
        commands = shapes_2_gcode(shapes)

    with open(gcode_path, 'w+') as output:
        for command in commands:
            output.write(command + "\n")

    print(f"G-Code generated and saved to {gcode_path}")

def write_file(output, commands):
    
    t1 = dt.now()
    with open(output, 'w+') as output_file:
        for i in commands:
            output_file.write(i + "\n")
    timer(t1, "writing file     ")
