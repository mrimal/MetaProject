
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 17:52:14 2017
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

#Reading projectIDs from the csv file provided with the project IDs.

projectIDs = pandas.read_csv('projectNewList.csv')
df1 = projectIDs.ix[:,500:1000] 

print(df1)

finalTable = []
#Looping over all the IDs in the project csv.
for projectID in df1:
    

    response = webdriver.request('POST', config.postUrl, data={"opspage": "dashboard > Budget", "disbRatio":"0.0", "projectId":projectID, "fiscalYear":"", "asaFlag":"false"})
    html2 = response.text
    encodedHtml = html2.encode('ascii', 'ignore')
    soup = BeautifulSoup(encodedHtml)
    
    #Finding the total number of years data is available for each of the projects 
    year_list = soup.find('select', {"class": "form-control"})
    
    #Looping over all the years 
    
    for option in year_list.find_all('option'):
        tempTable= []

        indi_year = option.text
        
        indi_year = indi_year.encode("utf-8")
        indi_year = indi_year.strip()
        print(indi_year)

        response = webdriver.request('POST', config.postUrl, data={"fiscalYear": indi_year, "projectId":projectID})
        pageHtml = response.text
        pageencodedHtml = pageHtml.encode('ascii', 'ignore')
        soup = BeautifulSoup(pageencodedHtml)
    
        try:
            table = soup.find('table', {"class": config.expenseTable})
            rows = table.find_all('tr')
        except AttributeError as e:
            print 'No table found'
            
        for row in rows :
            table_headers = row.find_all('th')
            if table_headers:
               tempTable.append([headers.get_text() for headers in table_headers])
            
            table_data = row.find_all('td', attrs={})    
            if table_data:
                tempTable.append([data.get_text() for data in table_data])
        for indiRows in tempTable:
            indiRows.insert(0, projectID)
            indiRows.insert(1, indi_year)
        
        finalTable = finalTable + tempTable
        
#Writing the final table to a Pandas Dataframe and exporting it to Excel. 

budgetTable = pandas.DataFrame(finalTable, index=None)
print(budgetTable)
writer = pandas.ExcelWriter('newOutput.xlsx')
budgetTable.to_excel(writer, 'Sheet1' )
writer.save() 