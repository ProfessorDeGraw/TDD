from os.path import basename, dirname, exists
from os import makedirs
import os
from unittest import skip

from pyvirtualdisplay import Display
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 4


class FunctionalTest(StaticLiveServerTestCase):

    def __init__(self, dont_care):
        self.counter = 0
        super(FunctionalTest, self).__init__(dont_care)

    def setUp(self):
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()

        self.set_up_browser()

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

        # How to run in command window
        # > Xvfb :99 -ac -screen 0 1280x1024x24 &
        # > export DISPLAY=:99
        # > java -jar selenium-server-standalone-3.6.0.jar

    def set_up_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # options.binary_location = "/usr/bin/google-chrome"
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

    @staticmethod
    def build_file_name(file, extension, number):
        if not exists(dirname(dirname(file)) + '/screens/'):
            makedirs(dirname(dirname(file)) + '/screens/')

        return dirname(dirname(file)) + '/screens/' + basename(file) + str(number) + extension

    def test_debug_show(self):
        self.counter = self.counter + 1
        self.take_screen_shot(self.counter)
        self.dump_html(self.counter)

    def take_screen_shot(self, number=0):
        self.browser.get_screenshot_as_file(self.build_file_name(__file__, '.png', number))

    def dump_html(self, number):
        with open(self.build_file_name(__file__, '.html', number), 'w') as f:
            f.write(self.browser.page_source)
