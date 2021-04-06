# -*- coding: utf-8 -*-

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Browser:
    def __init__(self, has_screen=True):
        service_args = ["--ignore-ssl-errors=true"]
        options = Options()
        if not has_screen:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")

        # 우회 관련 옵션
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            executable_path="chromedriver.exe",
            service_args=service_args,
            options=options,
        )
        self.driver.implicitly_wait(3)

    @property
    def all_cookies(self):
        return self.driver.get_cookies()

    def get(self, url):
        self.driver.get(url)

    def wait_state(self, state, wait=0.3):
        if state == 'normal':
            # normal 수준의 로딩 wait
            while self.driver.execute_script('return document.readyState;') != 'complete':
                time.sleep(wait)

    def find_one_by_css(self, css_selector, elem=None, wait_time=3):
        obj = elem or self.driver

        try:
            if wait_time:
                WebDriverWait(obj, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )

            res_elem = obj.find_element(By.CSS_SELECTOR, css_selector)
            return res_elem
        except TimeoutException:
            return None
        except NoSuchElementException:
            return None

    def pass_alert(self, wait_time=1):
        try:
            WebDriverWait(self.driver, wait_time).until(EC.alert_is_present(), '')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass

    def execute_script(self, script, args=None):
        if args:
            return self.driver.execute_script(script, args)
        else:
            return self.driver.execute_script(script)

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass


if __name__ == '__main__':
    driver = Browser()
    input(1)
