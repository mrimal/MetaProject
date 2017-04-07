# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 17:52:14 2017

@author: mpr`
"""

from seleniumrequests import Chrome
import config
#import os
from bs4 import BeautifulSoup
import pandas
from pandas import DataFrame

webdriver = Chrome()

#text_file = open("Output.txt", "w")
#text_file.write("%s" % encodedHtml)
#text_file.close()


projectIDs = pandas.read_csv('projects.csv')

finalTable= []
for projectID in projectIDs:
    
    response = webdriver.request('POST', config.postUrl, data={"opspage": "dashboard > Budget", "disbRatio":"0.0", "projectId":projectID, "fiscalYear":"", "asaFlag":"false"})
    html2 = response.text
    encodedHtml = html2.encode('ascii', 'ignore')
    soup = BeautifulSoup(html2)
    
    year_list = soup.find('select', {"class": "form-control"})
    
    for option in year_list.find_all('option'):
        indi_year = option.text
        print(indi_year)
    
    
        
        
        
        
    