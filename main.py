from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    fleece_jacket_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    fleece_jacket_to_cart_button.click()

    shopping_cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_container")
    shopping_cart_button.click()
    time.sleep(3)

    cart_item_name = driver.find_element(By.CSS_SELECTOR, ".cart_item_label .inventory_item_name").text
    cart_item_quantity = driver.find_element(By.XPATH, "//div[3]/*[contains(@class, 'cart_quantity')]").text
    assert cart_item_name == item_name and cart_item_quantity == quantity, "The cart does not work properly"

    driver.quit()


# Удаление товара из корзины через корзину
def test_remove_item_from_cart_using_cart():
    driver.get(URL)
    auth_data()

    fleece_jacket_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    fleece_jacket_to_cart_button.click()

    shopping_cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_container")
    shopping_cart_button.click()
    time.sleep(3)

    cart_item_name = driver.find_element(By.CSS_SELECTOR, ".cart_item_label .inventory_item_name")

    remove_fleece_jacket_button = driver.find_element(By.ID, "remove-sauce-labs-fleece-jacket")
    remove_fleece_jacket_button.click()

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "remove-sauce-labs-fleece-jacket")))
        not_found = False
    except:
        not_found = True
    time.sleep(3)
    assert not_found, f"The {cart_item_name.text} was not removed"


# Добавление товара в корзину из карточки товара
def test_add_item_to_cart_from_card():
    driver.get(URL)
    auth_data()

    bolt_t_shirt_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Sauce Labs Bolt T-Shirt')]")
    bolt_t_shirt_button.click()

    item_name = "Sauce Labs Bolt T-Shirt"
    quantity = "1"

    bolt_t_shirt_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    bolt_t_shirt_to_cart_button.click()

    shopping_cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_container")
    shopping_cart_button.click()

    time.sleep(3)

    cart_item_name = driver.find_element(By.CSS_SELECTOR, ".cart_item_label .inventory_item_name").text
    cart_item_quantity = driver.find_element(By.XPATH, "//div[3]/*[contains(@class, 'cart_quantity')]").text
    assert cart_item_name == item_name and cart_item_quantity == quantity, "The cart does not work properly"

    driver.quit()
