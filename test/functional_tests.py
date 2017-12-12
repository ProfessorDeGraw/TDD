import time
from pyvirtualdisplay import Display
from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


def take_screen_shot(headless_browser):
    filename = __file__ + '.png'
    print('screenshotting to', filename)
    headless_browser.get_screenshot_as_file(filename)


def dump_html(headless_browser):
    filename = __file__ + '.html'
    print('dumping page HTML to', filename)
    with open(filename, 'w') as f:
        f.write(headless_browser.page_source)


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # options.binary_location = "/usr/bin/google-chrome"
        print('set up driver')
        self.browser = webdriver.Chrome(chrome_options=options)
        # self.browser = webdriver.Firefox()

        self.browser.set_window_size(1024, 768)

        # How to run in command window
        # > Xvfb :99 -ac -screen 0 1280x1024x24 &
        # > export DISPLAY=:99
        # > java -jar selenium-server-standalone-3.6.0.jar

    def tearDown(self):
        # driver.close() # Close the current window.
        self.browser.quit()  # Quit the driver and close every associated window.
        self.display.stop()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        take_screen_shot(self.browser)
        dump_html(self.browser)

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

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
