from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

URL = "https://www.saucedemo.com/"


# Авторизация
# Авторизация, используя корректные данные (standard_user, secret_sauce)


def auth_data():
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")

    login_button = driver.find_element(By.CLASS_NAME, "submit-button")
    login_button.click()

    time.sleep(3)


def test_login_existing_user():
    driver.get(URL)
    auth_data()

    assert driver.current_url == "https://www.saucedemo.com/inventory.html"

    driver.quit()


# Авторизация, используя некорректные данные (user, user)
def test_login_non_existing_user():
    driver.get(URL)

    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("user")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("random")

    login_button = driver.find_element(By.CLASS_NAME, "submit-button")
    login_button.click()
    time.sleep(3)

    error_button_text = driver.find_element(By.XPATH, "//h3").text
    assert error_button_text == "Epic sadface: Username and password do not match any user in this service"

    driver.quit()


# Корзина
# Добавление товара в корзину через каталог
def test_add_item_from_catalogue():
    driver.get(URL)
    auth_data()

    item_name = "Sauce Labs Fleece Jacket"
    quantity = "1"

    fleece_jacket_to_card_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    fleece_jacket_to_card_button.click()

    shopping_cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_container")
    shopping_cart_button.click()
    time.sleep(3)

    cart_item_name = driver.find_element(By.CSS_SELECTOR, ".cart_item_label .inventory_item_name").text
    cart_item_quantity = driver.find_element(By.XPATH, "//div[3]/*[contains(@class, 'cart_quantity')]").text
    assert cart_item_name == item_name and cart_item_quantity == quantity, "The cart does not work properly"

    driver.quit()
