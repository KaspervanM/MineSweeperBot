from PIL import Image


def color_distance(color1, color2):
    """This function calculates the distance between two colors.

    Args:
        color1: The first color in the format (r, g, b).
        color2: The second color in the format (r, g, b).

    Returns:
        float: The distance between the two colors.
    """
    return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5


def parse_image(screenshot, field_width, field_height, color_sensitivity=5):
    """This function will parse the image and return the field data.

    Args:
        screenshot: The screenshot image of the field.
        field_width: The width of the field.
        field_height: The height of the field.
        color_sensitivity: The sensitivity of the color matching.

    Returns:
        list: The field data in the format [(x1, y1, num1), (x2, y2, num2), ...].
    """
    cell_width = screenshot.width / field_width
    cell_height = screenshot.height / field_height

    # Define a mapping of colors to labels (you may need to adjust these)
    color_to_label = {
        (222, 222, 222): 0,
        (221, 250, 195): 1,
        (236, 237, 191): 2,
        (237, 218, 180): 3,
        (237, 195, 138): 4,
        (247, 161, 162): 5,
        (254, 167, 133): 6,
        (255, 125, 96): 7,
        (255, 50, 60): 8,
    }

    # Parse the colors of each coordinate
    field_data = []

    for y in range(field_height):
        for x in range(field_width):
            image_x = x / field_width * screenshot.width + cell_width * 0.75
            image_y = y / field_height * screenshot.height + cell_height * 0.25
            pixel_color = screenshot.getpixel((image_x, image_y))
            for color, label in color_to_label.items():
                if color_distance(color, pixel_color) < color_sensitivity:
                    field_data.append((x, y, label))

    return field_data
