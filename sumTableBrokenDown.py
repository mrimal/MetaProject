
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

projectIDs = pandas.read_csv('projects.csv')

finalTable= []
yearTable = []
bodyTable = []
#Looping over all the IDs in the project csv.
for projectID in projectIDs:
   
    response = webdriver.request('POST', config.postUrl, data={"opspage": "dashboard > Budget", "disbRatio":"0.0", "projectId":projectID, "fiscalYear":"", "asaFlag":"false"})
    html2 = response.text
    encodedHtml = html2.encode('ascii', 'ignore')
    soup = BeautifulSoup(encodedHtml)
    
    #Finding the total number of years data is available for each of the projects 
    year_list = soup.find('select', {"class": "form-control"})
    
    #Looping over all the years. Since, year_list.find_all('option') finds the dropdown with the year options
    z = 0  #Table header counter
    p = 0  #Table body Counter
    
    for option in year_list.find_all('option'):
        
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
            try:
                if table_headers:
                   yearTable.append([headers.get_text() for headers in table_headers])
                   for x in yearTable[z:z+1] :
                       x.insert(0, projectID)
                       x.insert(1, indi_year)
                       
                   #yearTable.insert(0,projectID)
                   
                table_data = row.find_all('td', attrs={})    
                if table_data:
                    bodyTable.append([data.get_text() for data in table_data])
                    
            except AttributeError as e:
                print "Ain't nothing brah"
                #yearTable.append([projectID])
            #yearTable = [x + [projectID] for x in row]
            #yearTable = [x + [indi_year] for x in row]
        z += 1 
        
        for x in bodyTable[p:p+3]:
            x.insert(0,projectID)
            x.insert(1,indi_year)
        
        p+= 3
  
finalTable = yearTable + bodyTable
              
#Writing the final table to a Pandas Dataframe and exporting it to Excel. 

budgetTable = pandas.DataFrame(finalTable, index=None)
print(budgetTable)
writer = pandas.ExcelWriter('newOutput.xlsx')
budgetTable.to_excel(writer, 'Sheet1' )
writer.save() 

