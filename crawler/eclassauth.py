# -*- coding: utf-8 -*-
from selenium.common.exceptions import UnexpectedAlertPresentException

from crawler.browser import Browser


class EClass:
    def __init__(self, uid=None, upw=None):
        self.driver = Browser(False)
        self.uid, self.upw = uid, upw

    @property
    def is_logon(self) -> bool:
        try:
            self.driver.get("https://eclass3.cau.ac.kr/")
        except UnexpectedAlertPresentException:
            self.driver.pass_alert(wait_time=0.1)
            self.driver.pass_alert(wait_time=0.1)
            self.driver.pass_alert(wait_time=0.1)
            self.driver.get("https://eclass3.cau.ac.kr/")

        self.driver.wait_state("normal")
        self.driver.wait_state("normal")

        return bool(self.driver.find_one_by_css("#global_nav_profile_link"))

    def login(self, uid=None, upw=None) -> bool:
        # print("Login...", end='')

        self.uid = uid or self.uid
        self.upw = upw or self.upw

        try:
            self.driver.get(
                "https://ocs.cau.ac.kr/index.php?module=xn_sso2013&act=procXn_sso2013LoginGateway&from=web_redirect&login_type=sso&auto_login=true&sso_only=true&callback_url=https%3A%2F%2Feclass3.cau.ac.kr%2F/learningx/login")
        except UnexpectedAlertPresentException:
            self.driver.pass_alert(wait_time=0.1)
            self.driver.pass_alert(wait_time=0.1)
            self.driver.pass_alert(wait_time=0.1)
            self.driver.get(
                "https://ocs.cau.ac.kr/index.php?module=xn_sso2013&act=procXn_sso2013LoginGateway&from=web_redirect&login_type=sso&auto_login=true&sso_only=true&callback_url=https%3A%2F%2Feclass3.cau.ac.kr%2F/learningx/login")

        self.driver.wait_state("normal")
        self.driver.wait_state("normal")

        self.driver.execute_script(f"document.querySelector('#login_user_id').value = '{self.uid}';"
                                   f"document.querySelector('#login_user_password').value = '{self.upw}';")
        self.driver.execute_script(f"xn_content_manager_login_in_custom_mobile_login.login();")

        try:
            self.driver.wait_state("normal")
            self.driver.wait_state("normal")
            self.driver.wait_state("normal")
        except UnexpectedAlertPresentException:
            return False  # 로그인 실패!

        if not self.driver.find_one_by_css("#content"):
            # print("Fail!")
            return False

        # print("Done!")
        return True

    @property
    def auth_cookies(self) -> list:
        return self.driver.all_cookies

    def quit(self):
        self.driver.driver.quit()


if __name__ == '__main__':
    e_class = EClass("eclass id", "eclass pw")
    if e_class.login():
        print(12)
