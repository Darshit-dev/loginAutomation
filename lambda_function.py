from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def lambda_handler(event, context):
    # Setting up Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_driver_path = "/usr/local/bin/chromedriver"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Example: Scraping a website title
    driver.get("https://login.upstox.com/")
    title = driver.title
    print(title)

    # Clean up
    driver.quit()

    return {
        'statusCode': 200,
        'body': f'Title of the website: {title}'
    }

result = lambda_handler(None, None)
print("Response:", result)
