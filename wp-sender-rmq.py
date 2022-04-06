from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pika
import json

# def _login():
#     global driver
#     qr_box = '//canvas[@aria-label="Scan me!"]'
#     WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=qr_box))
#     driver.save_screenshot("qr.png")
#     time.sleep(15)
#     WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=qr_box))
#     driver.save_screenshot("qr2.png")
#     inp_xpath_search = '//div[@title="Search input textbox"]'
#     WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath_search))
#     return None


# def send(body):
#     print(body)
#     message = body.split(':')
#     global driver
#     driver.get(f"https://web.whatsapp.com/send?phone={message[0]}&text={message[1]}")
#     login_page = '//div[@class="_1E40b"][@role="button"][@style="opacity: 1;"]'
#     time.sleep(3)
#     try:
#         if driver.find_element(by=By.XPATH, value=login_page).is_displayed():
#             print("login needed")
#             _login()
#             print("login done")
#     except:
#         pass
#     inp_xpath_search = '//div[@title="Search input textbox"]'
#     WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath_search))
#     inp_xpath = '//div[@title="Type a message"]'
#     input_box = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
#     time.sleep(2)
#     input_box.send_keys(Keys.ENTER)
#     time.sleep(2)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
global driver
driver = webdriver.Chrome(executable_path="/home/arta/Downloads/chromedriver_linux64/chromedriver")

def callback(ch, method, properties, body):
    res = json.loads(body)
    global driver
    text = res.get('text')
    phone = res.get('phone')
    driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={text}")
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
                break
    except:
        pass
    inp_xpath_search = '//div[@title="Search input textbox"]'
    WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath_search))
    inp_xpath = '//div[@title="Type a message"]'
    input_box = WebDriverWait(driver,5).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    time.sleep(2)

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

channel.start_consuming()