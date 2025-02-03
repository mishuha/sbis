import logging
logger = logging.getLogger(__name__)


class BasePage:
    def go_to(self, sb, url):
        sb.open(url)

    def download_file(self, sb, file_url, path='.'):
        sb.download_file(file_url, destination_folder=path)

    # def __init__(self, home_dir):
    #     self.PROGRAM_DIR = home_dir
    #     logger.info(self.PROGRAM_DIR)
