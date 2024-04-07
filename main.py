from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from dotenv import dotenv_values
from playsound import playsound
from twilio.rest import Client


def get_credentials():
    return dotenv_values(".env")


def email():
    return get_credentials()['email']


def password():
    return get_credentials()['password']


# Function to send SMS using Twilio
def send_sms(message):
    client = Client(get_credentials()['account_sid'], get_credentials()['auth_token'])
    client.messages.create(
        to=get_credentials()['phone_number'],
        from_=get_credentials()['twilio_phone_number'],
        body=message
    )


def get_driver():
    # Set up the options
    options = Options()
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")

    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = uc.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    ua = UserAgent()

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": ua.random})

    return driver


def main():
    while True:
        home_page = "https://visas-fr.tlscontact.com/visa/ma/ma" + get_credentials()['center'] + "2fr/home"
        driver = get_driver()
        driver.get(home_page)
        time.sleep(random.randint(1, 4))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "You have been temporarily blocked to prevent unauthorized use." in body_text:
            print("Your ip is blacklisted. Please try to use your personal hotspot (or try using a VPN)")
            driver.quit()
            break
        try:
            accept_cookies = WebDriverWait(driver, random.randint(20, 25)).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "osano-cm-accept-all")))
            accept_cookies.click()
        except TimeoutException:
            print("Cookies banner not found.")
        try:
            login = WebDriverWait(driver, random.randint(20, 25)).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "LOGIN")))
            login.click()
        except TimeoutException:
            try:
                login = WebDriverWait(driver, random.randint(20, 25)).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "SE CONNECTER")))
                login.click()
            except TimeoutException:
                print("Login button not found.")
        try:
            username = WebDriverWait(driver, random.randint(20, 25)).until(
                EC.presence_of_element_located((By.ID, "username")))
            username.send_keys(email())
        except TimeoutException:
            print("Username field not found.")
        try:
            password_element = driver.find_element(By.ID, "password")
            password_element.send_keys(password())
        except NoSuchElementException:
            print("Password field not found.")
        time.sleep(random.randint(1, 3))
        try:
            submit = driver.find_element(By.ID, "kc-login")
            submit.click()
        except NoSuchElementException:
            print("Submit button not found.")
        time.sleep(random.randint(8, 10))
        try:
            group_page = WebDriverWait(driver, random.randint(20, 25)).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "tls-button-primary")))
            group_page.click()
            time.sleep(random.randint(4, 10))
        except TimeoutException:
            print("Group page button not found.")
        try:
            rdv_pages = WebDriverWait(driver, random.randint(20, 25)).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "button-neo-inside.-primary")))
            try:
                rdv_page = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(rdv_pages[len(rdv_pages)-1]))
                # Scroll to the element if it's outside the viewport
                driver.execute_script("arguments[0].scrollIntoView(true);", rdv_page)
                rdv_page.click()
            except ElementClickInterceptedException:
                print("RDV page button not clickable. Retrying...")
                try:
                    rdv_pages[len(rdv_pages)-1].click()
                except ElementClickInterceptedException:
                    print("RDV page button still not clickable. Restarting...")
                    driver.quit()
                    time.sleep(random.randint(30, 60))
                    continue
        except TimeoutException:
            print("Appointment page button not found")

        while True:
            time.sleep(random.randint(4, 8))
            try:
                no_rdv_button = WebDriverWait(driver, random.randint(25, 30)).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "tls-button-primary")))
                try:
                    no_rdv_button.click()
                except ElementClickInterceptedException:
                    print("RDV page button not clickable. Retrying...")
                    time.sleep(random.randint(30, 60))
                    no_rdv_button.click()
            except TimeoutException:
                try:
                    available_app = WebDriverWait(driver, random.randint(10, 15)).until(EC.presence_of_element_located((By.CLASS_NAME, "tls-time-unit.-available")))
                    playsound('./alert.mp3')
                    send_sms("Alert: Appointment available in " + get_credentials()["center"] + "!")
                    available_app.click()
                    try:
                        confirmation_popup = WebDriverWait(driver, random.randint(10, 15)).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "tls-popup-action")))
                        try:
                            validate_app = WebDriverWait(confirmation_popup, random.randint(20, 25)).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "tls-button-primary.-uppercase")))
                            validate_app.click()
                        except TimeoutException:
                            print("Validate app button not clickable. Retrying...")
                            time.sleep(random.randint(120, 200))
                            validate_app = WebDriverWait(confirmation_popup, random.randint(20, 25)).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "tls-button-primary.-uppercase")))
                            validate_app.click()
                    except TimeoutException:
                        print("Confirmation popup not found.")
                except TimeoutException:
                    try:
                        no_available_app = WebDriverWait(driver, random.randint(1, 3)).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "tls-time-unit.-unavailable")))
                    except TimeoutException:
                        print("Too many refreshes, the bot will restart to prevent ip blacklisting !")
                        break
            time.sleep(random.randint(10, 20))
            driver.refresh()
        driver.quit()
        time.sleep(random.randint(15, 30))
        continue


if __name__ == '__main__':
    main()
