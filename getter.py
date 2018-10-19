"""Get ingredients and equipment from the ChefSteps recipes."""
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

driver = webdriver.Chrome('chromedriver', chrome_options=options)
# give it a really long potential timeout in case something strange happens
driver.implicitly_wait(10)  # seconds


def sanitise_string(s):
    """Remove chars that will mess with the CSV spec."""
    s = s.replace("µm", "nanometer")
    s = s.replace("\"", "″")
    s = s.replace(",", "|comma|")
    return s


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
    time.sleep(1)
    fields[1].send_keys(Keys.ENTER)
    # print("entered", username, password)
    # driver.find_element_by_css_selector("button.modal-submit").click()
    time.sleep(5)
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
    return sanitise_string(name.text)


def get_it(selector):
    """Get list of things and format for csv."""
    list_things = driver.find_elements_by_css_selector(selector)

    row = ""
    if list_things:
        for lt in list_things:
            row += make_cell(lt) + ","

    return row


def get_title():
    time.sleep(4) # nasty
    title = driver.find_elements_by_css_selector('.hero-text h1')
    title = list(set([e.text for e in title]))[0]
    title = sanitise_string(title)
    return title


def prep_files(equipment_file_path, ingredients_file_path):
    with open(equipment_file_path, "w") as equipment_file:
        with open(ingredients_file_path, "w") as ingredient_file:
            equipment_file.write("title, equipment...\n")
            ingredient_file.write("title, ingredient...\n")


equipment_file_path = "temp_equipment.csv"
ingredients_file_path = "temp_ingredients.csv"

prep_files("temp_equipment.csv", "temp_ingredients.csv")

login("../chefstepsLogin")


for urlBit in content[44:]:
    with open(equipment_file_path, "a") as equipment_file:
        with open(ingredients_file_path, "a") as ingredient_file:
            with open("failures.txt", "a") as failure_file:
                try:
                    driver.get('https://www.chefsteps.com/activities/'+urlBit)
                    time.sleep(3)

                    # get the title of the page
                    title = get_title()
                    row_head = "{u},{t}".format(u=urlBit, t=title)

                    ingredients = get_it(" ".join(['.ingredients-wrapper',
                                                'cs-ingredients',
                                                'cs-ingredient',
                                                '.ingredient-title-desc']))
                    i_row = "{h},{i}\n".format(h=row_head, 
                                               i=ingredients)
                    ingredient_file.write(i_row)

                    equipment = get_it('.activity-amounts-equipment div')
                    e_row = "{h},{e}\n".format(h=row_head, 
                                               e=equipment)
                    equipment_file.write(e_row)

                    print("{t} - {u}".format(t=title, u=urlBit))
                    print("i_row", i_row)
                    print("e_row", e_row, "\n")

                    equipment_file.close()
                    ingredient_file.close()
                except Exception as e:
                    f = '{"e":{e}, "page": {urlBit}}'.format(e=e, page=urlBit)
                    failure_file.write(f)

driver.quit()

print("\nDONE!!\n")
