"""
This script automates the process of interacting with a web page using Selenium WebDriver.

The script requires the following environment variables:
- USER_NAME: The user's name.
- ID_VALUE: The ID value.
- URL: The URL of the web page.
- FORM_ELEMENT: The form element to be interacted with.
- BUTTON_ID: The ID of the button to be clicked.

These should be added to a .env file in the same directory as the script.

Dependencies:
    Selenium WebDriver
    python-dotenv: To load environment variables from .env file.
"""

import time
import os
import ssl
import sys
import smtplib
import signal
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

load_dotenv()

NAME = os.getenv("NAME")
ID_VALUE = os.getenv("ID_VALUE")
URL = os.getenv("URL")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")

BTN_ACEPTAR = "btnAceptar"
BTN_ENTRAR = "btnEntrar"
BTN_ENVIAR = "btnEnviar"
APPOINTMENT_AVAILABLE = False


def signal_exit_handler(signum, frame):
    """Handles the exit signal."""
    print("Exiting...")
    if APPOINTMENT_AVAILABLE:
        print("An appointment was found.")
    else:
        print("No appointment was found.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_exit_handler)


def send_email():
    """Sends an email."""

    msg = EmailMessage()
    msg["Subject"] = "Appointment available! 🎉"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_SENDER
    now = datetime.now()
    msg.set_content(
        f"""An appointment was found at {now.strftime('%H:%M:%S')}!, 
        hurry up and go to this link: {URL}"""
    )

    ctx = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())


def main():
    """Main function."""
    global APPOINTMENT_AVAILABLE
    driver = webdriver.Chrome()

    driver.get(URL)

    driver.implicitly_wait(2)
    request_exeded = driver.find_element(By.TAG_NAME, "h1")

    if request_exeded is not None:
        request_exeded = request_exeded.get_attribute("innerText")

        if request_exeded == "Too Many Requests":
            print("Request exceded.")
            return

    driver.implicitly_wait(10)
    driver.find_element(By.ID, "form").send_keys("Madrid")

    driver.find_element(By.ID, BTN_ACEPTAR).click()

    driver.find_element(By.ID, "tramiteGrupo[0]").send_keys(
        "POLICIA-CERTIFICADOS (DE RESIDENCIA, DE NO RESIDENCIA Y DE CONCORDANCIA)"
    )

    driver.find_element(By.ID, BTN_ACEPTAR).click()

    btn_enter_item = driver.find_element(By.ID, BTN_ENTRAR)

    footer = driver.find_element(By.ID, "footerNew")

    delta_y = footer.rect["y"]
    ActionChains(driver).scroll_by_amount(0, delta_y).perform()

    btn_enter_item.click()

    driver.find_element(By.ID, "rdbTipoDocDni").click()

    driver.find_element(By.ID, "txtIdCitado").send_keys(ID_VALUE)

    driver.find_element(By.ID, "txtDesCitado").send_keys(NAME)

    driver.find_element(By.ID, BTN_ENVIAR).click()

    inner_text = driver.find_element(By.XPATH, '//p[@class="mf-msg__info"]/span')

    if inner_text is not None:
        inner_text = inner_text.get_attribute("innerText")

        if inner_text != "Información: En este momento no hay citas disponibles":
            print("Appointment available!")
            APPOINTMENT_AVAILABLE = True
            print(URL)
            send_email()
            time.sleep(15)

    driver.quit()


if __name__ == "__main__":
    while True:
        main()
        print("Waiting 10 minutes...")
        time.sleep(600)
