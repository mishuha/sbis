from seleniumbase import BaseCase
from seleniumbase import get_driver
import logging
logger = logging.getLogger(__name__)


class BaseSetup(BaseCase):
    def setUp(self):
        super().setUp()
        # self.driver = get_driver(browser="chrome", headless=True)
        self.maximize_window()

    def tearDown(self):
        self.save_teardown_screenshot()  # If test fails, or if "--screenshot"
        if self.has_exception():
            pass
        else:
            pass
        # <<< Run custom tearDown() code BEFORE the super().tearDown() >>>
        super().tearDown()

