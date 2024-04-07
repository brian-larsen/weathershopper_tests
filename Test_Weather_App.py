import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTemperatureSite(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_temperature_selects_category(self):
        driver = self.driver
        driver.get("https://weathershopper.pythonanywhere.com/")
        temperature = driver.find_element(By.ID, "temperature").text.split(" ")[0]

        if int(temperature) < 19:
            b = driver.find_element(By.XPATH, "//h3[contains(text(), 'Moisturizers')]/following-sibling::a/button")
            b.click()
            self.assertEqual("https://weathershopper.pythonanywhere.com/moisturizer", driver.current_url)
            self.assertEqual("The Best Moisturizers in the World!", driver.title)
        elif int(temperature) > 34:
            b = driver.find_element(By.XPATH, "//h3[contains(text(), 'Sunscreens')]/following-sibling::a/button")
            b.click()
            self.assertEqual("https://weathershopper.pythonanywhere.com/sunscreen", driver.current_url)
            self.assertEqual("The Best Sunscreens in the World!", driver.title)
        else:
            t = "no purchases today"

    def test_moisturizer_cart(self):
        # least expensive containing aloe
        # least expensive containing almond
        # click cart
        driver = self.driver
        driver.get("https://weathershopper.pythonanywhere.com/moisturizer")
        return

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
