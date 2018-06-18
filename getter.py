from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import time


# Get the updated version of this by scrolling all the way to the
# bottom of the recipes page: https://www.chefsteps.com/gallery
# then running the following js in the console. It'll copy the result
# to the clipboard.
#
# var urls = [];
# document.querySelectorAll("matrix-item-card a").forEach(function(element) {
#     urls.push(element.href.split("/")[4]);
# });
# copy(urls);
content = json.load(open("newURLs.json"))
# print(content)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome('../chromedriver', chrome_options=options)
# give it a really long potential timeout in case something strange happens
driver.implicitly_wait(10)  # seconds


def login(credentials_path):
    """Log into the chefsteps site.

    This allows access to premium recipes.
    Read the credentials from a file.
    It's formatted as
    username
    password
    so [0] is the username and [1] is the password.
    """
    with open(credentials_path) as f:
        credentials = f.readlines()
    username, password = credentials[0], credentials[1]
    driver.get('https://www.chefsteps.com')
    driver.find_element_by_id("nav-login").click()
    fields = driver.find_elements_by_css_selector(".login-form input")
    fields[0].send_keys(username)
    fields[1].send_keys(password)
    print("entered", username, password)
    # time.sleep(1)
    # driver.find_element_by_css_selector("button.modal-submit").click()
    time.sleep(3)
    # print(driver.title)
    # assert 'Home' in driver.title


def make_cell(element):
    """TODO: work out what this function does."""
    driver.implicitly_wait(0)

    try:
        name = element.find_element_by_tag_name('a')
    except:
        name = element

    driver.implicitly_wait(90)
    return name.text.replace(",", "|comma|")


def get_it(selector):
    """Get list of things and format for csv."""
    list_things = driver.find_elements_by_css_selector(selector)

    row = ""
    if list_things:
        for lt in list_things:
            row += make_cell(lt) + ","

    return row


with open("equipment.csv", "w") as equipment_file:
    with open("ingredients.csv", "w") as ingredient_file:
        equipment_file.write("title, equipment...\n")
        ingredient_file.write("title, ingredient...\n")

login("../chefstepsLogin")

for urlBit in content:
    with open("equipment.csv", "a") as equipment_file:
        with open("ingredients.csv", "a") as ingredient_file:
            driver.get('https://www.chefsteps.com/activities/'+urlBit)
            time.sleep(3)

            # get the title of the page
            title = driver.find_elements_by_css_selector('h1')[0].text
            title = title.replace(",", "|comma|")

            ingredients = get_it(" ".join(['.ingredients-wrapper',
                                           'cs-ingredients',
                                           'cs-ingredient',
                                           '.ingredient-title-desc']))
            i_row = "{t},{i}\n".format(t=title, i=ingredients)
            ingredient_file.write(i_row)

            equipment = get_it('.activity-amounts-equipment div')
            e_row = "{t},{e}\n".format(t=title, e=equipment)
            equipment_file.write(e_row)

            print("i_row", i_row)
            print("e_row", e_row)

            equipment_file.close()
            ingredient_file.close()

driver.quit()

print("\nDONE!!\n")
