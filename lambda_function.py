import time
import pyotp
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
from telegramBot import send_alert
# from constant import config as user_config
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to the chromedriver.exe file


user_config = [
    # {
    #     'id': 'GC7132',
    #     'broker_name': 'Upstox',
    #     'name': 'Jaydeep',
    #     'url': 'https://www.quantman.in/?locale=en',
    #     'secret_key': 'VG6EADQM4IWXDHEKFZY3PDKA3AXF4FGR',
    #     'mobile':'8758614213',
    #     'pass': '123456'
    # },
    {
        'id':'3YB8J7',
        'name':'Nikunj',
        'broker_name':'Upstox',
        'url':'https://www.quantman.in/?locale=en',
        'secret_key': 'ITJVXEMVYRTAFATTJJQI34ANJSYWGAPQ',
        'pass' : '151015',
        'mobile': '7434002703'
    },
    {
        'id': 'FA187829',
        'broker_name': 'Finvasia',
        'name': 'Sanket',
        'url': 'https://www.quantman.in/?locale=en',
        'secret_key': 'AI266LYE7R35C75S6MZ33X22ZB7XGB25',
        'pass': 'DKking@@999'
    },
    {
        'id': 'FA163285',
        'name': 'Darshit',
        'broker_name': 'Finvasia',
        'url': 'https://www.quantman.in/?locale=en',
        'secret_key': 'J3TB5P6GAH66G76SI2645366B3DC57Y6',
        'pass': 'DKking@999'
    }
]
def generate_otp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()


def shoonya_login(driver, config):
    print("shoonya login Started")
    finvasia_id = driver.find_element(By.XPATH, '//input[@id="finvasia-id"]')
    finvasia_id.send_keys(config['id'])
    print(f"{config['id']} added")
    finvasia_password = driver.find_element(By.XPATH, '//input[@id="finvasia-password"]')
    finvasia_password.send_keys(config['pass'])
    finvasia_totp = driver.find_element(By.XPATH, '//input[@id="finvasia-totp"]')
    finvasia_totp.send_keys(generate_otp(config['secret_key']))
    finvasia_login = driver.find_element(By.CSS_SELECTOR, '#btn-finvasia')
    finvasia_login.click()
    driver.get_screenshot_as_file(f"shoonya_{config['name']}.png")
    time.sleep(5)
    caption = config['name'] + ' ' + config['broker_name']
    file = {'photo': open(f"shoonya_{config['name']}.png", 'rb')}
    send_alert(file,caption)
    time.sleep(2)
    os.remove(f"shoonya_{config['name']}.png")
    
    print("shoonya login Ended")

def upstox_login(driver, config):
    try:
        print("upstox login Started")
        upstox_id = driver.find_element(By.XPATH, '//input[@id="upstox-client-id"]')
        upstox_id.send_keys(config['id'])
        print(f"{config['id']} added")
        login_to_upstox = driver.find_element(By.XPATH, '//button[@id="btn-upstox"]')
        login_to_upstox.click()
        print(config['mobile'])
        mobile_input = (By.XPATH, '//input[@id="mobileNum"]')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(mobile_input))

        enter_mobile = driver.find_element(*mobile_input)
        enter_mobile.send_keys(config['mobile'])
        # enter_mobile = driver.find_element(By.XPATH, '//input[@id="mobileNum"]')

        # enter_mobile.send_keys(config['mobile'])
        get_otp = driver.find_element(By.XPATH, '//button[@id="getOtp"]')
        get_otp.click()

        print(config)
        totp = generate_otp(config['secret_key'])
        print(totp)
        time.sleep(2)
        enter_otp = driver.find_element(By.CSS_SELECTOR, '#otpNum')
        enter_otp.send_keys(totp)
        continue_btn = driver.find_element(By.XPATH, '//button[@id="continueBtn"]')
        continue_btn.click()
        time.sleep(3)
        find_enter_otp_btn = driver.find_element(By.XPATH, '//input[@id="pinCode"]')
        find_enter_otp_btn.send_keys(config['pass'])
        pin_continue_btn = driver.find_element(By.XPATH, '//button[@id="pinContinueBtn"]')
        pin_continue_btn.click()
        time.sleep(5)
        driver.get_screenshot_as_file("upstox_login.png")
        file = {'photo': open('upstox_login.png', 'rb')}
        caption = config['name'] + ' ' + config['broker_name']
        send_alert(file,caption)
        time.sleep(2)
        os.remove("upstox_login.png")
        print("upstox login Ended")

    except Exception as e:
        driver.get_screenshot_as_file("error.png")
        file = {'photo': open('error.png', 'rb')}
        caption = config['name'] + ' ' + config['broker_name']
        send_alert(file, caption)
        driver.quit()
        driver.close()
        print(e)


def login(config):
    try:
        # headless option
        chrome_options = Options()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_driver_path = "/usr/local/bin/chromedriver"
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver.maximize_window()
        driver.set_window_size(1920, 1080)
        # Example: Scraping a website title
        driver.get('https://www.quantman.in/')
        
        driver.find_element(By.CSS_SELECTOR, '#dropdownMenuButton').click()
        broker_name = config['broker_name']
        select_broker = driver.find_element(By.XPATH, f'//div[text()="{broker_name}"]')
        select_broker.click()
        driver.find_element(By.XPATH, '//button[text()="Login with broker"]').click()
        
        if broker_name == 'Finvasia':
            shoonya_login(driver, config)
        elif broker_name == 'Upstox':
            upstox_login(driver, config)
        driver.quit()
    except Exception as e:
        driver.quit()
        print(e)


def lambda_handler(event, context):
    for i in range(len(user_config)):
        try:
            login(user_config[i])
            print(f"Login for {user_config[i]['name']} completed")
        except Exception as e:
            print(e)
            
    return {
        'statusCode': 200,
        'body': 'Login Completed Successfully'
    }


result = lambda_handler(None, None)
print("Response:", result)

