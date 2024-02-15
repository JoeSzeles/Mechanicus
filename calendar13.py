import math
import svgwrite
import calendar

def polar_to_cartesian(center_x, center_y, radius, angle_deg):
    angle_rad = math.radians(angle_deg)
    x = center_x + radius * math.cos(angle_rad)
    y = center_y + radius * math.sin(angle_rad)
    return x, y

def calculate_new_date(day_count, start_day_of_week):
    # Assuming the new calendar starts from January 1st, 2024
    year = 2024
    month = 1
    day = 1
    day_of_week = (start_day_of_week + day_count - 1) % 7

    total_days = day_count

    while total_days >= 365:
        if year % 13 == 0:
            total_days -= 28
        else:
            total_days -= 28

        year += 1

    month += total_days // 28
    day += total_days % 28

    return year, month, day, day_of_week

def draw_calendar_svg():
    dwg = svgwrite.Drawing('13_month_calendar.svg', profile='tiny')

    # Define circle parameters
    center_x, center_y = 300, 300
    outer_radius, inner_radius = 250, 160
    num_segments = 364
    start_day_of_week = calendar.weekday(2024, 1, 1)  # January 1, 2024 is a Tuesday

    # Draw outer circle
    dwg.add(dwg.circle(center=(center_x, center_y), r=outer_radius, fill='none', stroke='black'))

    # Draw inner circle
    dwg.add(dwg.circle(center=(center_x, center_y), r=inner_radius, fill='none', stroke='black'))

    # Draw segments for each day with labels
    for i in range(num_segments):
        angle_deg = i * (360 / num_segments)
        start_point_inner = polar_to_cartesian(center_x, center_y, inner_radius, angle_deg)
        start_point_outer = polar_to_cartesian(center_x, center_y, outer_radius, angle_deg)
        label_point = polar_to_cartesian(center_x, center_y, outer_radius - 30, angle_deg)  # Adjust label distance

        # Calculate the new date
        year, month, day, day_of_week = calculate_new_date(i + 1, start_day_of_week)
        formatted_date = f"{year}/{month:02d}/{day:02d}"  # Format the date as YYYY/MM/DD

        # Get the day name
        day_name = calendar.day_name[day_of_week]

        # Add line segment
        dwg.add(dwg.line(start=start_point_inner, end=start_point_outer, stroke='black', stroke_width=0.5))

        # Add label with date, year, and day name
        date_label = f"{formatted_date}\n({day_name})"
        label_position = (label_point[0], label_point[1])  # Adjust label position

        # Calculate the rotation angle to face the center
        rotation_angle = angle_deg + 180  # Add 180 degrees for the correct orientation
        dwg.add(dwg.text(date_label, insert=label_position, font_size=4.5, text_anchor='middle', transform=f"rotate({rotation_angle},{label_position[0]},{label_position[1]})"))

    # Divide each month and week with lines
    num_months = 13
    for i in range(num_months):
        angle_deg = i * (360 / num_months)
        start_point_inner = polar_to_cartesian(center_x, center_y, inner_radius, angle_deg)
        end_point_outer = polar_to_cartesian(center_x, center_y, outer_radius, angle_deg)
        dwg.add(dwg.line(start=start_point_inner, end=end_point_outer, stroke='red'))

    # Save the SVG file
    dwg.save()

if __name__ == "__main__":
    draw_calendar_svg()
