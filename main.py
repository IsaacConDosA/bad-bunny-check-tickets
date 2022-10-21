from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tempfile import mkdtemp
import requests
import os
# import chromedriver_binary
# import chromedriver_autoinstaller as chromedriver
# chromedriver.install()

TOKEN = "5795554631:AAGarb9au_F-mXxa99iL0DHiyL6CVOt5Qr8"
CHAT_ID = "-606505312"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())

# os.system("cp ./chromedriver /tmp/chromedriver")
# os.chmod("/tmp/chromedriver", 0o777)

XPATH_BUY_TICKETS_BUTTON = './/a[contains(@class, "btn")]'

def send_update_to_telegram(message):
    url_telegram_group = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url_telegram_group).json()

def check_tickets(event=None, context=None):
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    chrome = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    # chrome = webdriver.Chrome()

    chrome.get("https://www.puntoticket.com/bad-bunny")
    elems = chrome.find_elements(By.XPATH, XPATH_BUY_TICKETS_BUTTON)
    hay = False
    for elem in elems:
        css_class = elem.get_attribute("class")
        if "disabled" in css_class or "inactive" in css_class:
            continue
        else:
            hay = True
            break

    if hay:
        message = "Se han encontrado entradas disponibles. Apúrate! https://www.puntoticket.com/bad-bunny"
    else:
        message = "No hay entradas disponibles. Avisaré en 5 horas más."
    send_update_to_telegram(message)

if __name__ == "__main__":
    check_tickets()

