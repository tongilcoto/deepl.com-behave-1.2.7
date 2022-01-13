import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utils.driver import element_value_is_not_null
from utils.driver import get_array_of_elements_text_for_elements_array



class MainPage:

    def __init__(self, language):
        """
        Initialises Main page model. It creates the selenium webdriver object and loads the selectors configuration file
        """
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.deepl.com')
        self.wait = WebDriverWait(self.driver, 10)
        self.selectors = json.load(open('sut/selectors/mainPage.json'))

    def input_source_text(self, text):
        """
        Informs the text to be translated
        :param text: string. text to be translated
        """
        source_text_element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.selectors['source_text'])))
        source_text_element.send_keys(text)

    def get_translated_text(self):
        """
        Gets the translated text
        :return: string
        """
        translated_text_element = self.wait.until(element_value_is_not_null((By.CSS_SELECTOR, self.selectors['translated_text'])))
        return translated_text_element.get_attribute('value').strip()

    def get_original_language(self):
        """
        Gets the translated text
        :return: string
        """
        original_language_label_element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.selectors['original_language_label'])))
        return original_language_label_element.text

    def get_translation_lemma_elements(self):
        """
        Gets the translation lemmas elements
        :return: WebElement[]
        """
        try:
            self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, self.selectors["array_translation_lemma_element"])))
        except TimeoutException:
            return []
        return self.driver.find_elements(By.CSS_SELECTOR, self.selectors["array_translation_lemma_element"])

    def get_translation_lemma_label(self, lemma_element):
        """
        Gets the translation lemmas label. Same as input word
        :return: string
        """
        return lemma_element.find_element(By.CSS_SELECTOR, self.selectors["array_translation_lemma_label"]).text

    def get_translation_lemma_wordtype(self, lemma_element):
        """
        Gets the translation lemmas wordtype
        :return: string
        """
        return lemma_element.find_element(By.CSS_SELECTOR, self.selectors["array_translation_lemma_wordtype"]).text

    def get_translation_lemma_meanings_label(self, lemma_element):
        """
        Gets the translation meanings [label] for a given lemma element
        :return: string[]
        """
        return get_array_of_elements_text_for_elements_array(lemma_element, self.selectors["array_translation_meaning_label"])

    def get_translation_lemma_usages(self, lemma_element):
        """
        Gets the translation meanings [label] for a given lemma element
        :return: string[]
        """
        return get_array_of_elements_text_for_elements_array(lemma_element, self.selectors["array_translation_lemma_usage"])

    def get_translation_alternatives(self):
        """
        Gets the translation alternatives [label]
        :return: string[]
        """
        return get_array_of_elements_text_for_elements_array(self.driver, self.selectors["array_translation_alternatives"])

    def close(self):
        """
        Closes the selenium webdriver
        """
        self.driver.close()

    def get_screenshot(self, screenshot_name):
        """
        Saves the screenshot of current page
        :param screenshot_name: screenshot file name
        :return: screenshot data
        """
        self.driver.save_screenshot(screenshot_name)
        return self.driver.get_screenshot_as_png()

