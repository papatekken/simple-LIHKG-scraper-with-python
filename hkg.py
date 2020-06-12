from openpyxl import Workbook
from openpyxl import load_workbook
from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import io

__version__ = '0.12'


def captureData(ID):
	browser = webdriver.Chrome() 
	browser.maximize_window()
	browser.get("http://lihkg.com/thread/"+ID) #navigate to the page	

	problem = False
	timeout = 10
	try: 
		element_present = EC.presence_of_element_located((By.CLASS_NAME, '_36ZEkSvpdj_igmog0nluzh'))
		WebDriverWait(browser, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out waiting for page to load" )
		problem = True
	
	if(not problem): #make sure the page can load
		with io.open(ID+"Exported.txt", "w", encoding="utf-8") as file:
			content = browser.find_element_by_class_name('_1H7LRkyaZfWThykmNIYwpH')
			opt = content.find_elements_by_tag_name('option') 
			i=len(opt)
			for counter in range(1, i):
				browser.get("http://lihkg.com/thread/"+ID+"/page/"+str(counter)) #navigate to the page by page no
				timeout = 10
				try:
					element_present = EC.presence_of_element_located((By.CLASS_NAME, '_36ZEkSvpdj_igmog0nluzh'))
					WebDriverWait(browser, timeout).until(element_present)
				except TimeoutException:
					file.write("Timed out waiting for page "+counter+"to load" )
					problem = True		
				if(not problem): #make sure the page can load	
					content = browser.find_elements_by_class_name('_36ZEkSvpdj_igmog0nluzh')
					for x in content:
						file.write("*************************************************")
						file.write(x.text)
		file.close()
	if (browser!=None):
		browser.quit()  
  
  
  
if(len(sys.argv)<2):
	print("no post ID found")
	sys.exit()

print("***simple scrape lihkg ***")
print("Version "+__version__)
print(" ")
captureData(sys.argv[1])
print("Finished")
