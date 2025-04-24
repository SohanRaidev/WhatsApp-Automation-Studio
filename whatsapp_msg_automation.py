
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
#-------------------------------------------------------------------------
from selenium import webdriver

driver = webdriver.Chrome()


driver.get("https://web.whatsapp.com/")
#-------------------------------------------------------------------------

time.sleep(30)

#Messages HERE:

sentences = [

 "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ", "ㅤ",

]

for i in range(len(sentences)):
    question = driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]')
    question.click() 
   # time.sleep(0.5)
    txtq = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p')
    txtq.send_keys(sentences[i])
    #time.sleep(0.5)
   # txtq.send_keys(webdriver.Keys.RETURN)
    submitq = driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button')
    submitq.click()
   # time.sleep(0.5)

#-------------------------------------------------------------------------------------
