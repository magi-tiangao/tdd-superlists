import time
from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait


TEST_EMAIL_GMAIL = 'superlists.magitests@gmail.com'
TEST_EMAIL_MOCKMYID = 'superlists.magitests@mockmyid.com'
TEST_EMAIL = TEST_EMAIL_MOCKMYID


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        self.sign_in_persona()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Refreshing the page, she sees it's a real session Login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Terrified of this new feature, she reflexively clicks "logout"
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(TEST_EMAIL)

        # The "Logged out" status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(TEST_EMAIL)

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

    def sign_in_persona(self):
        if TEST_EMAIL == TEST_EMAIL_MOCKMYID:
            self.sign_in_mockmyid()
        else:
            self.sign_in_google()

    def sign_in_google(self):
        ## Use Gmail for the test email
        self.provide_email_to_persona_sign_in_page()

        #self.switch_to_new_window('Google')
        self.browser.find_element_by_id('Email').send_keys('superlists.magitests')
        self.browser.find_element_by_id('Passwd').send_keys('wojiushi1ceshi')
        self.browser.find_element_by_id('signIn').click()
        ## Then the user authorize the Persona.org to view the email address
        #self.browser.find_element_by_id('submit_approve_access').click()

    def sign_in_mockmyid(self):
        ## Use mockmyid.com for test email
        self.provide_email_to_persona_sign_in_page()

    def provide_email_to_persona_sign_in_page(self):
        self.browser.find_element_by_id('authentication_email'
        ).send_keys(TEST_EMAIL)

        ## Find the button shows for desktop version
        #self.wait_for_element_by_css_selector('button.isDesktop')
        time.sleep(1)
        self.browser.find_element_by_css_selector('button.isDesktop').click()

