import os
import time
import re
from datetime import datetime, timedelta
from os import path

from bs4 import BeautifulSoup
from selenium import webdriver


# Helper functions

def openFile(filePath):
    if path.exists(filePath):  # Check if path already exists
        fileName = open(filePath, "w", encoding='utf-8')
    else:  # Create file if it doesn't exist
        fileName = open(filePath, "x", encoding='utf-8')
    return fileName


def openDriver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def smallDate(date):
    return "<small>(" + date + ")</small>"


# Variables

todaysDate = datetime.now()
offset = (todaysDate.weekday() - 1) % 7
mtlDate = todaysDate - timedelta(days=offset)
mtlDate = f'{mtlDate:%B} {mtlDate.day}, {mtlDate.year}'  # Format date
todaysDate = f'{todaysDate:%B} {todaysDate.day}, {todaysDate.year}'

# Check if folder for files exists. If not, create it
if not path.exists("infoboxes"):
    os.makedirs("infoboxes")

# File paths
QCPathName = "infoboxes/QuebecInfobox.txt"
MTLPathName = "infoboxes/MontrealInfobox.txt"
piechartPathName = "infoboxes/PiechartQuebecVaccination.txt"
infoboxPathName = "infoboxes/QuebecVaccination.txt"

# Open files for writing
QCFile = openFile(QCPathName)
MTLFile = openFile(MTLPathName)
infoboxFile = openFile(infoboxPathName)
piechartFile = openFile(piechartPathName)


def vaccination():  # Function for COVID-19 vaccination in Quebec article

    # Initial text
    textPiechart = "{{Pie chart\n| caption=Total " \
                   "number of people receiving vaccinations in Quebec as of " + todaysDate + "\n| ref=https://www.inspq.qc.ca/covid-19/donnees/vaccination"
    textInfobox = "| participants             ='''"

    quebecPopulation = 8585523  # Stats Can estimate Q2 2021

    # Set up web scraping
    driver = openDriver("https://www.inspq.qc.ca/covid-19/donnees/vaccination")

    try:
        time.sleep(1.5)  # Wait for the page to load completely
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Get page source

        result = soup.findAll("span", class_="chiffres")  # Get numbers from INSPQ

        # Extract and format numbers
        populationVaccinated = re.search('[0-9]{2}.[0-9]+', str(result[0]).replace(",", ".")).group(0)
        populationVaccinated = float(populationVaccinated)

        eligiblePopulationVaccinated = re.search('[0-9]{2}.[0-9]+', str(result[1]).replace(",", ".")).group(0)
        eligiblePopulationVaccinated = float(eligiblePopulationVaccinated)

        adequatelyVaccinated = re.search('[0-9]{2}.[0-9]+', str(result[2]).replace(",", ".")).group(0)
        adequatelyVaccinated = float(adequatelyVaccinated)

        dosesAdministered = re.search('[0-9]{2}\s[0-9]{3}\s[0-9]{3}', str(result[3])).group(0).replace(" ", "")
        dosesAdministered = int(dosesAdministered)

        secondDosesAdministered = re.search('[0-9]{1}\s[0-9]{3}\s[0-9]{3}', str(result[4])).group(0).replace(" ", "")
        secondDosesAdministered = int(secondDosesAdministered)
    finally:
        driver.quit()

    refs = ["<ref name=\"inspqVacc\">{{cite web |title=Données de " \
            "vaccination contre la COVID-19 au Québec " \
            "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination |website=INSPQ " \
            "|publisher=Gouvernement |access-date=2021-03-19|language=fr}}</ref>",
            "<ref name=\"inspqVacc\"/>"
            ]

    # Write to infobox file

    smallTodaysDate = smallDate(todaysDate)

    textInfobox += str(f'{dosesAdministered:,}') + "''' doses administered  " + smallTodaysDate + refs[0] + "\n" \
                                                                                                            "<br>'''" + str(
        f'{secondDosesAdministered:,}') + \
                   "''' second doses administered " + smallTodaysDate + refs[1] + \
                   "\n| outcome                  = '''" + str(populationVaccinated) + \
                   "%''' of the population has received at least one dose of a vaccine " + smallTodaysDate + refs[1] + \
                   "<br>'''" + str(eligiblePopulationVaccinated) + "%''' of the population " \
                                                                   "≥12 years old is \"adequately vaccinated\"" \
                                                                   "{{efn|The Quebec government defines an \"adequately vaccinated\" person " \
                                                                   "as someone who has either received two doses of a vaccine or one dose of a" \
                                                                   " vaccine if they have already had COVID-19}} " + smallTodaysDate + \
                   refs[1] + "\n" \
                             "|organizers               = - [[Health Canada]]<br>- [[Public Health Agency of " \
                             "Canada]]<br>- [[Quebec|Quebec government]]<br>- [[Municipal government in Canada]]\n" \
                             "| website                  = [https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus" \
                             "/situation-coronavirus-in-quebec/covid-19-vaccination-data Government of Quebec]\n}} "

    infoboxFile.write(textInfobox)

    # Calculations for piechart

    unvaccinated = int(((100 - populationVaccinated) / 100) * quebecPopulation)
    unvaccinatedPercentage = round((unvaccinated / quebecPopulation) * 100, 1)

    oneDose = int(((populationVaccinated / 100) * quebecPopulation) - secondDosesAdministered)
    oneDosePercentage = round((oneDose / quebecPopulation) * 100, 1)

    secondDosePercentage = round(populationVaccinated - oneDosePercentage, 1)

    textPiechart += "\n| label1 = Unvaccinated population: ~" + str(f'{unvaccinated:,}') + \
                    " people <!-- Quebec population estimate as of Q2 2021: 8,585,523 -->" \
                    "\n| value1 = " + str(unvaccinatedPercentage) + " | color1 = #BFBFBF" \
                                                                    "\n| label2 = Population who has received only one dose of a vaccine: " + \
                    str(f'{oneDose:,}') + " people" \
                                          "\n| value2 = " + str(oneDosePercentage) + " | color2 = #42f5da" \
                                                                                     "\n| label3 = Population who has been fully vaccinated (both doses): " + \
                    str(f'{secondDosesAdministered:,}') + " people" \
                                                          "\n| value3 = " + str(
        secondDosePercentage) + " | color3 = #008\n}}"

    piechartFile.write(textPiechart)

    return populationVaccinated


def generateAllInfoboxes():
    # Set up web scraping
    driver = openDriver("https://www.inspq.qc.ca/covid-19/donnees")

    # Set up web scraping for vaccination Montreal
    driver2 = openDriver("https://dsp-de-mtl.maps.arcgis.com/apps/dashboards/5cc9eed428cb454da09d7cde4228be92")

    populationVaccinated = vaccination()  # Get vaccination info

    try:
        time.sleep(1.5)  # Wait for the page to load completely
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Get page source
        soup2 = BeautifulSoup(driver2.page_source, 'html.parser')  # Get page source

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
        rows = table.find_all("tr")  # Find rows
        rowData = rows[8].find_all("td")  # Find data

        mtlCases = int(rowData[1].text.replace(" ", ""))
        mtlActiveCases = int(rowData[3].text.replace(" ", ""))

        # Find deaths table
        tableDeaths = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "tableau-rpa")
        rowsDeaths = tableDeaths.find_all("tr")  # Find rows
        rowDataDeaths = rowsDeaths[6].find_all("td")  # Find data

        mtlDeaths = int(re.sub(r"\s+", "", rowDataDeaths[7].text, flags=re.UNICODE))

        # Get vaccination info
        results = soup2.findAll("text")

        mtlPercentageVaccinated = (results[3].text.strip())[0:-2]
        mtlPercentageAdequatelyVaccinated = (results[5].text.strip())[0:-2]

    finally:
        driver.quit()
        driver2.quit()

    # Write to infobox file

    refs = ["<ref name=\"auto6\">{{Cite "
            "web|url=https://www.inspq.qc.ca/covid-19/donnees|title=Données "
            "COVID-19 au Québec|website=INSPQ}}</ref>\n",
            "<ref name=\"auto6\"/>\n",
            "<ref name=\"inspqVacc\">{{cite web |title=Données de "
            "vaccination contre la COVID-19 au Québec "
            "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination "
            "|website=INSPQ |publisher=Gouvernement "
            "|access-date=2021-03-19|language=fr}}</ref>",
            "<ref name=\"vacc\">{{cite web |title=DATA COVID-19 VACCINATION IN MONTRÉAL "
            "|url=https://santemontreal.qc.ca/en/public/coronavirus-covid-19/vaccination/data-vaccination/ "
            "|website=Santé Montréal |publisher=Gouvernement du Québec}}</ref>",
            "<ref name=\"vacc\"/>"
            ]

    # Write to QC file
    textQC = "| date            = " + todaysDate + "\n" \
                                                   "| confirmed_cases = " + str(f'{cases:,}') + refs[0] + \
             "| active_cases    = " + str(f'{activeCases:,}') + refs[1] + \
             "| deaths          = " + str(f'{deaths:,}') + refs[1] + \
             "| recovery_cases  = " + str(f'{recoveredCases:,}') + refs[1] + \
             "| fatality_rate   = {{Percentage|" + str(deaths) + "|" + str(cases) + \
             "|2}}\n| vaccinations    = \n*'''" + str(populationVaccinated) + \
             "%'''  vaccinated with at least one dose " + smallDate(todaysDate) + refs[2]

    QCFile.write(textQC)

    # Write to MTL file
    textMTL = "| date            = " + todaysDate + "\n" \
                                                    "| confirmed_cases = " + str(f'{mtlCases:,}') + refs[0] + \
              "| active_cases    = " + str(f'{mtlActiveCases:,}') + refs[1] + \
              "| deaths          = " + str(f'{mtlDeaths:,}') + refs[1] + \
              "| fatality_rate   = {{Percentage|" + str(mtlDeaths) + "|" + str(mtlCases) + \
              "|2}}\n| vaccinations    =\n*'''" + \
              mtlPercentageVaccinated + "%''' vaccinated with at least one dose " + smallDate(mtlDate) + refs[3] + \
              "\n*'''" + mtlPercentageAdequatelyVaccinated + "%''' fully vaccinated " + smallDate(mtlDate) + refs[4]

    MTLFile.write(textMTL)

if __name__ == "__main__":
    generateAllInfoboxes()
