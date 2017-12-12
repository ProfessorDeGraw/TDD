
from os.path import dirname
from os.path import basename
from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def build_file_name(file, extension):
    return dirname(dirname(file)) + '/screens/' + basename(file) + extension


def take_screen_shot(headless_browser):
    headless_browser.get_screenshot_as_file(build_file_name(__file__, '.png'))


def dump_html(headless_browser):
    with open(build_file_name(__file__, '.html'), 'w') as f:
        f.write(headless_browser.page_source)


display = Display(visible=0, size=(1024, 768))
display.start()

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
# options.binary_location = "/usr/bin/google-chrome"
print('set up driver')
browser = webdriver.Chrome(chrome_options=options)
# driver= webdriver.Firefox()
print('staring driver')

browser.set_window_size(1024, 768)

# > Xvfb :99 -ac -screen 0 1280x1024x24 &
# > export DISPLAY=:99
# > java -jar selenium-server-standalone-3.6.0.jar

browser.get('http://10.0.143.69:3000/')

elem = browser.find_element_by_id('terminal')
elem.send_keys("term")
elem.send_keys(Keys.RETURN)
elem.send_keys("term")
elem.send_keys(Keys.RETURN)
elem.send_keys("ssh nddegraw@10.0.143.69")
elem.send_keys(Keys.RETURN)
elem.send_keys("clear")
elem.send_keys(Keys.RETURN)
sleep(.3)
elem.send_keys("whoami")
elem.send_keys(Keys.RETURN)
elem.send_keys("hostname")
elem.send_keys(Keys.RETURN)
elem.send_keys("nova list")
elem.send_keys(Keys.RETURN)

browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
elem = browser.find_element_by_xpath("/html/body/x-screen/div")
x_row = browser.find_elements_by_xpath("/html/body/x-screen/div/x-row")
tag_output = elem.get_attribute('innerHTML')

# x_row_tags = re.compile("<x-row>*</x-row>")

print(tag_output)
print('=== Command output ====')
line = 1
for x in x_row:
    print('%s: %s' % (line, x.get_attribute('innerHTML')))
    line += 1
print('=======================')

take_screen_shot(browser)
dump_html(browser)

browser.switch_to.default_content()

assert 'localhost' in browser.title

# driver.close() # Close the current window.
browser.quit()  # Quit the driver and close every associated window.
display.stop()
