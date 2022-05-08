"""
    Uses browser to automate actions
    Proxies - -
https://www.alpharithms.com/scraping-dynamic-websites-with-webdriver-python-253418/
"""
from os import path, getcwd
from selenium import webdriver as web_driver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from loguru import logger

PROJECT_PATH = path.abspath(path.dirname(__file__))


class Browser:
    """
    Usage
    browser = Browser(cloudflare_bypass=False)
    driver = browser.get_driver()
    driver.get("https://www.delfi.com")
    """
    def __init__(self, headless: bool = False, extension: str = '', implicit_wait: int = 10, cloudflare_bypass=False):
        self.__version = 0.01
        self.options = Options()
        self.webdriver = web_driver
        self.headless = headless
        self.headless_init()

        if cloudflare_bypass:
            import undetected_chromedriver as uc
            logger.debug(f'Loading Bypass Cloudflare protection configuration')
            self.driver = uc.Chrome(options=self.options)
        else:
            service = Service(ChromeDriverManager().install())
            self.driver = self.webdriver.Chrome(service=service, options=self.options)


        self.extension = extension
        self.implicit_wait = implicit_wait

        if extension:
            logger.debug(f'Loading extension: {extension}')
            self.init_extension()




        logger.debug(f'Setting implicit wait: {implicit_wait} s')
        self.driver.implicitly_wait(self.implicit_wait)  # So that we don't need to use  WebDriverWait

    def get_driver(self):
        return self.driver

    def headless_init(self):
        "Full-screen in debug mode, headless in prod"
        if self.headless:
            logger.debug("Running in headless mode")
            self.options.add_argument('--headless')
            self.options.add_argument('--window-size=1920,1080')
        else:
            logger.debug("Running in browser mode")
            logger.debug("Running in full-screen mode")
            self.options.add_argument('--window-size=1920,1080')

    def init_extension(self):
        """
        Adds one extension .crx to chrome browser
        """
        self.options = self.webdriver.ChromeOptions()
        extension_path = path.join(PROJECT_PATH, self.extension)
        logger.debug(f'Extension path: {extension_path}')
        if not path.exists(extension_path):
            logger.debug(f'Changing path')
            extension_path = path.join(getcwd(), self.extension)
            if path.exists(extension_path):
                logger.debug(f'Extension path: {extension_path}')
                self.options.add_extension(extension_path)
                return
        if path.exists(extension_path):
            self.options.add_extension(extension_path)
        else:
            error = "Invalid browser extension (.crx) path!"
            logger.error(error)
            raise ValueError(error)


def run_here():
    browser = Browser(cloudflare_bypass=False)
    driver = browser.get_driver()
    driver.get("https://www.skelbiu.lt/skelbimai/?autocompleted=1&keywords=&submit_bn=&cost_min=&cost_max=&type=0&condition=&cities=465&distance=0&mainCity=1&search=1&category_id=83&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=1&detailsSearch=0")
    print("test")
if __name__ == "__main__":
    run_here()
