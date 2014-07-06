import time
from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(FunctionalTest):

    TEST_EMAIL_GMAIL = 'superlists.magitests@gmail.com'
    TEST_EMAIL_MOCKMYID = 'superlists.magitests@mockmyid.com'

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        self.sign_in_mockmyid()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in()

        # Refreshing the page, she sees it's a real session Login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # Terrified of this new feature, she reflexively clicks "logout"
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # The "Logged out" status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out()

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
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was {}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_for_element_by_css_selector(self, selector):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_css_selector(selector),
            'Could not find element with selector {}. Page text was {}'.format(
                selector, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(self.test_email, navbar.text)

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(self.test_email, navbar.text)

    def sign_in_google(self):
        ## Use Gmail for the test email
        self.test_email = self.TEST_EMAIL_GMAIL
        self.provide_email_to_persona_sign_in_page()

        #self.switch_to_new_window('Google')
        self.browser.find_element_by_id('Email').send_keys('superlists.magitests')
        self.browser.find_element_by_id('Passwd').send_keys('wojiushi1ceshi')
        self.browser.find_element_by_id('signIn').click()
        ## Then the user authorize the Persona.org to view the email address
        #self.browser.find_element_by_id('submit_approve_access').click()

    def sign_in_mockmyid(self):
        ## Use mockmyid.com for test email
        self.test_email = self.TEST_EMAIL_MOCKMYID
        self.provide_email_to_persona_sign_in_page()

    def provide_email_to_persona_sign_in_page(self):
        self.browser.find_element_by_id('authentication_email'
        ).send_keys(self.test_email)

        ## Find the button shows for desktop version
        self.wait_for_element_by_css_selector('button.isDesktop')
        self.browser.find_element_by_css_selector('button.isDesktop').click()

