from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

import time

with open("login") as f:
    credentials = f.readlines()

with open("chefstepsURLS") as f:
    content = f.readlines()


ff = webdriver.Firefox()
ff.implicitly_wait(10) # seconds # give it a really long potential timeout in case something strange happens


def login(username, password):
    ff.get('https://www.chefsteps.com')
    ff.find_element_by_id("nav-login").click()
    fields = ff.find_elements_by_css_selector(".login-form input")
    fields[0].send_keys(username)
    fields[1].send_keys(password)
    print "entered", username, password
    time.sleep(1)
    ff.find_element_by_css_selector("button.modal-submit").click()
    time.sleep(3)
    assert 'Home' in ff.title


def make_cell(element):
    ff.implicitly_wait(0)

    try:
        name = element.find_element_by_tag_name('a'   ).text.encode('ascii', 'ignore')
    except:
        name = element.text.encode('ascii', 'ignore')

    # try:
    #     comments = element.find_element_by_tag_name('span').text.encode('ascii', 'ignore')
    # except:
    #     comments = ""
    ff.implicitly_wait(90)

    return name.replace(",", "|comma|")#, comments.replace(",", "|comma|")


def get_it(selector):
    row = ""
    list_things = ff.find_elements_by_css_selector(selector)

    if list_things:
        for lt in list_things:
            row += make_cell(lt)+","

    return row


login(credentials[0], credentials[1])

with open("equipment.csv", "w") as equipment_file, open("ingredients.csv", "w") as ingredient_file:
    equipment_file.write("title, equipment...\n")
    for urlBit in content:
        ff.get('https://www.chefsteps.com/activities/'+urlBit)
        # assert 'Recipe | ChefSteps' in ff.title
        time.sleep(3)

        # get the title of the page
        title = ff.find_elements_by_css_selector('h1')[0].text.encode('ascii', 'ignore')
        title = title.replace(",", "|comma|")

        i_row = title + "," + get_it('.ingredients-wrapper .ingredient-title-desc') + "\n" # ingredients
        e_row = title + "," + get_it('.activity-amounts-equipment div')             + "\n" # equipment
        equipment_file.write(  e_row)
        ingredient_file.write( i_row)
        print "\n", title
        print i_row
        print e_row

equipment_file.close()
ingredient_file.close()
ff.quit()
