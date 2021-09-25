import os
import time
import re
import datetime
from os import path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import mwclient

# Variables
import vaccinationPiechartWikipedia

todaysDate = datetime.datetime.now()
todaysDate = f'{todaysDate:%B} {todaysDate.day}, {todaysDate.year}'

MTL_ROW = 8

# Creating and/or opening files
if not path.exists("infoboxes"):  # Check if folder exists. If not, create it
    os.makedirs("infoboxes")

# File names
QCPathName = "infoboxes/QuebecInfobox.txt"
MTLPathName = "infoboxes/MontrealInfobox.txt"

# Open file for writing
if path.exists(QCPathName):
    QCFile = open(QCPathName, "w", encoding='utf-8')
else:  # Create file if it doesn't exist
    QCFile = open(QCPathName, "x", encoding='utf-8')

# Open file for writing
if path.exists(MTLPathName):
    MTLFile = open(MTLPathName, "w", encoding='utf-8')
else:  # Create file if it doesn't exist
    MTLFile = open(MTLPathName, "x", encoding='utf-8')

# Set up web scraping
driver = webdriver.Chrome()
url = "https://www.inspq.qc.ca/covid-19/donnees"
driver.get(url)

try:
    time.sleep(1.5)  # Wait for the page to load completely
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Get page source

    ##########
    # QUEBEC #
    ##########

    result = soup.findAll("span", class_="chiffres")  # Get numbers from INSPQ

    # Extract and format numbers
    cases = re.search('[0-9]{3}\s[0-9]{3}', str(result[0])).group(0)
    cases = int(cases.replace(" ", ""))

    activeCases = re.search('[0-9]\s[0-9]{3}', str(result[1])).group(0)
    activeCases = int(activeCases.replace(" ", ""))

    recoveredCases = re.search('[0-9]{3}\s[0-9]{3}', str(result[2])).group(0)
    recoveredCases = int(recoveredCases.replace(" ", ""))

    deaths = re.search('[0-9]{2}\s[0-9]{3}', str(result[3])).group(0)
    deaths = int(deaths.replace(" ", ""))

    ############
    # MONTREAL #
    ############

    # Find cases table
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "cas_regions")
    rows = table.find_all("tr") # Find rows
    rowData = rows[MTL_ROW].find_all("td")  # Find data

    mtlCases = rowData[1].text
    mtlActiveCases = rowData[3].text

    # Find deaths table
    tableDeaths = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "tableau-rpa")
    rowsDeaths = tableDeaths.find_all("tr")  # Find rows
    #rowDataDeaths = rowsDeaths[6].find_all("td")  # Find data
    for x in rowsDeaths:
        print(x.text)

    #mtlDeaths = rowDataDeaths[7]

    #print(mtlDeaths)

finally:
    driver.quit()

# Write to infobox file

refs = ["<ref name=\"auto6\">{{Cite "
        "web|url=https://www.inspq.qc.ca/covid-19/donnees|title=Données "
        "COVID-19 au Québec|website=INSPQ}}</ref>\n", "<ref name=\"auto6\"/>\n",
        "<ref name=\"inspqVacc\">{{cite web |title=Données de "
        "vaccination contre la COVID-19 au Québec "
        "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination "
        "|website=INSPQ |publisher=Gouvernement "
        "|access-date=2021-03-19|language=fr}}</ref>"]

textQC = "| confirmed_cases = " + str(f'{cases:,}') + refs[0] + \
         "| active_cases    = " + str(f'{activeCases:,}') + refs[1] + \
         "| deaths          = " + str(f'{deaths:,}') + refs[1] + \
         "| recovery_cases  = " + str(f'{recoveredCases:,}') + refs[1] + \
         "| fatality_rate   = {{Percentage|" + str(deaths) + "|" + str(cases) + \
         "|2}}\n| vaccinations    = \n*'''" + str(vaccinationPiechartWikipedia.populationVaccinated) + \
         "%'''  vaccinated with at least one dose <small>(" + todaysDate + \
         ")</small>" + refs[2]

QCFile.write(textQC)
