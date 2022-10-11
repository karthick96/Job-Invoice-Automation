from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# install chrome driver and connect to the chrome browser
#  #Add options inside webdriver.chrome method during deployment
driver = webdriver.Chrome(ChromeDriverManager().install())  # , options=options

try:
    # search the URL in the browser
    driver.get('https://app.poweredbyliquid.com/liquid/home')

    '''wait till the page reloads to the final required login page (finding if it is the final page by checking
    if input id provided in html of the login page is same as expected login page of the site)'''
    try:
        delay = 5  # in seconds
        element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.ID, "1-email")))
        print("login Page is ready!")
    except TimeoutException:
        print("Loading of login page took too much time!")

    time.sleep(3)

    driver.find_element(By.ID,
                        '1-email').send_keys('karthickrajamrita@gmail.com')

    time.sleep(4)

    driver.find_element(By.XPATH,
                        "//input[@type='password' and @name='password' and @class='auth0-lock-input']").send_keys('Sh8zLvCyLBD6ZfK')

    time.sleep(3)

    driver.find_element(By.XPATH,
                        "//button[ @class='auth0-lock-submit' and @name='submit' and @type='submit']").click()
    time.sleep(3)

    try:
        delay = 5  # in seconds
        element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "welcome-message")))
        print("Welcome page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    print("Login Successfull!")

    time.sleep(1)

    # go to invoice tab on the welcome page
    driver.find_element(By.XPATH,
                        "//a[@href='/liquid/invoices']").click()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='mat-focus-indicator mat-menu-trigger no-borders mat-button mat-button-base mat-primary']//span[@class='mat-button-wrapper']")))
        print("Invoice tab is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    # click add invoice button
    element.click()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' For an existing client ')]")))
        print("Invoice button is ready to be clickable!")
    except TimeoutException:
        print("Loading took too much time!")

    # click existing client
    element.click()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@color='primary' and @class='mat-focus-indicator dialog-button mat-flat-button mat-button-base mat-primary']//span[@class='mat-button-wrapper']")))
        print("Create client invoice for a client is selected!")
    except TimeoutException:
        print("Loading took too much time!")

    # click select for a client in create client invoice
    element.click()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        a = ActionChains(driver)
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//span[starts-with(@class, 'mat-select-placeholder mat-select-min-line ng-tns-c111')]")))

        print("click to select the work order is clickable!")
    except TimeoutException:
        print("Loading took too much time!")

    # move the cursor to the position and then click
    a.move_to_element(element).click().perform()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        a = ActionChains(driver)
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='mat-option-text'][1]")))  # ISSUE NEEDS TO BE FIXED!!!

        print("selecting the work order ' Coding Instructor ' is clickable!")
    except TimeoutException:
        print("Loading took too much time!")

    # move the cursor to the position and then click
    a.move_to_element(element).click().perform()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        a = ActionChains(driver)
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' Select ')]")))

        print("select Button is clickable!")
    except TimeoutException:
        print("Loading took too much time!")

    # move the cursor to the position and then click
    a.move_to_element(element).click().perform()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        a = ActionChains(driver)
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' Yes ')]")))

        print("yes Button is clickable!")
    except TimeoutException:
        print("Loading took too much time!")

    # move the cursor to the position and then click
    a.move_to_element(element).click().perform()

    time.sleep(1)

    try:
        delay = 5  # in seconds
        a = ActionChains(driver)
        element = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Time Entry ')]")))

        print("Time entry Button is clickable!")
    except TimeoutException:
        print("Loading took too much time!")

    # move the cursor to the position and then click
    a.move_to_element(element).click().perform()

    time.sleep(5)

except Exception as e:
    print(e)

finally:
    driver.quit()
