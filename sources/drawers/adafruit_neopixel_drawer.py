import board
import neopixel

from sources.helpers.color_rgb import ColorRGB

from sources.drawers.base import DrawerBase


class NeoPixelDrawer(DrawerBase):
    calibration_table = [
        0, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 2, 2, 2, 2, 2, 2, 2,
        2, 3, 3, 3, 3, 3, 3, 3,
        4, 4, 4, 4, 4, 5, 5, 5,
        5, 6, 6, 6, 6, 7, 7, 7,
        7, 8, 8, 8, 9, 9, 9, 10,
        10, 10, 11, 11, 11, 12, 12, 13,
        13, 13, 14, 14, 15, 15, 16, 16,
        17, 17, 18, 18, 19, 19, 20, 20,
        21, 21, 22, 22, 23, 24, 24, 25,
        25, 26, 27, 27, 28, 29, 29, 30,
        31, 32, 32, 33, 34, 35, 35, 36,
        37, 38, 39, 39, 40, 41, 42, 43,
        44, 45, 46, 47, 48, 49, 50, 50,
        51, 52, 54, 55, 56, 57, 58, 59,
        60, 61, 62, 63, 64, 66, 67, 68,
        69, 70, 72, 73, 74, 75, 77, 78,
        79, 81, 82, 83, 85, 86, 87, 89,
        90, 92, 93, 95, 96, 98, 99, 101,
        102, 104, 105, 107, 109, 110, 112, 114,
        115, 117, 119, 120, 122, 124, 126, 127,
        129, 131, 133, 135, 137, 138, 140, 142,
        144, 146, 148, 150, 152, 154, 156, 158,
        160, 162, 164, 167, 169, 171, 173, 175,
        177, 180, 182, 184, 186, 189, 191, 193,
        196, 198, 200, 203, 205, 208, 210, 213,
        215, 218, 220, 223, 225, 228, 231, 233,
        236, 239, 241, 244, 247, 249, 252, 255
    ]

    calibrate = False
    intensity_min = 1
    intensity_max = 100

    def __init__(self, n_led):
        super().__init__(n_led)
        self.pixels = neopixel.NeoPixel(board.D18, n_led, auto_write=False)
        self.clear()
        self.pixels_indexes = range(0, n_led - 1)

    def set_color(self, position, color, calibrate=None):
        if calibrate is None:
            calibrate = self.calibrate

        if calibrate:
            self.pixels[position] = (self.calibration_table[color.r], self.calibration_table[color.g],
                                     self.calibration_table[color.b])
        else:
            self.pixels[position] = (color.r, color.g, color.b)

    def set_color_raw(self, position, r, g, b, calibrate=None):
        if calibrate is None:
            calibrate = self.calibrate

        if calibrate:
            self.pixels[position] = (self.calibration_table[int(r)], self.calibration_table[int(g)],
                                     self.calibration_table[int(b)])
        else:
            self.pixels[position] = (int(r), int(g), int(b))

    def set_empty(self, position):
        self.pixels[position] = (0, 0, 0)

    def show(self):
        self.pixels.show()

        if self.recording:
            frame = [] * self.n_led
            for pixel_index in self.pixels_indexes:
                frame.append(self.pixels[pixel_index])

            self.frames.append(frame)

    def clear(self, show=True):
        self.pixels.fill((0, 0, 0))
        if show:
            self.pixels.show()

    def calibrate_color(self, color):
        return ColorRGB(self.calibration_table[color.r], self.calibration_table[color.g],
                        self.calibration_table[color.b])

    def show_frame(self, frame):
        for pixel_index in self.pixels_indexes:
            self.pixels[pixel_index] = frame[pixel_index]
        self.show()

    def replay(self, timeout):
        while not timeout.is_expired():
            for frame in self.frames:
                self.show_frame(frame)
