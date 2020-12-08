from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which


firefox_options = Options()
# firefox_options.add_argument("--headless")
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
print(driver.title)

driver.set_page_load_timeout(10)
driver.get('https://www.baidu.com')

driver.find_element_by_id('kw').send_keys("微博")
# driver.find_element_by_id('su').click()
driver.find_element_by_id('su').send_keys(Keys.ENTER)
print(driver.title)

time.sleep(2)

driver.close()
driver.quit()

print('Test Complete.')