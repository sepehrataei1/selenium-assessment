import unittest
import time, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class HomePageSelectors:
    email_input = (By.XPATH, '//div[@id="test-1-div"]//form[@class="form-signin"]//input[@type="email"]')
    password_input = (By.XPATH, '//div[@id="test-1-div"]//form[@class="form-signin"]//input[@type="password"]')
    login_button = (By.XPATH, '//div[@id="test-1-div"]//form[@class="form-signin"]//button[@type="submit"]')
    test_2_items = (By.XPATH, '//div[@id="test-2-div"]//ul[@class="list-group"]/li[contains(text(), "List")]')
    test_2_badges = (By.XPATH, '//div[@id="test-2-div"]//ul[@class="list-group"]/li/span')
    test_3_button = (By.XPATH, '//div[@id="test-3-div"]//div[@class="dropdown"]//button[@type="button"]')
    test_3_options = (By.XPATH, '//div[@id="test-3-div"]//a[@class="dropdown-item"]')
    test_4_buttons = (By.XPATH, '//div[@id="test-4-div"]//button')
    test_5_button = (By.XPATH, '//div[@id="test-5-div"]/button')
    success_message = (By.XPATH, '//div[@id="test-5-div"]//div[@id="test5-alert"]')
    test_6_grid_cells = (By.XPATH, '//div[@id="test-6-div"]//table//tbody/tr/td')


class ResolverTests(unittest.TestCase):

    # Catch exception when element is not found
    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(*xpath)
        except NoSuchElementException:
            return False
        return True

    # Return value at grid cell x,y
    def get_value_in_grid(self, x, y):
        test_6_grid_cells = self.driver.find_elements(*HomePageSelectors.test_6_grid_cells)
        test_6_grid_values = [[], [], []]
        # Build a 3x3 array to store grid values
        test_6_grid_values[0] = [test_6_grid_cells[0].text, test_6_grid_cells[1].text, test_6_grid_cells[2].text]
        test_6_grid_values[1] = [test_6_grid_cells[3].text, test_6_grid_cells[4].text, test_6_grid_cells[5].text]
        test_6_grid_values[2] = [test_6_grid_cells[6].text, test_6_grid_cells[7].text, test_6_grid_cells[8].text]
        return test_6_grid_values[x][y]

    # setUp runs before every test
    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.html_file = os.getcwd() + "//" + "QE-index.html"
        self.driver.get("file:///" + self.html_file)

    # tearDown runs after every test
    def tearDown(self) -> None:
        self.driver.close()

    def test_1(self) -> None:
        assert self.check_exists_by_xpath(HomePageSelectors.email_input)
        assert self.check_exists_by_xpath(HomePageSelectors.password_input)
        assert self.check_exists_by_xpath(HomePageSelectors.login_button)
        # Find email and pw fields and enter values
        email_input = self.driver.find_element(*HomePageSelectors.email_input)
        password_input = self.driver.find_element(*HomePageSelectors.password_input)
        email_input.send_keys("resolver@resolver.com")
        password_input.send_keys("Resolver!")

    def test_2(self) -> None:
        list_elements = self.driver.find_elements(*HomePageSelectors.test_2_items)
        list_badges = self.driver.find_elements(*HomePageSelectors.test_2_badges)
        # Count number of list elements
        num_list_elements = len(list_elements)
        assert num_list_elements is 3
        second_list_item = list_elements[1].text
        second_list_badge = list_badges[1].text
        # Remove badge text and trailing whitespace
        second_list_item = second_list_item.replace(second_list_badge, "").strip()
        assert second_list_item == "List Item 2"
        assert second_list_badge == "6"

    def test_3(self) -> None:
        test_3_button = self.driver.find_element(*HomePageSelectors.test_3_button)
        test_3_default = test_3_button.text
        assert test_3_default == "Option 1"
        test_3_button.click()
        test_3_options = self.driver.find_elements(*HomePageSelectors.test_3_options)
        # select third option
        test_3_option_3 = test_3_options[2]
        test_3_option_3.click()

    def test_4(self) -> None:
        buttons = self.driver.find_elements(*HomePageSelectors.test_4_buttons)
        # Assert first button is enabled and second is disabled
        assert buttons[0].is_enabled()
        assert not buttons[1].is_enabled()

    def test_5(self) -> None:
        # Wait a maximum of 100 seconds for the button to be clickable
        WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable(HomePageSelectors.test_5_button))
        test_5_button = self.driver.find_element(*HomePageSelectors.test_5_button)
        test_5_message = self.driver.find_element(*HomePageSelectors.success_message)
        test_5_button.click()
        assert test_5_message.is_displayed()
        assert not test_5_button.is_enabled()

    def test_6(self) -> None:
        val = self.get_value_in_grid(2, 2)
        assert val == 'Ventosanzap'


