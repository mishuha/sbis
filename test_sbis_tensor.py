# -*- coding: utf-8 -*-
from base_case_setup import BaseSetup
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
import os
import logging
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

logger = logging.getLogger(__name__)

PROGRAM_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class TestSbisToTensor(BaseSetup):
    def test_case1(self):
        logger.info('1st case start')

        sbis_page = SbisPage(PROGRAM_DIR)
        tensor_page = TensorPage(PROGRAM_DIR)

        # Переходим на страницу sbis.ru и в раздел "Контакты"
        sbis_page.go_to(self, "https://sbis.ru/")
        sbis_page.click_contacts(self)
        sbis_page.go_to_contacts_page(self)  # Не сходится с ТЗ, доп. действие

        # Находим и кликаем по баннеру Тензор
        sbis_page.click_tensor_banner(self)

        # Проверяем, что тут есть блок "Сила в людях"
        tensor_page.check_strength_in_people_block(self)

        # Переходим по ссылке "Подробнее"
        tensor_page.go_to_more_details(self)

        # Проверяем, что страница https://tensor.ru/about
        tensor_page.check_about_page(self)

        # Проверяем фотографии в хронологии
        # time.sleep(3)
        tensor_page.check_chronology_images(self)

    def test_case2(self):
        logger.info('2nd case start')

        sbis_page = SbisPage(PROGRAM_DIR)
        # Переходим на страницу sbis.ru и в раздел "Контакты"
        sbis_page.go_to(self, "https://sbis.ru/")
        sbis_page.click_contacts(self)
        sbis_page.go_to_contacts_page(self)  # Не сходится с ТЗ, доп. действие

        # Проверить, что определился ваш регион (в нашем примере Ярославская обл.)
        sbis_page.check_local_region(self)
        # есть список партнеров.
        sbis_page.count_partners(self)
        sbis_page.switch_region(self)

        # Проверить, что подставился выбранный регион,
        self.sleep(1)
        sbis_page.check_new_region(self)
        # список партнеров изменился,
        sbis_page.check_partners_changed(self)
        # url и title содержат информацию выбранного региона
        sbis_page.check_region_in_title(self)
        sbis_page.check_page_url_region(self)

    def test_case3(self):
        logger.info('3rd case start')

        sbis_page = SbisPage(PROGRAM_DIR)

        # Перейти на https://sbis.ru/
        sbis_page.go_to(self, "https://sbis.ru/")

        # В Footer'e найти и перейти "Скачать локальные версии"
        sbis_page.go_to_downloads(self)

        # Скачать СБИС Плагин для вашей для windows, веб-установщик в папку с данным тестом
        sbis_page.download_plugin(self)

        # Скачан и размер соответствует указанному на сайте
        sbis_page.check_download_plugin()
