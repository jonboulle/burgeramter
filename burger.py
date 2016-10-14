#!/usr/bin/env python
#
# Try, painfully, to get a Berlin burgeramt appointment.
#
# Inspired by https://gist.github.com/pbock/3ab260f3862c350e6b5f
#

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import subprocess
import sys
import time

DEFAULT_SLEEP = 30 # seconds

URL = 'https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=120686&dienstleisterlist=122210,327316,122217,122219,327312,327314,122227,122231,327346,327423,122243,327348,122252,327338,122260,327340,122262,122254,122271,122273,122277,327294,327290,327292,122291,327270,122285,327266,122286,327264,122296,327268,150230,122301,327282,122297,327286,122294,327284,122312,122314,122304,327330,122311,327334,122309,327332,317869,324433,325341,324434,327352,324414,122283,327354,122276,327324,122274,327326,122267,327328,122246,327318,122251,327320,122257,327322,122208,327298,122226,327300&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F120686%2F'

def notify(message):
    subprocess.call(["i3-nagbar", "-m", message])

def appointment_available(drv):
    print("Looking for appointments...")
    try:
        return drv.find_element_by_class_name('tagesauswahl')
    except NoSuchElementException as err:
        return None

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
    driver.get(URL)
    app_link = appointment_available(driver)
    while not app_link:
        print("- No appointments found, sleeping {0}s...".format(sleep))
        time.sleep(sleep)
        print("Refreshing...")
        driver.refresh()
        app_link = appointment_available(driver)
    link = app_link.get_attribute("href")
    load_link_in_new_tab(driver, link)
    notify("Appointment found!")
    time.sleep(sys.maxint)

if __name__ == "__main__":
    main()
