""" Selenium tests for Sciebo
Author: Richard Freitag <freitag@sunet.se>
Selenium tests to log on to the Sciebo test node, performing various operations to ensure basic operation
"""
import xmlrunner
import unittest
import sunetdrive
from webdav3.client import Client

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from datetime import datetime

# 'prod' for production environment, 'test' for test environment
g_testtarget = os.environ.get('DriveTestTarget')
g_sciebourl = 'https://sns-testing.sciebo.de'
g_driverTimeout = 30

class TestSciebo(unittest.TestCase):
    def test_sciebo_login(self):
        drv = sunetdrive.TestTarget(g_testtarget)
        loginurl = g_sciebourl
        print("Login url: ", loginurl)
        sciebouserenv = "SCIEBO_USER"
        sciebouser = os.environ.get(sciebouserenv)
        sciebopwdenv = "SCIEBO_USER_PASSWORD"
        nodepwd = os.environ.get(sciebopwdenv)
        
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
        except:
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options)
        driver.maximize_window()
        # driver2 = webdriver.Firefox()
        driver.get(loginurl)

        wait = WebDriverWait(driver, g_driverTimeout)
        wait.until(EC.presence_of_element_located((By.ID, 'user'))).send_keys(sciebouser)
        wait.until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(nodepwd + Keys.ENTER)

        try:
            myElem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'All files')))
            print("All files visible!")
        except TimeoutException:
            print("Loading of all files took too much time!")

        time.sleep(1)

    def test_sciebo_rds_project(self):
        drv = sunetdrive.TestTarget(g_testtarget)
        loginurl = g_sciebourl
        print("Login url: ", loginurl)
        sciebouserenv = "SCIEBO_USER"
        sciebouser = os.environ.get(sciebouserenv)
        sciebopwdenv = "SCIEBO_USER_PASSWORD"
        nodepwd = os.environ.get(sciebopwdenv)
        
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
        except:
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options)
        driver.maximize_window()
        # driver2 = webdriver.Firefox()
        driver.get(loginurl)

        wait = WebDriverWait(driver, g_driverTimeout)
        wait.until(EC.presence_of_element_located((By.ID, 'user'))).send_keys(sciebouser)
        wait.until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(nodepwd + Keys.ENTER)

        try:
            myElem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'All files')))
            print("All files visible!")
        except TimeoutException:
            print("Loading of all files took too much time!")

        burgerButton = driver.find_element(by=By.CLASS_NAME, value='burger')
        burgerButton.click()

        time.sleep(1)

        rdsAppButton = driver.find_element(by=By.XPATH, value='//a[@href="'+ '/apps/rds/' +'"]')
        rdsAppButton.click()
        time.sleep(1)
        
        try:
            print("Waiting for rds frame")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "rds-editor")))
            print("RDS iframe loaded")
        except:
            print("RDS iframe not loaded")

        # WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, ''))).click()

        # Projects
        # print(driver.find_element(by=By.XPATH, value='//*[@id="inspire"]/div/main/div/div/main/div/div/div[2]/div[2]/div[2]/div/div[2]/div/button/span/span[contains(text(),\'Connect\')]'))
        # /html/body/div/div/div/nav/div[1]/div[2]/div/a[2]/div[2]/div[contains(text(),\'Projects\')]
        print("Select projects from menu")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/nav/div[1]/div[2]/div/a[2]/div[2]/div[contains(text(),\'Projects\')]'))).click()

        # New project
        # /html/body/div/div/div/main/div/div/main/div/div/div/div[1]/div[3]/button/span
        print("New project")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div/div[1]/div[3]/button/span'))).click()

        # Pick folder
        # /html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/button/span
        print("Click on pick folder")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/button/span'))).click()

        # Folder RDSTest
        # /html/body/div[5]/div[1]/ul/li[2]/div/span[1][contains(text(),\'RDSTest\')]
        
        time.sleep(3)

        # Span class is called 'filename'

        # folderPickerFrame = driver.find_element(By.XPATH, '//iframe[1]')
        # driver.switch_to.frame(folderPickerFrame)

        # We need to switch to the parent frame to use RDS here
        print("Switch to parent frame")
        driver.switch_to.parent_frame() 
        print("Wait for folder RDSTest to be visible")
        WebDriverWait(driver, g_driverTimeout).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "oc-dialog-title"), "Choose source folder"))
        print("Visible!")

        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/ul/li[2]/div/span[1]')))
        print("Select folder RDSTest")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[1]/ul/li[2]/div/span[1]'))).click()
        print("Choose folder")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/button'))).click()

        print("Switch back to RDS frame")
        try:
            print("Waiting for rds frame")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "rds-editor")))
            print("RDS iframe loaded")
        except:
            print("RDS iframe not loaded")

        # Input field always has a random ID
        # //*[@id="input-101"]
        # WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        print("Input project name")

        # projectInput = driver.find_element(By.XPATH, "//*[contains(@id, 'input-')]")
        # print(projectInput)
        # print("Here...")

        tsProject = "Test Project - " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'input-')]"))).send_keys(tsProject)

        # OSF repository
        print("Select OSF to publish")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[4]/div/div/div[2]/div[3]/div/div/div/div[3]'))).click()

        # Continue button
        print("Continue")
        # /html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[3]/div/div/button/span
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[3]/div/div/button/span'))).click()

        print("Switch back to Describo frame")
        try:
            print("Waiting for describo frame")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "describoWindow")))
            print("Describo iframe loaded")
        except:
            print("Describo iframe not loaded")
        time.sleep(3)

        # OSF Settings
        print("Wait for OSF Settings and click")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"tab-OSF settings\"]/span"))).click()
        time.sleep(1)

        # Check if we have to delete entries:
        checkForOsfEntries = True
        while checkForOsfEntries == True:
            try:
                deleteButton = driver.find_element(by=By.CLASS_NAME, value='el-button--danger')
                deleteButton.click()
                print("Deleting existing entries")
                time.sleep(1)
            except:
                print("No more entries to delete, continue")
                checkForOsfEntries = False

        # OSF Text
        # /html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/div/button/span
        print("Click on +Text")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pane-OSF settings"]/div/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/div/button/span'))).click()

        # OSF Add Text, again random number ID
        print("Add OSF Title")
        # wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'el-id-')]"))).send_keys("OSF Title")

        tsTitle = "RDS Test Title - " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add text']"))).send_keys(tsTitle + Keys.ENTER)
        # //*[@id="el-id-4106-2"]
        # WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="el-id-2110-7"]'))).click()

        time.sleep(3)

        print("Click on +Select for Osfcategory")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"pane-OSF settings\"]/div/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/button/span"))).click()
                                                                               
        print("Click on category dropdown menu")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Select']"))).click()
        time.sleep(1)
        
        print("Click on third entry in category list")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'el-popper-container-')]/div/div/div/div[1]/ul/li[3]"))).click()
        time.sleep(1)
 
        # print("Select data category")
        # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"el-popper-container-254\"]/div/div/div/div[1]/ul/li[3]"))).click()
        # time.sleep(1)

        print("Click on +TextArea for OSF Description")
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"pane-OSF settings\"]/div/div[3]/div/div[2]/div[1]/div[1]/div/div[1]/div/button"))).click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-textarea__inner'))).send_keys("OSF Project Description")


        print("Switch to parent frame")
        driver.switch_to.parent_frame() 

        print("Click on continue button")
        # /html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[3]/div/button[2]/span
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[3]/div/button[2]/span'))).click()

        print("Click on publish button")
        # /html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[3]/div/button[2]/span
        WebDriverWait(driver, g_driverTimeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div/div[2]/div/div/div/div[3]/div/button[2]/span'))).click()


        try:
            print("Waiting for publication notification")
            WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "v-snack__content"), "successfully published"))
            print("Looks like the data has been published! Well done!")
        except:
            print("Timeout while waiting for publication")

        print("Done...")
        time.sleep(3)

if __name__ == '__main__':
    # unittest.main()
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
