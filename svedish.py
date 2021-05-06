#!/usr/bin/env python
#
# Try, painfully, to get a svedish embassy appointment
#

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import subprocess
import sys
import time

DEFAULT_SLEEP = 5 # seconds

URL = 'https://www.migrationsverket.se/ansokanbokning/valjtyp?0&enhet=U0586&sprak=en&callback=https:/www.swedenabroad.se'

def notify(message):
    subprocess.call(["i3-nagbar", "-m", message])

def appointment_available(drv):
    print("Looking for appointments...")

    drv.get(URL)

    reason_for_appointment = drv.find_element_by_id("viseringstyp")
    Select(reason_for_appointment).select_by_value('6')

    # wait for number selector to show up
    time.sleep(1)
    
    number_of_persons = drv.find_element_by_id("antalpersoner")
    Select(number_of_persons).select_by_value('0')

    time.sleep(1)
    drv.find_element_by_name("fortsatt").click()

    time.sleep(1)
    try:
        error_box = drv.find_element_by_class_name("feedbackPanelERROR")
    except NoSuchElementException as err:
        return True
    print(error_box.text)
    return False


def load_link_in_new_tab(drv, url):
    drv.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
    drv.execute_script('window.open("{}", "_blank");'.format(url))
    drv.switch_to_window(drv.window_handles[1])

def main():
    try:
        sleep = int(sys.argv[1])
    except IndexError:
        sleep = DEFAULT_SLEEP
    except ValueError:
        print("Usage: {} [sleep_seconds]".format(sys.argv[0]))
        sys.exit(1)

    print("Loading Chrome...")
    driver = webdriver.Chrome()
    app_link = appointment_available(driver)
    while not app_link:
        print("- No appointments found, sleeping {0}s...".format(sleep))
        time.sleep(sleep)
        print("Refreshing...")
        driver.refresh()
        app_link = appointment_available(driver)
#    link = app_link.get_attribute("href")
#    load_link_in_new_tab(driver, link)
    notify("Appointment found!")
    time.sleep(sys.maxint)

if __name__ == "__main__":
    main()
