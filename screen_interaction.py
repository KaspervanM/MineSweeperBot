from pyautogui import click
from pynput.mouse import Listener
from PIL import ImageGrab
from image_parser import parse_image


class ScreenInterface:
    """Class to select the area of the screen to take a screenshot of."""

    def __init__(self, field_width, field_height):
        """Initialize the ScreenshotAreaSelector."""
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.listener = None
        self.get_screenshot_area()
        self.field_width = field_width
        self.field_height = field_height

    def on_click(self, x, y, button, pressed):
        """Callback function to handle the mouse click event."""
        if pressed:
            if not self.x1 and not self.y1:
                self.x1, self.y1 = x, y
                print("Click the bottom-right corner of the screenshot area.")
            else:
                self.x2, self.y2 = x, y
                self.listener.stop()

    def get_screenshot_area(self):
        """Get the area of the screen to take a screenshot of.

        Returns:
            tuple: The top-left and bottom-right coordinates of the screenshot area.
        """
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        print("Click the top-left corner of the screenshot area.")
        with Listener(on_click=self.on_click) as self.listener:
            self.listener.join()

    def get_field_knowns(self):
        screenshot = ImageGrab.grab()
        cropped_screenshot = screenshot.crop((self.x1, self.y1, self.x2, self.y2))
        return parse_image(cropped_screenshot, self.field_width, self.field_height)

    def click_cell(self, x, y):
        """Click the mouse at the specified cell coordinates."""
        cell_width = (self.x2 - self.x1) / self.field_width
        cell_height = (self.y2 - self.y1) / self.field_height
        x_coord = self.x1 + cell_width * (x + 0.5)
        y_coord = self.y1 + cell_height * (y + 0.5)
        click(x_coord, y_coord)
