# -*- coding: utf-8 -*-
from pages.base_page import BasePage
import logging


logger = logging.getLogger(__name__)


class TensorPage(BasePage):
    STRENGTH_IN_PEOPLE_BLOCK = "//p[. = 'Сила в людях']"
    MORE_DETAILS_LINK = "//p[. = 'Сила в людях']/..//a[. = 'Подробнее']"
    WORKING_SECTION = "//h2[. = 'Работаем']"
    IMG_CONTAINER = WORKING_SECTION + "/../../../div[contains(@class, 'block3')]/div[contains(@class, 'Grid-container')]"
    CHRONOLOGY_IMAGES = IMG_CONTAINER + "//div[contains(@class, 'image-wrapper')]/img"

    def check_strength_in_people_block(self, sb):
        # assert sb.is_element_present(self.STRENGTH_IN_PEOPLE_BLOCK)
        sb.assert_element_present(self.STRENGTH_IN_PEOPLE_BLOCK)

    def go_to_more_details(self, sb):
        sb.click(self.MORE_DETAILS_LINK)

    def check_about_page(self, sb):
        assert sb.get_current_url() == "https://tensor.ru/about"

    def check_chronology_images(self, sb):
        images = sb.find_elements(self.CHRONOLOGY_IMAGES)
        heights = set()
        widths = set()
        for image in images:
            size = image.size
            heights.add(size['height'])
            widths.add(size['width'])
        assert len(heights) == 1, "Images have different heights"
        assert len(widths) == 1, "Images have different widths"
