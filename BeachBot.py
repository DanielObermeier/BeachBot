#!python3

# import libraries 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import os.path
import time
import datetime
from datetime import timedelta

# Function to initiate the webdriver (headless)
def init_webdriver_headless():
    """ this function initiates the webdriver using the chromedriver.exe located in the directory in headless mode and returns a driver object"""

    #import selenium
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    import os

    # get path of webdriver
    #chrome_driver = os.getcwd() +"\\chromedriver.exe"
    my_path = os.path.abspath(os.path.dirname(__file__))
    chrome_driver = my_path+ "\chromedriver.exe"
        # set options of webdriver to headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
        # set screensize to 2560x1440
    chrome_options.add_argument("--window-size=2560x1440")

    # init webdriver with options
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

    # return webdriver object
    return driver



# Function to Initiate the webdriver (normally)
def init_webdriver():
    """ this function initiates the webdriver using the chromedriver.exe located in the directory and returns a driver object"""

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    driver = webdriver.Chrome("C:/Users/danie/OneDrive/Dokumente/Coding/SideProjects/BeachBot/chromedriver.exe")
    driver.maximize_window()
    #driver.set_window_size(2560, 1440)

    return driver

# Function to end the webdriver session
def quit_webdriver(driver):
    """ this function quits the webdriver session"""
    driver.quit()


# Booking function 
def book_court(driver, username, pswd):
    """This function takes three arguments and proceeds in two steps. 
        First, it logs into the booking page. 
        Second, it loops through a preference list and tries to book a court. 
        If a court is successfully booked it confirms the booking to the user.

        This function returns a message list that is logged in a file.
        
        Arguments:
        driver = webdriver object
        username = string 
        pswd = string
        """

    #import selenium
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    import time

    # init message list that is logged later

    message_list = []

    """ 1. the webdriver navigates to the booking page and logs in first"""
    # navigate webdriver the court booking webpage
    while True:
        try:
            driver.get("https://ssl.forumedia.eu/zhs-courtbuchung.de/")
        except:
            message_list.append("webdriver failure - webdriver could not access website")
            break

        # navigate to login page
        try:
            driver.find_element_by_xpath('//*[@id="login_block"]').click()
        except: 
            message_list.append("webdriver could not find login page")
            break
        

        # insert user name
        try:
            
            login_username = driver.find_element_by_css_selector('#login')
            login_username.send_keys(username)
        except:
            message_list.append("webdriver could not insert username")
            break

        # test insert password
        try:
            
            login_password = driver.find_element_by_css_selector('#password')
            login_password.send_keys(pswd)
        except:
            message_list.append("webdriver could not insert password")
            break


        # submit login 
        try:
            driver.find_element_by_xpath("//input[@type='submit']").click()
        except: 
            message_list.append("webdriver could not submit login data")
            break




        """ 2. Try to book courts according to a preference list"""
        # nested preference list of courts 
            # format pref_list = [["court number","order_element","booking_element"],[...],[...]]
        pref_list = [["5","26","5"],["6","27","6"],["7","28","7"],["1","22","1"],["2","23","2"],["3","24","3"],["4","25","4"],["8","51","1"],["9","52","2"],["10","53","3"],["11","54","4"],["12","55","5"],["13","56","6"]] 

        # books court at newly added day
        date = str(datetime.date.today() + timedelta(days=8))

        # navigate webdriver to booking page of a given day (court 1 - 7) 
        booking_url = "https://ssl.forumedia.eu/zhs-courtbuchung.de/reservations.php?action=showRevervations&type_id=2&date="+date+"&page="
        
        page = 1
        
        try:
            driver.get(booking_url+str(page))
        except:
            message_list.append("webdriver failure, driver was not able to access booking website")
            break

        try:
            # scroll down to clickable booking slot
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="areas-content-block"]/table/tbody/tr/td[1]/form/div/input'))
        except:
            message_list.append("webdriver could not scroll to booking elements")

        # initiate iterator
        i = 0 

        while i <= 6:
            try: 
                # try to tick two consecutive 1h slots
                driver.find_element_by_css_selector('#order_el_'+pref_list[i][1]+'_18\:00').click()
                driver.find_element_by_css_selector('#order_el_'+pref_list[i][1]+'_19\:00').click()

                # scroll down to submission button
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="areas-content-block"]/table/tbody/tr/td['+pref_list[i][2]+']/form/div/input')) 

                # submit selection
                driver.find_element_by_xpath('//*[@id="areas-content-block"]/table/tbody/tr/td['+pref_list[i][2]+']/form/div/input').click()

                # scroll down to booking confirmation button
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="main-content-tabs"]/form/div/input')) 
                
                # confirm booking 
                driver.find_element_by_xpath('//*[@id="main-content-tabs"]/form/div/input').click()

                # confirm booking to user
                message = "court " + pref_list[i][0] + "has been booked for you!"
                message_list.append(message)
                i = 13
                break
                
            except:
                message = "\nnot able to book court:" + str(pref_list[i][0])
                message_list.append(message)
                

            #increment i and repeat
            i += 1



        # navigate webdriver to booking page of a given day (court 8 - 13) 
        page = 2 # court 8 - 13 listed at another subpage with different time slots

        try:
            driver.get(booking_url+str(page))
        except:
            message_list.append("webdriver failure, driver was not able to access booking website")

        try:
            # scroll down to clickable booking slot
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="areas-content-block"]/table/tbody/tr/td[1]/form/div/input'))
        except:
            message_list.append("webdriver could not scroll to booking elements")

        while i <= 12:
            try: 
                
                # try to tick two consecutive 1h slots
                driver.find_element_by_css_selector('#order_el_'+pref_list[i][1]+'_18\:30').click()
                driver.find_element_by_css_selector('#order_el_'+pref_list[i][1]+'_19\:30').click()

                # scroll down to submission button
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="areas-content-block"]/table/tbody/tr/td['+pref_list[i][2]+']/form/div/input'))                

                # submit selection
                driver.find_element_by_xpath('//*[@id="areas-content-block"]/table/tbody/tr/td['+pref_list[i][2]+']/form/div/input').click()

                # scroll down to booking confirmation button
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="main-content-tabs"]/form/div/input')) 
                
                # confirm booking 
                driver.find_element_by_xpath('//*[@id="main-content-tabs"]/form/div/input').click()

                # confirm booking to user
                message = "\ncourt " + pref_list[i][0]+" has been booked for you!"
                message_list.append(message)
                i = 13
                break
                
            except:
                message = "\nnot able to book court: " + pref_list[i][0]
                message_list.append(message)

            #increment i and repeat
            i += 1
        
        
        break
    message_list.append("\nbooking is completed")

    return message_list




def main():
    today = datetime.date.today().weekday()
    log_location = "beachbot_log.txt"

    """my_path = os.path.abspath(os.path.dirname(__file__))
    f=open(my_path+ "\login.txt","r")
    lines=f.readlines()
    username=lines[0]
    pswd=lines[1]
    f.close()"""

    # the conditional makes sure that the bot only books on Tue and Thur. Monday is 0 and Wednesday 2 two but the bot has to run at 23:59:58 as it takes two seconds to load the webpage
    if today == 0 or today == 2:        

        username = "username" # load from environment
        pswd = 'password' # load from environment

        driver = init_webdriver() # normal webdriver
        #driver = init_webdriver_headless() #headless webdriver 
        message_list = book_court(driver, username, pswd)
        quit_webdriver(driver)


        text_file = open(log_location, "a")

        message = "\n\n"+ str(datetime.date.today()) +  ": Tryed to book today, Sir!"
        m = text_file.write(message)

        for message in message_list:
            n = text_file.write(message)
        text_file.close()
    else: 
        text_file = open(log_location, "a")

        message = "\n\n"+ str(datetime.date.today()) +  ": No Tue/Thur...no booking today, Sir!"
        m = text_file.write(message)

if __name__ == "__main__":
    main()