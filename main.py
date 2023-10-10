from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

URL = "https://www.saucedemo.com/"

# Авторизация
# Авторизация, используя корректные данные (standard_user, secret_sauce)

def test_login_existing_user():
    driver.get(URL)

    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")

    login_button = driver.find_element(By.CLASS_NAME, "submit-button")
    login_button.click()

    time.sleep(3)

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