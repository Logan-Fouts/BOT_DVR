import time
from dataclasses import dataclass
import easyocr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pyautogui as pg


@dataclass
class Platform:
    """
    Stores information about streaming platform
    to be recoreded.
    """

    name: str
    img_ll: str
    move_left: int
    move_top: int


class MetaPuller:
    """
    Defines functions to pull episode length from any
    media on a supported streaming platform.
    """

    def __init__(self, slctd_pltfrm=0):
        self.slctd_pltfrm = slctd_pltfrm
        self.platforms = []
        self.setup_platforms()
        self.final_ss = "ep_length.png"
        self.length = 0

    def run(self):
        """
        Pulls length of episode from screen shot.
        """
        length_pos = self.locate_length(self.platforms[self.slctd_pltfrm])
        self.take_screenshot(length_pos, self.platforms[self.slctd_pltfrm])

        self.extract_number_from_image(self.final_ss)

        self.timestamp_to_seconds(self.length)

    def setup_platforms(self):
        """
        Sets up all streaming platform options.
        """
        self.platforms = [
            Platform(
                name="Dinsey",
                img_ll="ll_images/disney_ll.png",
                move_left=30,
                move_top=25,
            ),
            Platform(
                name="Netflix",
                img_ll="ll_images/netflix_ll.png",
                move_left=80,
                move_top=-65,
            ),
        ]

    def locate_length(self, pltfrm):
        """
        Wake and pause screen with mouse then return
        location of length number.
        """
        time.sleep(2)
        pg.click(960, 540, duration=0.5)
        time.sleep(0.25)

        return pg.locateOnScreen(pltfrm.img_ll, grayscale=False, confidence=0.75)

    def take_screenshot(self, pos, pltfrm):
        """
        Given position values takes screenshot of time stamp.
        """
        left = int(pos.left + pltfrm.move_left)
        top = int(pos.top + pltfrm.move_top)

        pg.click(960, 545, duration=0.5)
        pg.screenshot(region=(left, top, pos.width, pos.height)).save(self.final_ss)

    def extract_number_from_image(self, image_path):
        """
        Uses EasyOCR to extract timestamp from screenshot.
        """
        reader = easyocr.Reader(["en"])

        image = Image.open(image_path).convert("L")
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2).filter(ImageFilter.SHARPEN)

        image_np = np.array(image)

        results = reader.readtext(image_np)

        if results:
            self.length = results[0][1]
        else:
            self.length = 0

        print(f"Interpreted episode length: {self.length}")

    def timestamp_to_seconds(self, timestamp):
        """
        Converts time stamp into seconds to record.
        hours:mins:seconds
        """
        cleaned = "".join(filter(str.isdigit, timestamp))

        if len(cleaned) % 2 != 0:
            cleaned = "0" + cleaned

        pairs = [cleaned[max(0, i - 2) : i] for i in range(len(cleaned), 0, -2)]

        total_seconds = 0
        for i, pair in enumerate(pairs):
            total_seconds += int(pair) * (60**i)

        self.length = total_seconds

        if self.slctd_pltfrm == 0:
            self.length = self.length - 60
