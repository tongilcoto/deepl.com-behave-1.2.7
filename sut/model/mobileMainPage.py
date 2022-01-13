import json
from sut.model.mainPage import MainPage as DesktopMainPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class MainPage(DesktopMainPage):

    def __init__(self, language):
        """
        Initialises Mobile Main page model. It creates the selenium webdriver object and loads the selectors configuration file
        """
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://www.deepl.com')
        self.wait = WebDriverWait(self.driver, 10)
        self.selectors = json.load(open('sut/selectors/mainPage.json'))
        self.selectors |= json.load(open('sut/selectors/mobileMainPage.json'))


