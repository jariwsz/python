from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path='../drivers/geckodriver.exe')
# implicit wait
# driver.implicitly_wait(10)


driver.get("https://www.baidu.com")

driver.find_element_by_id('kw').send_keys("微博")

try:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'su')))
    print('element clickable')
except:
    print('element unclickable')
    exit(1)

element.click()

# driver.find_element_by_id('su').send_keys(Keys.ENTER)

print(driver.title)

driver.close()
driver.quit()