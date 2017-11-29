from pyvirtualdisplay import Display
from selenium import webdriver


def take_screen_shot(headless_browser):
    filename = __file__ + '.png'
    print('screenshotting to', filename)
    headless_browser.get_screenshot_as_file(filename)


def dump_html(headless_browser):
    filename = __file__ + '.html'
    print('dumping page HTML to', filename)
    with open(filename, 'w') as f:
        f.write(headless_browser.page_source)


display = Display(visible=0, size=(1024, 768))
display.start()

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
#options.binary_location = "/usr/bin/google-chrome"
print('set up driver')
browser = webdriver.Chrome(chrome_options=options)
#driver= webdriver.Firefox()
print('staring driver')

browser.set_window_size(1024, 768)

# > Xvfb :99 -ac -screen 0 1280x1024x24 &
# > export DISPLAY=:99
# > java -jar selenium-server-standalone-3.6.0.jar

browser.get('http://localhost:8000')

take_screen_shot(browser)
dump_html(browser)

assert 'Django' in browser.title

# driver.close() # Close the current window.
browser.quit() # Quit the driver and close every associated window.
display.stop()
