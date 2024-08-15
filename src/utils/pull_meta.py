import time
import easyocr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pyautogui as pg

from models.platforms import PlatformFactory as pfrms
from .singleton_meta import SingletonMeta


class MetaPuller(metaclass=SingletonMeta):
    """
    Defines functions to pull episode length from any
    media on a supported streaming platform.
    """

    def __init__(self, slctd_pltfrm=0):
        self.slctd_pltfrm = slctd_pltfrm
        self.pltfrm = None
        self.setup_platforms()
        self.final_ss = "assets/images/ep_length.png"
        self.length = 0

    def run(self):
        """
        Pulls length of episode from screen shot.
        """
        length_pos = self.locate_length(self.pltfrm)
        self.take_screenshot(length_pos, self.pltfrm)

        self.extract_number_from_image(self.final_ss)

        self.timestamp_to_seconds(self.length)

    def setup_platforms(self):
        """
        Sets up the chosen platform's data class to be used.
        """
        platform_mapping = {0: "Disney", 1: "Netflix"}

        platform_name = platform_mapping.get(self.slctd_pltfrm)

        if platform_name is None:
            raise ValueError(f"Invalid platform selection: {self.slctd_pltfrm}")

        self.pltfrm = pfrms.create_platform(platform_name)

    def locate_length(self, pltfrm):
        """
        Wake and pause screen with mouse then return
        location of length number.
        """
        location = None

        while location is None:
            time.sleep(3)
            pg.hotkey("alt", "tab")
            time.sleep(2)
            pg.click(360, 140, duration=2)
            location = pg.locateOnScreen(
                pltfrm.img_ll, grayscale=False, confidence=0.75
            )

        return location

    def find_skip(self):
        """
        Tries to see if episode is over using skip button on each platform.
        """
        try:
            return pg.locateOnScreen(
                self.pltfrm.img_end, grayscale=False, confidence=0.75
            )
        except pg.ImageNotFoundException:
            print("Image not found on screen")
            return None

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
            self.length = self.length - 50

        pg.hotkey("alt", "tab")

    def reset_run(self):
        """
        Attempts to restart episode before running again.
        """
        print("Reseting this episode and trying again.")

        time.sleep(2)
        pg.hotkey("alt", "tab")

        time.sleep(2)
        pg.click(950, 600, duration=0.5)

        time.sleep(5)
        pg.hotkey("ctrl", "shift", "r")

        time.sleep(10)
        pg.click(950, 600, duration=0.5)

        time.sleep(5)
        pg.hotkey("f")

        time.sleep(6)
        for _ in range(200):
            time.sleep(0.17)
            pg.press("left")

        time.sleep(5)
        pg.click(960, 545, duration=1)

        pg.hotkey("alt", "tab")

        self.run()
