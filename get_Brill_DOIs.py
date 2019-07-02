#!/usr/bin/env python

#python 3.5.1, selenium 3.4.3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv
import sys
import re

def main(input, output):
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    browser = webdriver.Firefox(capabilities=firefox_capabilities)    
    outputFile = open(output, 'w')
    writer = csv.writer(outputFile, doublequote=True, escapechar='\\', lineterminator='\r')

    with open(input, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            #print(row[0])
            result = row
            doi = ''
            title = ''
            
            if 'http' not in row[len(row)-1]:
                result.append('DOI')
                result.append('TITLE')
                writer.writerow(result)
            else:
                url = row[len(row)-1]
                #print(url)
                browser.get(url)
                
                #<meta content="..." name="dc.identifier"></meta>
                doi = browser.find_element_by_xpath(
                    '//meta[@name="dc.identifier"]').get_attribute('content')
                #print(doi)
                #<title>...</title>
                title = browser.title
                #print(title)
                
            result.append(doi)
            result.append(title.encode('utf-8')) #makes the output weird but avoids errors; if using again use try/except
            writer.writerow(result)
    browser.close()
    outputFile.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])