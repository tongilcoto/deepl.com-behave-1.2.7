from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By


def element_value_is_not_null(locator):
    """
    An expectation for checking if the element's value is filled
    locator, text
    """

    def _predicate(driver):
        try:
            element_text = driver.find_element(*locator).get_attribute("value")
            return driver.find_element(*locator) if element_text != "" else ""
        except InvalidSelectorException as e:
            raise e
        except StaleElementReferenceException:
            return False

    return _predicate


def get_array_of_elements_text_for_elements_array(parent_element, selector):
    text_array = []
    for element in parent_element.find_elements(By.CSS_SELECTOR, selector):
        text_array.append(element.text)

    return text_array
