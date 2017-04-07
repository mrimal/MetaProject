# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 15:31:18 2017

@author: mpr
"""

from seleniumrequests import Chrome
import config
#import os
from bs4 import BeautifulSoup
import pandas
from pandas import DataFrame

webdriver = Chrome()
response = webdriver.request('POST', config.postUrl, data={"opspage": "dashboard > Budget", "disbRatio":"0.0", "projectId":config.projectID, "fiscalYear":"", "asaFlag":"false"})
html2 = response.text
encodedHtml = html2.encode('ascii', 'ignore')
#text_file = open("Output.txt", "w")
#text_file.write("%s" % encodedHtml)
#text_file.close()

soup = BeautifulSoup(html2)
projectIDs = pandas.read_csv('projects.csv')

finalTable= []
for projectID in projectIDs:
    
    try:
        table = soup.find('table', {"class": config.budgetTableClass})
        rows = table.find_all('tr')
    except AttributeError as e:
        print 'No table found'
        
    for row in rows :
            table_headers = row.find_all('th')
            if table_headers:
                finalTable.append([headers.get_text() for headers in table_headers])
                #finalTable.insert(0,config.projectID)
            
            table_data = row.find_all('td', attrs={})    
            if table_data:
                finalTable.append([data.get_text() for data in table_data])
                #finalTable.insert(0,config.projectID)

budgetTable = pandas.DataFrame(finalTable, index=None)

print(budgetTable)

writer = pandas.ExcelWriter('newOutputShort.xlsx')
budgetTable.to_excel(writer, 'Sheet1' )
writer.save()