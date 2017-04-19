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
    
    year_list = soup.find_all(name='select', attrs={'class': 'form-control'})
    print(year_list)
    
    for year in year_list.find_all('option'):
        indi_year = year.text
        indi_year = indi_year.strip()
        
        response = webdriver.request('POST', config.summaryTableURL, data={"fiscalYear": indi_year, "projectId":projectID})
        pageHtml = response.text
        pageencodedHtml = pageHtml.encode('ascii', 'ignore')
        soup = BeautifulSoup(pageencodedHtml)
        try:
            table = soup.find('table', {"class": config.budgetTableClass})
            rows = table.find_all('tr')
        except AttributeError as e:
            print 'No table found'
        
       
        for row in rows :
                table_headers = row.find_all('th')
                if table_headers:
                   finalTable.append([headers.get_text() for headers in table_headers])
                   
                table_data = row.find_all('td', attrs={})    
                if table_data:
                    finalTable.append([data.get_text() for data in table_data])
    

budgetTable = pandas.DataFrame(finalTable, index=None)

print(budgetTable)

writer = pandas.ExcelWriter('newOutputShort.xlsx')
budgetTable.to_excel(writer, 'Sheet1' )
writer.save()