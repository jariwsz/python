import unittest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import HtmlTestRunner


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        cls.driver = webdriver.Firefox(executable_path='../drivers/geckodriver.exe', options=firefox_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    def testSearch(self):
        self.driver.get("http://www.baidu.com")
        self.driver.find_element_by_id('kw').send_keys("微博")
        self.driver.find_element_by_id('su').send_keys(Keys.ENTER)
        print(self.driver.title)

    @unittest.skip('this is a skipped test')
    def skiptest(self):
        '''this is a skipped test'''

if __name__ == '__main__':
    # unittest.main(verbosity=2, testRunner=HtmlTestRunner.HTMLTestRunner(output="D:/temp/test"))
    unittest.main(verbosity=2)
