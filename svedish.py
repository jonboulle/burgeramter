#!/usr/bin/env python
#
# Try, painfully, to get a svedish embassy appointment
#

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import sys
import time

DEFAULT_SLEEP = 5 # seconds

URL = 'https://www.migrationsverket.se/ansokanbokning/valjtyp?0&enhet=U0586&sprak=en&callback=https:/www.swedenabroad.se'

def notify(message):
    print("????? do something here")

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
    while not appointment_available(driver):
        print("- No appointments found, sleeping {0}s...".format(sleep))
        time.sleep(sleep)
        print("Refreshing...")
        driver.refresh()
    notify("Appointment found!")
    time.sleep(sys.maxint)

if __name__ == "__main__":
    main()
