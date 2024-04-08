import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestWeatherShopperSite(unittest.TestCase):

    def get_price(self, element) -> int:
        return int(element.find_element(By.XPATH, "./p[2]").get_property('textContent').split()[-1])

    def get_cart_state(self, driver) -> str:
        return driver.find_element(By.ID, 'cart').get_property('textContent')

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_temperature_selects_category(self):
        """
        Test objective:
        Shop for moisturizers if the temperature is below 19 degrees Celsius.
        Shop for sunscreens if the temperature is above 34 degrees Celsius.
        Do nothing if the temperature is between 19 and 34 degrees Celsius.
        Tests are successful if the title of the current web page matches the expected page title.
        """
        driver = self.driver
        driver.get("https://weathershopper.pythonanywhere.com/")
        temperature = driver.find_element(By.ID, "temperature").text.split(" ")[0]

        if int(temperature) < 19:
            b = driver.find_element(By.XPATH, "//h3[contains(text(), 'Moisturizers')]/following-sibling::a/button")
            b.click()
            self.assertEqual(driver.current_url, "https://weathershopper.pythonanywhere.com/moisturizer")
            self.assertEqual("The Best Moisturizers in the World!", driver.title)
        elif int(temperature) > 34:
            b = driver.find_element(By.XPATH, "//h3[contains(text(), 'Sunscreens')]/following-sibling::a/button")
            b.click()
            self.assertEqual(driver.current_url, "https://weathershopper.pythonanywhere.com/sunscreen")
            self.assertEqual("The Best Sunscreens in the World!", driver.title)
        else:
            self.assertEqual("Current Temperature", driver.title)

    def test_moisturizer_cart(self):
        """
        Test objective:
        Add two moisturizers to your cart. First, select the least expensive moisturizer that contains Aloe.
        For your second moisturizer, select the least expensive moisturizer that contains almond.
        Click on cart when you are done.
        """

        driver = self.driver
        driver.get("https://weathershopper.pythonanywhere.com/moisturizer")

        # Make sure cart is empty
        cart_state = self.get_cart_state(driver)
        self.assertEqual(cart_state, 'Empty')

        # Identify the cheapest item from each category
        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-center col-4')]")
        min_aloe = None
        min_almond = None
        for i in range(len(items)):
            name = items[i].find_element(By.XPATH, "./p[1]").get_property('textContent')
            if "Aloe" in name:
                price = self.get_price(items[i])
                if min_aloe is None or price < min_aloe[0]:
                    min_aloe = (price, i, name)
            if "Almond" in name:
                price = self.get_price(items[i])
                if min_almond is None or price < min_almond[0]:
                    min_almond = (price, i, name)

        # Add the items to the cart by clicking the "Add" button for each minimum price element
        # If there are no items in that category then do not add an item to the basket
        for min_item in [min_aloe, min_almond]:
            if min_item is not None:
                items[min_item[1]].find_element(By.XPATH, "./button").click()

        # Verify that there are 2 items in the cart
        cart_state = self.get_cart_state(driver)
        self.assertEqual(cart_state, '2 item(s)')

        # Click on the cart button and verify that the user is brought to the cart page
        driver.find_element(By.XPATH, "//nav/ul/button").click()
        self.assertEqual(driver.current_url, "https://weathershopper.pythonanywhere.com/cart")

        """
        Verify that the shopping cart looks correct. Then, fill out your payment details and submit the form. 
        You can Google for 'Stripe test card numbers' to use valid cards. 
        Note: The payment screen will error 5% of the time by design
        """

        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        checkout_total = 0
        for i in rows:
            item_name = i.find_element(By.XPATH, "./td[1]").get_property('textContent')
            item_price = int(i.find_element(By.XPATH, "./td[2]").get_property('textContent'))
            checkout_total += item_price

            # Verify that the names of the items in the cart are correct
            # Verify price matches the name for each item
            if item_name in min_aloe:
                self.assertEqual(item_price, min_aloe[0])
            else:
                self.assertEqual(item_price, min_almond[0])

        # Verify total price is the sum of both prices
        total_price = int(driver.find_element(By.ID, "total").get_property('textContent').split()[-1])
        self.assertEqual(total_price, checkout_total)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
