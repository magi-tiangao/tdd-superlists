import time
from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(FunctionalTest):

    TEST_EMAIL_GMAIL = 'superlists.magitests@gmail.com'
    TEST_EMAIL_MOCKMYID = 'superlists.magitests@mockmyid.com'

    def sign_in_google(self):
        self.browser.find_element_by_id('authentication_email'
        ).send_keys('superlists.magitests@gmail.com')
        ## Find the button shows for desktop version
        self.browser.find_element_by_css_selector('button.isDesktop').click()
        #self.switch_to_new_window('Google')
        self.browser.find_element_by_id('Email').send_keys('superlists.magitests')
        self.browser.find_element_by_id('Passwd').send_keys('wojiushi1ceshi')
        self.browser.find_element_by_id('signIn').click()
        ## Then the user authorize the Persona.org to view the email address
        #self.browser.find_element_by_id('submit_approve_access').click()

    def sign_in_mockmyid(self):
        ## Use mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email'
        ).send_keys('superlists.magitests@mockmyid.com')
        ## Find the button shows for desktop version
        self.browser.find_element_by_css_selector('button.isDesktop').click()

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        self.sign_in_google()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('superlists.magitests@gmail.com', navbar.text)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )