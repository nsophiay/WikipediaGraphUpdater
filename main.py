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
mainRef = "<ref name=\"auto6\"/>"


####################
# Helper functions #
####################

def computeAverage(lst):
    return sum(lst) / len(lst)


def smallDate(date):
    return "<small>(" + date + ")</small>"


def createAttribute(name, val):
    attr = {
        "name": name,
        "value": val
    }

    return attr


def createColumn(name, index, date, region, varType):
    attr = {
        "name": name,
        "index": index,
        "date": date,
        "region": region,
        "type": varType
    }
    return attr


def openFile(filePath):
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


def readCSVpandas(csv, skipRange):
    df = pd.read_csv(csv, index_col=False, parse_dates=[0], skiprows=lambda x: x in skipRange, dtype='str')
    return df


######################
# Montreal functions #
######################

def montrealGraphs(data):
    dates = data.loc[(data['Croisement'] == 'RSS06'), 'ï»¿Date']
    newCases = data.loc[(data['Croisement'] == 'RSS06'), 'cas_quo_tot_n']

    if not path.exists("Files_Montreal"):  # Check if folder exists. If not, create it
        os.makedirs("Files_Montreal")

    # File names
    MontrealNewCases = "Files_Montreal/MontrealNewCases.txt"

    # Open file for writing
    if path.exists(MontrealNewCases):
        montrealCases = open(MontrealNewCases, "w")
    else:  # Create file if it doesn't exist
        montrealCases = open(MontrealNewCases, "x")

    montrealCases.writelines(["=== Montreal region, new cases per day ===\n",
                              "{{Graph:Chart\n",
                              "|width=850\n",
                              "|colors=#FF6347\n",
                              "|showValues= offset:2\n",
                              "|xAxisAngle=-40\n",
                              "|xType=date\n",
                              "|type=line\n",
                              "|x = "])

    # Write to file
    montrealCases = open(MontrealNewCases, "a")
    for x in dates:
        montrealCases.write(f"{x},")

    montrealCases.writelines(["\n|yAxisTitle=New Cases\n", "|y1="])
    for x in newCases:
        montrealCases.write(f"{x},")

    montrealCases.writelines(["\n\n|y1Title=New cases per day\n",
                              "|yGrid= |xGrid=\n",
                              "}}\n",
                              "<!-- https://santemontreal.qc.ca/en/public/coronavirus-covid-19/situation-of-the-coronavirus-covid-19-in-montreal/#c43710 -->\n",
                              "<!-- Note that you should check numbers a few days back since numbers in the last few days might be increased -->"])
    montrealCases.close()


def montrealInfobox(data, vaxData):
    dates = data.loc[(data['Croisement'] == 'RSS06'), 'ï»¿Date']
    casesMTL = data.loc[(data['Croisement'] == 'RSS06'), 'cas_cum_tot_n']
    deathsMTL = data.loc[(data['Croisement'] == 'RSS06'), 'dec_cum_tot_n']

    dateVaccination = vaxData.loc[(vaxData['Croisement'] == 'RSS06'), 'ï»¿Date']
    percentage1stMTL = vaxData.loc[(vaxData['Croisement'] == 'RSS06'), 'cvac_cum_tot_1_p'].iloc[-1]
    percentage2ndMTL = vaxData.loc[(vaxData['Croisement'] == 'RSS06'), 'cvac_cum_tot_2_p'].iloc[-1]

    MTLPathName = "infoboxes/MontrealInfobox.txt"
    MTLFile = openFile(MTLPathName)

    ref = "<ref name=\"auto6\">{{Cite web|url=https://www.inspq.qc.ca/covid-19/donnees|title=Données COVID-19 au Québec|website=INSPQ}}</ref>"

    efn = "{{efn|This figure may not represent the current epidemiological situation — the Quebec government " \
          "restricted PCR COVID-19 tests to certain vulnerable groups on January 4, 2022.}}"

    currentDate = datetime.strftime(dates.iloc[-1], '%B %d, %Y')

    date = createAttribute("date", currentDate)
    confirmedCases = createAttribute("confirmed_cases", f'{int(casesMTL.iloc[-1]):,}{efn}{ref}')
    death = createAttribute("deaths", f'{int(deathsMTL.iloc[-1]):,}{mainRef}')
    fatalityRate = createAttribute("fatality_rate",
                                   "{{Percentage|" + deathsMTL.iloc[-1] + "|" + casesMTL.iloc[-1] + "|2}}")

    currentDate = datetime.strftime(dateVaccination.iloc[-1], '%B %d, %Y')
    currentDate = smallDate(currentDate)

    firstDose = f"\n*'''{float(percentage1stMTL):.1f}%''' vaccinated with at least one dose {currentDate}{mainRef}"
    secondDose = f"\n*'''{float(percentage2ndMTL):.1f}%''' fully vaccinated {currentDate}{mainRef}"
    vax = createAttribute("vaccinations", firstDose + secondDose)

    infobox = [date, confirmedCases, death, fatalityRate, vax]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}          = {attribute['value']}\n"

    MTLFile.write(text)
    MTLFile.close()


####################
# Quebec functions #
####################

def quebecGraphs(data):
    movingAverage = []

    dates = data.loc[(data['Croisement'] == 'RSS99'), 'ï»¿Date']
    newCases = data.loc[(data['Croisement'] == 'RSS99'), 'cas_quo_tot_n']
    newCases = pd.to_numeric(newCases)
    deaths = data.loc[(data['Croisement'] == 'RSS99'), 'dec_quo_tot_n']

    # File names
    QuebecNewCases = "Files_Quebec/QuebecNewCases.txt"
    QuebecNewDeaths = "Files_Quebec/QuebecNewDeaths.txt"

    if not path.exists("Files_Quebec"):
        os.makedirs("Files_Quebec")

    # Open file for writing
    if path.exists(QuebecNewCases):
        quebecCases = open(QuebecNewCases, "w")
    else:  # Create file if it doesn't exist
        quebecCases = open(QuebecNewCases, "x")

    # Open file for writing
    if path.exists(QuebecNewDeaths):
        quebecDeaths = open(QuebecNewDeaths, "w")
    else:  # Create file if it doesn't exist
        quebecDeaths = open(QuebecNewDeaths, "x")

    quebecCases.writelines(["<div style=\"overflow-x:auto;>\n",
                            "{{Graph:Chart\n",
                            "|width=950\n",
                            "|colors=#ffc1b5, #FF6347\n",
                            "|showValues= offset:2\n",
                            "|type=line\n",
                            "|xAxisTitle=Date\n",
                            "|xAxisFormat=%B %Y\n",
                            "|xAxisAngle=-40\n",
                            "|yAxisTitle=No. of new cases\n",
                            "|legend=Legend\n",
                            "|yGrid= |xGrid=\n",
                            "|xType = date\n",
                            "|x = "])

    quebecDeaths.writelines(["<div style=\"overflow-x:auto;>\n",
                             "{{Graph:Chart\n",
                             "| height = 180\n",
                             "| width = 950\n",
                             "|colors=#FF6347\n",
                             "|xAxisTitle=Date\n",
                             "|xAxisFormat=%B %Y\n",
                             "|xAxisAngle=-40\n",
                             "|yAxisTitle=No. of new deaths\n",
                             "| yAxisMin = 0\n",
                             "|type=line\n",
                             "|xType = date\n",
                             "|x = "])

    # Calculate 7-day moving average
    i = 0
    j = 7

    for iterate in range(len(newCases)):
        if len(newCases[i:j]) == 7:
            movingAverage.append(computeAverage(newCases[i:j]))
            i += 1
            j += 1

    # Write to file
    quebecCases = open(QuebecNewCases, "a")

    for x in dates:
        quebecCases.write(f"{x:%Y-%m-%d},")

    quebecCases.writelines(["\n|y1Title=Daily new cases\n", "|y1="])
    for x in newCases:
        quebecCases.write(f"{x},")

    quebecCases.writelines(["\n|y2Title=7-day moving average\n", "|y2="])
    for x in movingAverage:
        quebecCases.write(f"{x},")

    quebecCases.writelines(["\n}}\n", "</div>"])
    quebecCases.close()

    quebecDeaths = open(QuebecNewDeaths, "a")

    for x in dates:
        quebecDeaths.write(f"{x:%Y-%m-%d},")

    quebecDeaths.writelines(["\n|y1Title=Deaths\n", "|y1="])
    for x in deaths:
        quebecDeaths.write(f"{x},")

    quebecDeaths.writelines(["\n}}\n", "</div>"])
    quebecDeaths.close()


def quebecInfobox(data, vaxData):
    dates = data.loc[(data['Croisement'] == 'RSS99'), 'ï»¿Date']
    cases = data.loc[(data['Croisement'] == 'RSS99'), 'cas_cum_tot_n']
    deathsTotal = data.loc[(data['Croisement'] == 'RSS99'), 'dec_cum_tot_n']
    hospitalizations = data.loc[(data['Croisement'] == 'RSS99'), 'hos_act_tot_n']
    percentage1st = vaxData.loc[(vaxData['Croisement'] == 'RSS99'), 'cvac_cum_tot_1_p']

    refs = ["<ref name=\"auto6\">{{Cite "
            "web|url=https://www.inspq.qc.ca/covid-19/donnees|title=Données "
            "COVID-19 au Québec|website=INSPQ}}</ref>",
            "<ref name=\"auto6\"/>",
            "<ref name=\"inspqVacc\">{{cite web |title=Données de "
            "vaccination contre la COVID-19 au Québec "
            "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination "
            "|website=INSPQ |publisher=Gouvernement "
            "|access-date=2021-03-19|language=fr}}</ref>"
            ]

    QCPathName = "infoboxes/QuebecInfobox.txt"
    QCFile = openFile(QCPathName)

    # Format infobox

    efn = "{{efn|This figure may not represent the current epidemiological situation — the Quebec government " \
          "restricted PCR COVID-19 tests to certain vulnerable groups on January 4, 2022.}} "

    currentDate = datetime.strftime(dates.iloc[-1], '%B %d, %Y')

    date = createAttribute("date", currentDate)
    confirmedCases = createAttribute("confirmed_cases", f'{int(cases.iloc[-1]):,}{efn}{refs[0]}')
    death = createAttribute("deaths", f'{int(deathsTotal.iloc[-1]):,}{refs[1]}')
    fatalityRate = createAttribute("fatality_rate",
                                   "{{Percentage|" + deathsTotal.iloc[-1] + "|" + cases.iloc[-1] + "|2}}")
    hospitalization = createAttribute("hospitalized_cases", f'{int(hospitalizations.iloc[-1]):,}')
    vax = createAttribute("vaccinations",
                          "\n*'''" + f'{float(percentage1st.iloc[-1]):.1f}' + "%'''   vaccinated with at least one dose " +
                          refs[2])

    infobox = [date, confirmedCases, death, fatalityRate, hospitalization, vax]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}          = {attribute['value']}\n"

    QCFile.write(text)
    QCFile.close()


#########################
# Vaccination functions #
#########################

def vaccinationGraphs(data):
    dateVaccination = data.loc[(data['Croisement'] == 'RSS99'), 'ï»¿Date']

    dailyDoses1st = data.loc[(data['Croisement'] == 'RSS99'), 'vac_quo_1_n']
    dailyDoses2nd = data.loc[(data['Croisement'] == 'RSS99'), 'vac_quo_2_n']
    dailyDoses3rd = data.loc[(data['Croisement'] == 'RSS99'), 'vac_quo_3_n']
    dailyDoses4th = data.loc[(data['Croisement'] == 'RSS99'), 'vac_quo_4_n']

    totalDoses1st = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_1_n']
    totalDoses2nd = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_2_n']
    totalDoses3rd = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_3_n']
    totalDoses4th = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_4_n']
    totalDosesTotal = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_tot_n']

    percentage1st = data.loc[(data['Croisement'] == 'RSS99'), 'cvac_cum_tot_1_p']
    percentage2nd = data.loc[(data['Croisement'] == 'RSS99'), 'cvac_cum_tot_2_p']

    # File names
    DailyDoses = "Files_Vaccination/DailyDoses.txt"
    TotalDoses = "Files_Vaccination/TotalDoses.txt"
    PercentageVaccinated = "Files_Vaccination/PercentageVaccinated.txt"

    if not path.exists("Files_Vaccination"):
        os.makedirs("Files_Vaccination")

    # Open file for writing
    if path.exists(DailyDoses):
        dailyDoses = open(DailyDoses, "w")
    else:  # Create file if it doesn't exist
        dailyDoses = open(DailyDoses, "x")

    # Open file for writing
    if path.exists(TotalDoses):
        totalDoses = open(TotalDoses, "w")
    else:  # Create file if it doesn't exist
        totalDoses = open(TotalDoses, "x")

    # Open file for writing
    if path.exists(PercentageVaccinated):
        percentage = open(PercentageVaccinated, "w")
    else:  # Create file if it doesn't exist
        percentage = open(PercentageVaccinated, "x")

    dailyDoses.writelines(["=== Daily doses ===\n",
                           "{{Graph:Chart\n",
                           "| height =\n",
                           "|width=800\n",
                           "| xAxisTitle=Date (YYYY-MM)\n",
                           "| xType = date\n",
                           "| xAxisAngle=-40\n",
                           "| xAxisFormat=%Y-%m\n",
                           "| yGrid= 1\n",
                           "| xGrid= 1\n",
                           "| colors= #72B8B1, #3b94a8, #196165, #043538\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| y3Title=3rd dose\n",
                           "| y4Title=4th dose\n",
                           "| yAxisTitle = Number of doses\n",
                           "| x="
                           ])

    totalDoses.writelines(["=== Total doses ===\n",
                           "{{Graph:Chart\n",
                           "| height =\n",
                           "|width=800\n",
                           "| xAxisTitle=Date (YYYY-MM)\n",
                           "| xType = date\n",
                           "| xAxisAngle=-40\n",
                           "| xAxisFormat=%Y-%m\n",
                           "| yGrid= 1\n",
                           "| xGrid= 1\n",
                           "| colors= #72B8B1, #3b94a8, #196165, #043538,#929292\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| y3Title=3rd dose\n",
                           "| y4Title=4th dose\n",
                           "| y5Title= Total\n",
                           "| yAxisTitle = Cumulative number of doses\n",
                           "| x="
                           ])
    percentage.writelines(["=== Percentage of the population vaccinated ===\n",
                           "{{Graph:Chart\n",
                           "| height =\n",
                           "|width=800\n",
                           "| xAxisTitle=Date (YYYY-MM)\n",
                           "| xType = date\n",
                           "| xAxisAngle=-40\n",
                           "| xAxisFormat=%Y-%m\n",
                           "| yGrid= 1\n",
                           "| xGrid= 1\n",
                           "| colors= #72B8B1, #196165\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| yAxisTitle =  Percentage of the population vaccinated (%)\n",
                           "| x="
                           ])

    dailyDoses = open(DailyDoses, "a")

    # TODO: for the love of god just make this a method
    for x in dateVaccination:
        dailyDoses.write(f"{x},")

    dailyDoses.writelines(["\n|y1="])
    for x in dailyDoses1st:
        dailyDoses.write(f"{x},")

    dailyDoses.writelines(["\n|y2="])
    for x in dailyDoses2nd:
        dailyDoses.write(f"{x},")

    dailyDoses.writelines(["\n|y3="])
    for x in dailyDoses3rd:
        dailyDoses.write(f"{x},")

    dailyDoses.writelines(["\n|y4="])
    for x in dailyDoses4th:
        dailyDoses.write(f"{x},")

    dailyDoses.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv "
                           "CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] "
                           "website.</div>"])
    dailyDoses.close()

    totalDoses = open(TotalDoses, "a")

    for x in dateVaccination:
        totalDoses.write(f"{x},")

    totalDoses.writelines(["\n|y1="])
    for x in totalDoses1st:
        totalDoses.write(f"{x},")

    totalDoses.writelines(["\n|y2="])
    for x in totalDoses2nd:
        totalDoses.write(f"{x},")

    totalDoses.writelines(["\n|y3="])
    for x in totalDoses3rd:
        totalDoses.write(f"{x},")

    totalDoses.writelines(["\n|y4="])
    for x in totalDoses4th:
        totalDoses.write(f"{x},")

    totalDoses.writelines(["\n|y5="])
    for x in totalDosesTotal:
        totalDoses.write(f"{x},")

    totalDoses.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] website.</div>"])
    totalDoses.close()

    percentage = open(PercentageVaccinated, "a")

    for x in dateVaccination:
        percentage.write(f"{x},")

    percentage.writelines(["\n|y1="])
    for x in percentage1st:
        percentage.write(f"{x},")

    percentage.writelines(["\n|y2="])
    for x in percentage2nd:
        percentage.write(f"{x},")

    percentage.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] website.</div>"])
    percentage.close()


def vaccinationInfobox(data):
    dateVaccination = data.loc[(data['Croisement'] == 'RSS99'), 'ï»¿Date']
    totalDoses2nd = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_2_n']
    totalDosesTotal = data.loc[(data['Croisement'] == 'RSS99'), 'vac_cum_tot_n']
    percentage1st = data.loc[(data['Croisement'] == 'RSS99'), 'cvac_cum_tot_1_p']

    refs = ["<ref name=\"inspqVacc\">{{cite web |title=Données de " \
            "vaccination contre la COVID-19 au Québec " \
            "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination |website=INSPQ " \
            "|publisher=Gouvernement |access-date=2021-03-19|language=fr}}</ref>",
            "<ref name=\"inspqVacc\"/>"
            ]

    vaxPathName = "infoboxes/vaccination.txt"
    vaxFile = openFile(vaxPathName)

    currentDate = datetime.strftime(dateVaccination.iloc[-1], '%B %d, %Y')
    currentDate = smallDate(currentDate)

    totalAdministered = f"'''{int(totalDosesTotal.iloc[-1]):,}''' doses administered {currentDate}{refs[0]}<br>"
    total2Administered = f"'''{int(totalDoses2nd.iloc[-1]):,}''' second doses administered {currentDate}{refs[1]}"
    participants = createAttribute("participants", totalAdministered + total2Administered)

    outcome1 = f"'''{float(percentage1st.iloc[-1]):.1f}%''' of the population has received at least one dose of a vaccine {currentDate}{refs[1]}"
    outcome = createAttribute("outcome", outcome1)

    infobox = [participants, outcome]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}          = {attribute['value']}\n"

    vaxFile.write(text)
    vaxFile.close()

    vaccinationPiechart(dateVaccination.iloc[-1], percentage1st.iloc[-1], totalDoses2nd.iloc[-1])


def vaccinationPiechart(dateVaccination, percentage1st, totalDoses2nd):
    quebecPopulation = 8585523  # Stats Can estimate Q2 2021

    currentDate = datetime.strftime(dateVaccination, '%B %d, %Y')

    vaxPathName = "infoboxes/PiechartQuebecVaccination.txt"
    vaxFile = openFile(vaxPathName)

    # Calculations for piechart

    unvaccinated = int(((100 - float(percentage1st)) / 100) * quebecPopulation)
    unvaccinatedPercentage = round((unvaccinated / quebecPopulation) * 100, 1)

    oneDose = int(((float(percentage1st) / 100) * quebecPopulation) - int(totalDoses2nd))
    oneDosePercentage = round((oneDose / quebecPopulation) * 100, 1)

    secondDosePercentage = round(float(percentage1st) - oneDosePercentage, 1)

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

    infobox = [caption, ref, label1, value1, color1, label2, value2, color2, label3, value3, color3]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}              = {attribute['value']}\n"

    vaxFile.write(text)
    vaxFile.close()


if __name__ == "__main__":
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
    quebecCasesCSV = open("covid19-hist.csv", "r")

    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv', "vaccination.csv")
    vaccinationsCSV = open("vaccination.csv", "r")

    mainData = readCSVpandas(quebecCasesCSV, range(1, 1429))
    vData = readCSVpandas(vaccinationsCSV, range(0, 0))

    quebecGraphs(mainData)
    quebecInfobox(mainData, vData)

    montrealGraphs(mainData)
    montrealInfobox(mainData, vData)

    vaccinationGraphs(vData)
