import requests
import re
from os import path
import os
from datetime import datetime
import pandas as pd

####################
# Global variables #
####################

fileDir = os.path.dirname(os.path.realpath('__file__'))

# TODO: Use dictionaries for these
refs = ["<ref name=\"auto6\">{{Cite "
        "web|url=https://www.inspq.qc.ca/covid-19/donnees|title=Données "
        "COVID-19 au Québec|website=INSPQ}}</ref>",
        "<ref name=\"auto6\"/>",
        "<ref name=\"inspqVacc\">{{cite web |title=Données de "
        "vaccination contre la COVID-19 au Québec "
        "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination "
        "|website=INSPQ |publisher=Gouvernement "
        "|access-date=2021-03-19|language=fr}}</ref>",
        "<ref name=\"inspqVacc\"/>"
        ]
mainRef = refs[1]

efn = "{{efn|This figure may not represent the current epidemiological situation — the Quebec government " \
      "restricted PCR COVID-19 tests to certain vulnerable groups on January 4, 2022.}}"

REGION = 'Croisement'
QC = 'RSS99'
MTL = 'RSS06'


####################
# Helper functions #
####################

def computeAverage(lst):
    return sum(lst) / len(lst)


def computeMovingAverage(data):
    # Calculate 7-day moving average
    i = 0
    j = 7

    movingAverage = []
    for iterate in range(len(data)):
        if len(data[i:j]) == 7:
            movingAverage.append(computeAverage(data[i:j]))
            i += 1
            j += 1

    return movingAverage


def smallDate(date):
    return "<small>(" + date + ")</small>"


def createAttribute(name, val):
    attr = {
        "name": name,
        "value": val
    }

    return attr


def writeAttributes(ls_attributes):
    text = ""
    for attribute in ls_attributes:
        if attribute['value'] is not None:
            text += f"| {attribute['name']:<15} = {attribute['value']}\n"
    return text


def writeValues(graphFile, name, vals):
    if vals is not None:
        graphFile.write(f"\n|{name} = ")
        for x in vals:
            graphFile.write(f"{x},")


def openFileForWriting(filePath):
    # Check if folder exists. If not, create it
    if not path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath))

    if path.exists(filePath):  # Check if path already exists
        fileName = open(filePath, "w", encoding='utf-8')
    else:  # Create file if it doesn't exist
        fileName = open(filePath, "x", encoding='utf-8')

    return fileName


def downloadCSV(url, fileName):
    try:
        # Download and save file
        r = requests.get(url, allow_redirects=True)

        if os.path.isfile(fileName):
            open(fileName, 'wb').write(r.content)
    except PermissionError:
        print(f"Error: you currently have {fileName} open. Please close it and try running the program again.")
        exit()


def readCSV(csv, skipRange):
    df = pd.read_csv(csv, index_col=False, parse_dates=[0], skiprows=lambda x: x in skipRange, dtype='str')
    return df

########################
# Generation functions #
########################

def generateGraphs(pathName, dates, y1Vals, y2Vals=None, y3Vals=None, y4Vals=None, y5Vals=None,
                   width=850, colors=None, showValues='offset:2', myType='line',
                   xAxisTitle='Date', xAxisFormat='%B %Y', xAxisAngle='-40',
                   yAxisTitle=None, y1Title=None, y2Title=None, y3Title=None, y4Title=None, y5Title=None,
                   xGrid='', yGrid='',
                   legend=None, xType='date', yType=None):
    # Open file for writing
    graphFile = openFileForWriting(pathName)

    # Create chart attributes

    attrs = [createAttribute("width", width), createAttribute("colors", colors),
             createAttribute("showValues", showValues), createAttribute("type", myType),
             createAttribute("xAxisTitle", xAxisTitle), createAttribute("xAxisFormat", xAxisFormat),
             createAttribute("xAxisAngle", xAxisAngle), createAttribute("xType", xType),
             createAttribute("yAxisTitle", yAxisTitle),
             createAttribute("y1Title", y1Title), createAttribute("y2Title", y2Title),
             createAttribute("y3Title", y3Title), createAttribute("y4Title", y4Title),
             createAttribute("y5Title", y5Title), createAttribute("yType", yType),
             createAttribute("xGrid", xGrid), createAttribute("yGrid", yGrid),
             createAttribute("legend", legend)]

    graphFile.write("{{Graph:Chart\n")
    graphFile.write(writeAttributes(attrs))

    # Write x and y values
    graphFile.write("|x = ")
    for x in dates:
        graphFile.write(f"{x:%Y-%m-%d},")

    writeValues(graphFile, "y1", y1Vals)
    writeValues(graphFile, "y2", y2Vals)
    writeValues(graphFile, "y3", y3Vals)
    writeValues(graphFile, "y4", y4Vals)
    writeValues(graphFile, "y5", y5Vals)

    graphFile.write("\n}}\n")
    graphFile.close()


def generateInfobox(pathName, ls_attributes):
    txtFile = openFileForWriting(pathName)
    txtFile.write(writeAttributes(ls_attributes))
    txtFile.close()


######################
# Montreal functions #
######################

def montreal(data, vaxData):

    ######################################
    # Get subsets of data from DataFrame #
    ######################################

    # Date
    dates = data.loc[(data[REGION] == MTL), 'ï»¿Date']
    currentDate = datetime.strftime(dates.iloc[-1], '%B %d, %Y')
    date = createAttribute("date", currentDate)

    # Cases
    newCases = data.loc[(data[REGION] == MTL), 'cas_quo_tot_n']
    casesMTL = data.loc[(data[REGION] == MTL), 'cas_cum_tot_n']
    confirmedCases = createAttribute("confirmed_cases", f'{int(casesMTL.iloc[-1]):,}{efn}{refs[0]}')

    # Deaths
    deathsMTL = data.loc[(data[REGION] == MTL), 'dec_cum_tot_n']
    death = createAttribute("deaths", f'{int(deathsMTL.iloc[-1]):,}{mainRef}')
    fatalityRate = createAttribute("fatality_rate",
                                   "{{Percentage|" + deathsMTL.iloc[-1] + "|" + casesMTL.iloc[-1] + "|2}}")

    # Vaccination dates
    dateVaccination = vaxData.loc[(vaxData[REGION] == MTL), 'ï»¿Date']
    currentDateVax = datetime.strftime(dateVaccination.iloc[-1], '%B %d, %Y')
    currentDateVax = smallDate(currentDateVax)

    # Vaccination stats
    percentage1stMTL = vaxData.loc[(vaxData[REGION] == MTL), 'cvac_cum_tot_1_p'].iloc[-1]
    percentage2ndMTL = vaxData.loc[(vaxData[REGION] == MTL), 'cvac_cum_tot_2_p'].iloc[-1]

    firstDose = f"\n*'''{float(percentage1stMTL):.1f}%''' vaccinated with at least one dose {currentDateVax}{mainRef}"
    secondDose = f"\n*'''{float(percentage2ndMTL):.1f}%''' fully vaccinated {currentDateVax}{mainRef}"

    vax = createAttribute("vaccinations", firstDose + secondDose)

    # Add all attributes to list and generate infobox
    attrs = [date, confirmedCases, death, fatalityRate, vax]
    generateInfobox("infoboxes/MontrealInfobox.txt", attrs)

    # Generate graphs
    generateGraphs("Files_Montreal/MontrealNewCases.txt", dates, newCases, colors="#FF6347",
                   yAxisTitle='New cases per day', y1Title='Cases')


####################
# Quebec functions #
####################

def quebec(data, vaxData):

    ######################################
    # Get subsets of data from DataFrame #
    ######################################

    # Date
    dates = data.loc[(data[REGION] == QC), 'ï»¿Date']
    currentDate = datetime.strftime(dates.iloc[-1], '%B %d, %Y')
    date = createAttribute("date", currentDate)

    # Cases
    newCases = data.loc[(data[REGION] == QC), 'cas_quo_tot_n']
    newCases = pd.to_numeric(newCases)

    cases = data.loc[(data[REGION] == QC), 'cas_cum_tot_n']
    confirmedCases = createAttribute("confirmed_cases", f'{int(cases.iloc[-1]):,}{efn}{refs[0]}')

    # Deaths
    deaths = data.loc[(data[REGION] == QC), 'dec_quo_tot_n']
    deathsTotal = data.loc[(data[REGION] == QC), 'dec_cum_tot_n']
    death = createAttribute("deaths", f'{int(deathsTotal.iloc[-1]):,}{refs[1]}')
    fatalityRate = createAttribute("fatality_rate",
                                   "{{Percentage|" + deathsTotal.iloc[-1] + "|" + cases.iloc[-1] + "|2}}")

    # Hospitalizations
    hospitalizations = data.loc[(data[REGION] == QC), 'hos_act_tot_n']
    hospitalization = createAttribute("hospitalized_cases", f'{int(hospitalizations.iloc[-1]):,}')

    # Vaccination
    percentage1st = vaxData.loc[(vaxData[REGION] == QC), 'cvac_cum_tot_1_p']
    vax = createAttribute("vaccinations",
                          "\n*'''" + f'{float(percentage1st.iloc[-1]):.1f}' + "%'''   vaccinated with at least one dose " +
                          refs[2])

    # Generate infobox
    attrs = [date, confirmedCases, death, fatalityRate, hospitalization, vax]
    generateInfobox("infoboxes/QuebecInfobox.txt", attrs)

    # Generate graphs
    generateGraphs("Files_Quebec/QuebecNewCases.txt", dates, newCases, y2Vals=computeMovingAverage(newCases),
                   colors='#ffc1b5, #FF6347', yAxisTitle='No. of new cases',
                   y1Title='Daily new cases', y2Title='7-day moving average',
                   legend='Legend')
    generateGraphs("Files_Quebec/QuebecNewDeaths.txt", dates, deaths,
                   colors='#FF6347', yAxisTitle='No. of new deaths',
                   y1Title='Daily new deaths', legend='Legend')


#########################
# Vaccination functions #
#########################

def vaccination(data):

    ######################################
    # Get subsets of data from DataFrame #
    ######################################

    # Date
    dateVaccination = data.loc[(data[REGION] == QC), 'ï»¿Date']
    currentDate = datetime.strftime(dateVaccination.iloc[-1], '%B %d, %Y')
    currentDate = smallDate(currentDate)

    # Daily doses
    dailyDoses1st = data.loc[(data[REGION] == QC), 'vac_quo_1_n']
    dailyDoses2nd = data.loc[(data[REGION] == QC), 'vac_quo_2_n']
    dailyDoses3rd = data.loc[(data[REGION] == QC), 'vac_quo_3_n']
    dailyDoses4th = data.loc[(data[REGION] == QC), 'vac_quo_4_n']

    # Total doses
    totalDoses1st = data.loc[(data[REGION] == QC), 'vac_cum_1_n']
    totalDoses2nd = data.loc[(data[REGION] == QC), 'vac_cum_2_n']
    totalDoses3rd = data.loc[(data[REGION] == QC), 'vac_cum_3_n']
    totalDoses4th = data.loc[(data[REGION] == QC), 'vac_cum_4_n']
    totalDosesTotal = data.loc[(data[REGION] == QC), 'vac_cum_tot_n']

    totalAdministered = f"'''{int(totalDosesTotal.iloc[-1]):,}''' doses administered {currentDate}{refs[2]}<br>"
    total2Administered = f"'''{int(totalDoses2nd.iloc[-1]):,}''' second doses administered {currentDate}{refs[3]}"
    participants = createAttribute("participants", totalAdministered + total2Administered)

    # Percentages
    percentage1st = data.loc[(data[REGION] == QC), 'cvac_cum_tot_1_p']
    percentage2nd = data.loc[(data[REGION] == QC), 'cvac_cum_tot_2_p']
    outcome1 = f"'''{float(percentage1st.iloc[-1]):.1f}%''' of the population has received at least one dose of a vaccine {currentDate}{refs[3]}"
    outcome = createAttribute("outcome", outcome1)

    # Generate infobox
    generateInfobox("infoboxes/vaccination.txt", [participants, outcome])
    vaccinationPiechart(dateVaccination.iloc[-1], percentage1st.iloc[-1], totalDoses2nd.iloc[-1])

    # Generate graphs
    generateGraphs("Files_Vaccination/DailyDoses.txt", dateVaccination, dailyDoses1st, y1Title='1st dose',
                   y2Vals=dailyDoses2nd, y2Title='2nd dose', y3Vals=dailyDoses3rd, y3Title='3rd dose',
                   y4Vals=dailyDoses4th, y4Title='4th dose', yAxisTitle='Number of doses',
                   legend='Legend', colors='#72B8B1, #3b94a8, #196165, #043538'
                   )
    generateGraphs("Files_Vaccination/TotalDoses.txt", dateVaccination, totalDoses1st, y1Title='1st dose',
                   y2Vals=totalDoses2nd, y2Title='2nd dose', y3Vals=totalDoses3rd, y3Title='3rd dose',
                   y4Vals=totalDoses4th, y4Title='4th dose', y5Vals=totalDosesTotal, y5Title='Total doses',
                   yAxisTitle='Number of doses', legend='Legend',
                   colors='#72B8B1, #3b94a8, #196165, #043538, #929292'
                   )
    generateGraphs("Files_Vaccination/PercentageVaccinated.txt", dateVaccination, percentage1st, y1Title='1st dose',
                   y2Vals=percentage2nd, y2Title='2nd dose', yAxisTitle='Percentage of the population vaccinated (%)',
                   legend='Legend', colors='#72B8B1, #196165'
                   )


def vaccinationPiechart(dateVaccination, percentage1st, totalDoses2nd):

    quebecPopulation = 8585523  # Stats Can estimate Q2 2021

    # Open file
    vaxPathName = "infoboxes/PiechartQuebecVaccination.txt"
    vaxFile = openFileForWriting(vaxPathName)

    # Calculations for piechart
    unvaccinated = int(((100 - float(percentage1st)) / 100) * quebecPopulation)
    unvaccinatedPercentage = round((unvaccinated / quebecPopulation) * 100, 1)

    oneDose = int(((float(percentage1st) / 100) * quebecPopulation) - int(totalDoses2nd))
    oneDosePercentage = round((oneDose / quebecPopulation) * 100, 1)

    secondDosePercentage = round(float(percentage1st) - oneDosePercentage)

    currentDate = datetime.strftime(dateVaccination, '%B %d, %Y')

    # Create attributes
    caption = createAttribute("caption", f"Total number of people receiving vaccinations in Quebec as of {currentDate}")
    ref = createAttribute("ref", "https://www.inspq.qc.ca/covid-19/donnees/vaccination")

    label1 = createAttribute("label1",
                             f"Unvaccinated population: ~{unvaccinated:,} people <!-- Quebec population estimate as of Q2 2021: 8,585,523 -->")
    value1 = createAttribute("value1", unvaccinatedPercentage)
    color1 = createAttribute("color1", "#BFBFBF")

    label2 = createAttribute("label2", f"Population who has received only one dose of a vaccine: {oneDose:,} people")
    value2 = createAttribute("value2", oneDosePercentage)
    color2 = createAttribute("color2", "#42f5da")

    label3 = createAttribute("label3",
                             f"Population who has been fully vaccinated (both doses): {int(totalDoses2nd):,} people")
    value3 = createAttribute("value3", secondDosePercentage)
    color3 = createAttribute("color3", "#008")

    # Write to file
    attrs = [caption, ref, label1, value1, color1, label2, value2, color2, label3, value3, color3]
    vaxFile.write(writeAttributes(attrs))
    vaxFile.close()


if __name__ == "__main__":

    # Get CSVs
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
    quebecCasesCSV = open("covid19-hist.csv", "r")

    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv', "vaccination.csv")
    vaccinationsCSV = open("vaccination.csv", "r")

    # Read CSVs
    mainData = readCSV(quebecCasesCSV, range(1, 1429))
    vData = readCSV(vaccinationsCSV, range(0, 0))

    # Generate infoboxes and graphs for each article
    quebec(mainData, vData)
    montreal(mainData, vData)
    vaccination(vData)
