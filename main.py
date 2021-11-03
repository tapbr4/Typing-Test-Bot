from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import config


# Launch Microsoft Edge (Chromium)
options = EdgeOptions()
options.use_chromium = True
if config.setup.get('start_maximized'): options.add_argument("--start-maximized")
driver = Edge(options=options, executable_path='msedgedriver.exe')

# Login
if(config.login.get('login')):
    driver.get('https://10fastfingers.com/login')
    email = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'UserEmail')))
    email.send_keys(config.login.get('email'))
    driver.find_element(By.ID, 'UserPassword').send_keys(config.login.get('password'))
    driver.find_element(By.ID, 'login-form-submit').click()

# Goes to the typing test page with the given language
driver.get('https://10fastfingers.com/typing-test/{}'.format(config.setup.get('language')))

# Allow all/necessary Cookies
wait_details = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyEdgeMoreDetailsLink')))
if config.setup.get('cookies'):
    allow_all = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection')
    driver.execute_script("arguments[0].click();", allow_all)
else:
    preferences = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonPreferences')
    driver.execute_script("arguments[0].click();", preferences)
    statistics = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonStatistics')
    driver.execute_script("arguments[0].click();", statistics)
    marketing = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonMarketing')
    driver.execute_script("arguments[0].click();", marketing)
    decline = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyButtonDecline')))
    driver.execute_script("arguments[0].click();", decline)

# Wait until the input field is available
inputfield = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'inputfield')))

# Wait until words are available
words = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'highlight')))

# 356 available words
for i in range(356):
    words = driver.find_element(By.CLASS_NAME, 'highlight')
    # Writing
    for char in words.text:
        driver.find_element(By.ID, 'inputfield').send_keys(char)
        sleep(config.setup.get('delay')) # Delay in seconds for each character
    driver.find_element(By.ID, 'inputfield').send_keys(Keys.SPACE)
