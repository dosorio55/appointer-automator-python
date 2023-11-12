"""
This script automates the process of interacting with a web page using Selenium WebDriver.

The script requires the following environment variables:
- USER_NAME: The user's name.
- ID_VALUE: The ID value.
- URL: The URL of the web page.

These should be added to a .env file in the same directory as the script.

Dependencies:
    Selenium WebDriver
    python-dotenv: To load environment variables from .env file.
"""

import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
load_dotenv()

NAME = os.getenv("NAME")
ID_VALUE = os.getenv("ID_VALUE")
URL = os.getenv("URL")

BTN_ACEPTAR = "btnAceptar"
BTN_ENTRAR = "btnEntrar"
BTN_ENVIAR = "BTN_ENVIAR"

driver.get(URL)

driver.implicitly_wait(10)
time.sleep(2)

driver.find_element(By.ID, "form").send_keys("Madrid")

driver.find_element(By.ID, BTN_ACEPTAR).click()

driver.find_element(By.ID, "tramiteGrupo[0]").send_keys(
    "POLICIA-CERTIFICADOS (DE RESIDENCIA, DE NO RESIDENCIA Y DE CONCORDANCIA)"
)

driver.find_element(By.ID, BTN_ACEPTAR).click()

btnEnterItem = driver.find_element(By.ID, BTN_ENTRAR)

footer = driver.find_element(By.ID, "footerNew")

delta_y = footer.rect["y"]
ActionChains(driver).scroll_by_amount(0, delta_y).perform()

btnEnterItem.click()

driver.find_element(By.ID, "rdbTipoDocDni").click()

driver.find_element(By.ID, "txtIdCitado").send_keys(ID_VALUE)

driver.find_element(By.ID, "txtDesCitado").send_keys(NAME)

driver.find_element(By.ID, BTN_ENVIAR).click()

time.sleep(10)


driver.quit()
