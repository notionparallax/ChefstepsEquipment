from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

import time

with open("chefstepsURLS") as f:
    content = f.readlines()


ff = webdriver.Firefox()
ff.implicitly_wait(90) # seconds # give it a really long potential timeout in case something strange happens

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
 
login("your@email.address", "yourPassword")

with open("eq.csv", "a") as myfile:
    myfile.write("title, equiptment...\n")
    for urlBit in content:
        row = ""
        ff.get('https://www.chefsteps.com/activities/'+urlBit)
        # assert 'Recipe | ChefSteps' in ff.title
        time.sleep(3)
        title      = ff.find_elements_by_css_selector('h1')[0]
        equiptment = ff.find_elements_by_css_selector('.activity-amounts-equipment div')  
        
        row += ( title.text.encode('ascii', 'ignore') + ",")
        
        for e in equiptment:
            row += ( e.text.encode('ascii', 'ignore') + ",")
        
    	myfile.write(row + "\n")
        print row

ff.quit()