from operator import concat
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pika
import json
import os
import random
import pyperclip
from selenium.webdriver.remote.webelement import WebElement
from platform import system
from config.settings import BASE_DIR





def callback(ch, method, properties, body):
    res = json.loads(body)
    global driver
    media = res.get("media", None)
    text = res.get('text')
    phone = res.get('phone')
    login_page = '//img[@crossorigin="anonymous"][@style="visibility: visible;"][@alt=""]'
    time.sleep(3)
    try:
        while True:
            if driver.find_element(by=By.XPATH, value=login_page).is_displayed():
                qr_box = '//canvas[@aria-label="Scan me!"]'
                WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=qr_box))
                driver.save_screenshot("qr.png")
                time.sleep(15)
                try:
                    inp_xpath_search = '//div[@title="Search input textbox"]'
                    driver.find_element(by=By.XPATH, value=inp_xpath_search)
                    break
                except:
                    pass
                WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=qr_box))
                driver.save_screenshot("qr2.png")
                inp_xpath_search = '//div[@title="Search input textbox"]'
                WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath_search))
                os.remove("qr.png") 
                os.remove("qr2.png") 
                break
    except:
        pass
    inp_xpath_search = '//div[@title="Search input textbox"]'
    inp_xpath_search_box = WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath_search))
    inp_xpath_search_box.click()
    inp_xpath_search_box.send_keys('Wp test')
    selected_group = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value="//span[@title='Wp test']"))
    selected_group.click()
    inp_xpath = '//div[@title="Type a message"]'
    input_box = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
    time.sleep(random.randint(5, 10))
    contact = f"http://wa.me/{phone}"
    try:
        message_link = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH , value = f'//a[@href="{contact}"]'))
    except:
        input_box.send_keys(contact+Keys.ENTER)
        time.sleep(random.randint(7, 11))
        message_link = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH , value = f'//a[@href="{contact}"]'))
    message_link.click()
    time.sleep(random.randint(3, 9))
    if media is not None:
        from io import BytesIO

        import win32clipboard
        from PIL import Image

        image = Image.open(media)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        input_box_after_link = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
        input_box_after_link.send_keys(text)
        input_box_after_link.send_keys(Keys.CONTROL + "v")
        inp_xpath = '//div[@role="button"][@aria-label="Send"]'
        input_box_after_link_image = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
        time.sleep(2)
        input_box_after_link_image.click()
                
    else:
        input_box_after_link = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
        input_box_after_link.send_keys(text + Keys.ENTER)
    time.sleep(random.randint(8, 15))

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)


def start():
    global driver
    if system().lower() == "linux":
        driver_exe = "chromium/linux/chromedriver"
    elif system().lower() == "windows":
        driver_exe = r"chromium\windows\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_exe)
    driver.get(f"https://web.whatsapp.com/")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    try:
        channel.start_consuming()
    except:
        main()


main()