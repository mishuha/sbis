# -*- coding: utf-8 -*-
from pages.base_page import BasePage
from transliterate import translit
import re
import os
import logging

from lib import lib

logger = logging.getLogger(__name__)


class SbisPage(BasePage):
    CONTACTS_BAR = "//div[contains(@class,'Header')]/child::div[contains(text(), 'Контакты')]"
    CONTACTS_LINK = "//div[contains(@class,'Header')]/child::a[contains(@href, 'contacts')]"
    TENSOR_BANNER = "//div[@id='contacts_clients']//child::a[contains(@class,'logo') and contains(@href,'//tensor.ru') and contains(@title,'tensor.ru')]"

    CONTACTS_CURRENT_REGION = "//div[contains(@class, 'sbis_ru-container sbisru-Contacts__relative')]//span[contains(@class, 'sbis_ru-Region-Chooser__text sbis_ru-link')]"
    REGION_TEXT_LOCAL = 'Костром'
    REGION_TEXT_NEW = 'Камчат'
    REGION_SELECTOR = f"//div[@name='dialog']"
    REGION_NEW = REGION_SELECTOR + f"//span[contains(text(),'{REGION_TEXT_NEW}')]"
    PARTNERS_NAMES = "//div[contains(@class, 'sbisru-Contacts-List__col')]//div[@name='itemsContainer']//div[@title and contains(@class, 'sbisru-Contacts-List__name')]"

    DOWNLOAD_LOCAL_VERSIONS = "//div[contains(@class, 'Footer')]//a[. = 'Скачать локальные версии']"
    SELECT_PLUGIN_TAB = "//div[@name='TabButtons']//div[text() = 'Saby Plugin']"
    SELECT_WINDOWS_TAB = "//div[@data-for='plugin']//span[contains(text(), 'Windows')]"
    PLUGIN_WEB_INSTALLER = "//div[@name = 'SwitchableArea']//div[contains(@class, 'DownloadNew-block')]//h3[contains(text(), 'Веб-установщик')]"
    PLUGIN_GET_LINK = PLUGIN_WEB_INSTALLER + "/../..//a[contains(text(), 'Скачать')]"

    current_region = None
    current_partner_list = []
    file_metadata = {'expected_size': .0, 'file_path': ''}

    def click_contacts(self, sb):
        sb.click(self.CONTACTS_BAR)

    def go_to_contacts_page(self, sb):
        sb.click(self.CONTACTS_LINK)

    def click_tensor_banner(self, sb):
        sb.click(self.TENSOR_BANNER)
        sb.switch_to_newest_window()  # firefox only?

    def get_region(self, sb):
        self.current_region = sb.find_element(self.CONTACTS_CURRENT_REGION).text

    def check_region(self, sb, region_name):
        self.get_region(sb)
        logger.info(f'Looking for: "{region_name}" in "{self.current_region}"')
        assert region_name in self.current_region

    def check_local_region(self, sb):
        self.check_region(sb, self.REGION_TEXT_LOCAL)

    def get_partners(self, sb):
        for element in sb.find_elements(self.PARTNERS_NAMES):
            self.current_partner_list.append(element.text)

    def count_partners(self, sb):
        self.get_partners(sb)
        assert len(self.current_partner_list) > 0
        
    def switch_region(self, sb):
        sb.click(self.CONTACTS_CURRENT_REGION)
        sb.assert_element_present(self.REGION_SELECTOR)
        sb.assert_element_present(self.REGION_NEW)
        sb.click(self.REGION_NEW)

    def check_new_region(self, sb):
        self.check_region(sb, self.REGION_TEXT_NEW)

    def check_partners_changed(self, sb):
        local_list = set()
        for element in sb.find_elements(self.PARTNERS_NAMES):
            local_list.add(element.text)
        assert local_list != set(self.current_partner_list)

    def check_region_in_title(self, sb):
        assert self.current_region in sb.get_title()

    def check_page_url_region(self, sb):
        url = sb.get_current_url()
        url_trans = re.findall('-.*?-', url.split('/')[-1].split('?')[0])[0].lower()
        trans_region_text = translit(self.REGION_TEXT_NEW, 'ru', reversed=True).lower()
        # todo:
        #   aja != aya
        # print()
        # print(trans_region_text)
        # print(url_trans)
        assert trans_region_text in url_trans

    def go_to_downloads(self, sb):
        sb.click(self.DOWNLOAD_LOCAL_VERSIONS)
        sb.wait_for_element_clickable(self.SELECT_PLUGIN_TAB).click()
        sb.wait_for_element_clickable(self.SELECT_WINDOWS_TAB).click()

    def download_plugin(self, sb):
        _ = sb.find_element(self.PLUGIN_GET_LINK)  # built-in assert?
        url = _.get_attribute('href')
        filename = os.path.basename(url)
        file_path = os.path.join(sb.PROGRAM_DIR, filename)
        text_size = re.findall('\d+[\.|,]\d+', sb.find_element(self.PLUGIN_GET_LINK).text)
        assert len(text_size) > 0  # any match
        file_size_expected = lib.str2float(text_size[0])  # MB
        if os.path.isfile(file_path):
            os.remove(file_path)
        self.download_file(sb, url, path=sb.PROGRAM_DIR)
        self.file_metadata.update({'expected_size': file_size_expected, 'file_path': file_path})

    def check_download_plugin(self):
        file_path = self.file_metadata['file_path']
        file_size_expected = self.file_metadata['expected_size']
        precision = len(str(file_size_expected).split('.')[1])
        # last_valued_digit = float('0.' + '0' * (precision - 1) + '1')
        last_valued_digit = 1 / 10**precision
        logger.debug(f'precision: {precision}, last_valued_digit: {last_valued_digit}')
        # file exists
        assert os.path.isfile(file_path)
        file_size_real = round(os.path.getsize(file_path) / (1 << 20), precision)  # MB
        logger.debug(f'real: {file_size_real} MB, expected: {file_size_expected} MB')
        assert file_size_real - file_size_expected < last_valued_digit  # conversion error
