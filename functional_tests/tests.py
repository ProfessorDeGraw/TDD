from os.path import basename, dirname

from pyvirtualdisplay import Display
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 4


def build_file_name(file, extension, number):
    return dirname(dirname(file)) + '/screens/' + basename(file) + str(number) + extension


def take_screen_shot(headless_browser, number=0):
    headless_browser.get_screenshot_as_file(build_file_name(__file__, '.png', number))


def dump_html(headless_browser, number):
    with open(build_file_name(__file__, '.html', number), 'w') as f:
        f.write(headless_browser.page_source)


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()

        self.set_up_browser()

        # How to run in command window
        # > Xvfb :99 -ac -screen 0 1280x1024x24 &
        # > export DISPLAY=:99
        # > java -jar selenium-server-standalone-3.6.0.jar

    def set_up_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # options.binary_location = "/usr/bin/google-chrome"
        print('set up driver')
        self.browser = webdriver.Chrome(chrome_options=options)
        # self.browser = webdriver.Firefox()
        self.browser.set_window_size(1024, 768)

    def tearDown(self):
        # driver.close() # Close the current window.
        self.browser.quit()  # Quit the driver and close every associated window.
        self.display.stop()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        take_screen_shot(self.browser, 0)
        dump_html(self.browser, 0)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title, "Is the server running? try:\npython manage.py runserver")

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        take_screen_shot(self.browser, 1)
        dump_html(self.browser, 1)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')

        take_screen_shot(self.browser, 2)
        dump_html(self.browser, 2)

        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        take_screen_shot(self.browser, 3)
        dump_html(self.browser, 3)

        # Satisfied, she goes back to sleep

    def test_muliple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)

        take_screen_shot(self.browser, 4)
        dump_html(self.browser, 4)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')

        take_screen_shot(self.browser, 5)
        dump_html(self.browser, 5)

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        take_screen_shot(self.browser, 6)
        dump_html(self.browser, 6)

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        # # We use a new browser session to make sure that no information
        # # of Edith's is coming through from cookies etc
        self.browser.quit()
        self.set_up_browser()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)

        take_screen_shot(self.browser, 7)
        dump_html(self.browser, 7)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')

        take_screen_shot(self.browser, 8)
        dump_html(self.browser, 8)

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        take_screen_shot(self.browser, 9)
        dump_html(self.browser, 9)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
