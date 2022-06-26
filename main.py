import requests
import re
from os import path
import os
from datetime import datetime, timedelta

fileDir = os.path.dirname(os.path.realpath('__file__'))

# If running program on a weekend, set date to the last Friday
if datetime.now().weekday() == 5:
    todaysDate = datetime.now() - timedelta(days=1)
elif datetime.now().weekday() == 6:
    todaysDate = datetime.now() - timedelta(days=2)
else:  # Otherwise set to today's date
    todaysDate = datetime.now()

offset = (datetime.now().weekday() - 1) % 7
mtlDate = datetime.now() - timedelta(days=offset)
mtlDate = f'{mtlDate:%B} {mtlDate.day}, {mtlDate.year}'  # Format date
todaysDate = f'{todaysDate:%B} {todaysDate.day}, {todaysDate.year}'
mainRef = "<ref name=\"auto6\"/>"

# Figure out how better to do this later
dates = []

cases = []
casesMTL = []

activeCases = []
activeCasesMTL = []

newCases = []
newCasesMTL = []

dateDeaths = []
deaths = []
deathsTotal = []
deathsMTL = []

hospitalizations = []

percentage1st = []
percentage1stMTL = []
percentage2nd = []
percentage2ndMTL = []

dateVaccination = []

dailyDoses1st = []
dailyDoses2nd = []
dailyDoses3rd = []
dailyDosesTotal = []

totalDoses1st = []
totalDoses2nd = []
totalDoses3rd = []
totalDosesTotal = []

# Helper function to compute the average of a list
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


def readCSV(csv):
    csv.readline()  # Skip first line

    casesFlag = False
    deathsFlag = False
    hospitalizationsFlag = False

    # Parse file
    for x in csv:
        line = re.split(',', x)
        if (not line[0]) or (len(line) <= 1):
            break

        if (not casesFlag) and (line[0] == '2020-02-24'):
            casesFlag = True

        if (not deathsFlag) and (line[0] == '2020-03-15'):
            deathsFlag = True

        if (not hospitalizationsFlag) and (line[0] == '2020-04-10'):
            hospitalizationsFlag = True

        # Gather data and add to arrays
        if casesFlag and (line[2] == "RSS99"):
            dates.append(line[0])  # Add dates into array
            newCases.append(int(line[11]))  # Add new cases into array
            cases.append(int(line[6]))
            activeCases.append(int(line[12]))
        elif casesFlag and (line[2] == "RSS06"):
            newCasesMTL.append(int(line[11]))  # Add new cases into array
            casesMTL.append(int(line[6]))
            activeCasesMTL.append(int(line[12]))

        if hospitalizationsFlag and (line[2] == "RSS99") and line[44] != '.':
            hospitalizations.append(int(line[44]))

        if deathsFlag and (line[1] == 'Sexe') and (line[2] == 'TOT'):
            dateDeaths.append(line[0])  # Add dates into array
            deaths.append(line[25])  # Add deaths into array
            deathsTotal.append(int(line[18]))
        elif deathsFlag and (line[2] == "RSS06"):
            deathsMTL.append(int(line[18]))

def montreal():
    montrealGraphs()
    montrealInfobox()

def montrealGraphs():

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
        montrealCases.write(x + ",")

    montrealCases.writelines(["\n|yAxisTitle=New Cases\n", "|y1="])
    for x in newCasesMTL:
        montrealCases.write(f"{x},")

    montrealCases.writelines(["\n\n|y1Title=New cases per day\n",
                              "|yGrid= |xGrid=\n",
                              "}}\n",
                              "<!-- https://santemontreal.qc.ca/en/public/coronavirus-covid-19/situation-of-the-coronavirus-covid-19-in-montreal/#c43710 -->\n",
                              "<!-- Note that you should check numbers a few days back since numbers in the last few days might be increased -->"])
    montrealCases.close()

def montrealInfobox():

    MTLPathName = "infoboxes/MontrealInfobox.txt"
    MTLFile = openFile(MTLPathName)

    ref = "<ref name=\"auto6\">{{Cite web|url=https://www.inspq.qc.ca/covid-19/donnees|title=Données COVID-19 au Québec|website=INSPQ}}</ref>"

    efn = "{{efn|This figure may not represent the current epidemiological situation — the Quebec government " \
          "restricted PCR COVID-19 tests to certain vulnerable groups on January 4, 2022.}} "

    currentDate = datetime.strptime(dates[-1], '%Y-%m-%d')
    currentDate = datetime.strftime(currentDate, '%B %d, %Y')

    date = createAttribute("date", currentDate)
    confirmedCases = createAttribute("confirmed_cases", f'{casesMTL[-1]:,}{ref}')
    activeCase = createAttribute("active_cases", f'{activeCasesMTL[-1]:,}{efn}{mainRef}')
    death = createAttribute("deaths", f'{deathsMTL[-1]:,}{mainRef}')
    fatalityRate = createAttribute("fatality_rate","{{Percentage|" + str(deathsMTL[-1]) + "|" + str(casesMTL[-1]) + "|2}}")

    currentDate = datetime.strptime(dateVaccination[-1], '%Y-%m-%d')
    currentDate = datetime.strftime(currentDate, '%B %d, %Y')
    currentDate = smallDate(currentDate)

    firstDose = f"\n*'''{float(percentage1stMTL[-1]):.1f}%''' vaccinated with at least one dose {currentDate}{mainRef}"
    secondDose = f"\n*'''{float(percentage2ndMTL[-1]):.1f}%''' fully vaccinated {currentDate}{mainRef}"
    vax = createAttribute("vaccinations",firstDose+secondDose)

    infobox = [date, confirmedCases, activeCase, death, fatalityRate, vax]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}          = {attribute['value']}\n"

    MTLFile.write(text)
    MTLFile.close()


def quebec():
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
    quebecCasesCSV = open("covid19-hist.csv", "r")

    readCSV(quebecCasesCSV)

    quebecGraphs(quebecCasesCSV)
    quebecInfobox(quebecCasesCSV)


def quebecGraphs(csv):
    movingAverage = []

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

    quebecCases.writelines(["=== Quebec new cases per day ===\n",
                            "<div style=\"overflow-x:auto;>\n",
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

    quebecDeaths.writelines(["=== Quebec new deaths per day ===\n",
                             "<div style=\"overflow-x:auto;>\n",
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
        quebecCases.write(x + ",")

    quebecCases.writelines(["\n|y1Title=Daily new cases\n", "|y1="])
    for x in newCases:
        quebecCases.write(str(x) + ",")

    quebecCases.writelines(["\n|y2Title=7-day moving average\n", "|y2="])
    for x in movingAverage:
        quebecCases.write(str(x) + ",")

    quebecCases.writelines(["\n}}\n", "</div>"])
    quebecCases.close()

    quebecDeaths = open(QuebecNewDeaths, "a")

    for x in dateDeaths:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(["\n|y1Title=Deaths\n", "|y1="])
    for x in deaths:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(["\n}}\n", "</div>"])
    quebecDeaths.close()


def quebecInfobox(csv):
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

    currentDate = datetime.strptime(dates[-1], '%Y-%m-%d')
    currentDate = datetime.strftime(currentDate, '%B %d, %Y')

    date = createAttribute("date", currentDate)
    confirmedCases = createAttribute("confirmed_cases", f'{cases[-1]:,}{refs[0]}')
    activeCase = createAttribute("active_cases", f'{activeCases[-1]:,}{efn}')
    death = createAttribute("deaths", f'{deathsTotal[-1]:,}{refs[1]}')
    fatalityRate = createAttribute("fatality_rate",
                                   "{{Percentage|" + str(deathsTotal[-1]) + "|" + str(cases[-1]) + "|2}}")
    hospitalization = createAttribute("hospitalized_cases", f'{hospitalizations[-1]:,}')
    vax = createAttribute("vaccinations",
                          "\n*'''" + f'{float(percentage1st[-1]):.1f}' + "%'''   vaccinated with at least one dose " +
                          refs[2])

    infobox = [date, confirmedCases, activeCase, death, fatalityRate, hospitalization, vax]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}          = {attribute['value']}\n"

    QCFile.write(text)
    QCFile.close()


def vaccination():
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv', "vaccination.csv")
    vaccinationsCSV = open("vaccination.csv", "r")

    vaccinationGraphs(vaccinationsCSV)
    vaccinationInfobox()
    vaccinationPiechart()


def vaccinationGraphs(vaccinationsCSV):
    vaccinationsCSV.readline()  # Skip first line

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
                           "| colors= #72B8B1, #3b94a8, #196165, #929292,\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| y3Title=3rd dose\n",
                           "| y4Title= Total\n",
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
                           "| colors= #72B8B1, #3b94a8, #196165, #929292\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| y3Title=3rd dose\n",
                           "| y4Title= Total\n",
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
                           "| colors= #72B8B1, #196165, #0055ff\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           #                     "| y3Title=3rd dose\n",
                           "| yAxisTitle =  Percentage of the population vaccinated (%)\n",
                           "| x="
                           ])

    # Parse file
    for x in vaccinationsCSV:
        line = re.split(',', x)
        if (not line[0]) or (len(line) <= 1):
            break

        # Gather data and add to arrays
        if line[2] == 'RSS99':
            dateVaccination.append(line[0])  # Add dates into array

            dailyDoses1st.append(line[4])
            dailyDoses2nd.append(line[5])
            dailyDoses3rd.append(line[6])
            dailyDosesTotal.append(line[12])

            totalDoses1st.append(line[8])
            totalDoses2nd.append(line[9])
            totalDoses3rd.append(line[10])
            totalDosesTotal.append(line[13])

            percentage1st.append(line[14])
            percentage2nd.append(line[15])
        if line[2] == 'RSS06':
            percentage1stMTL.append(line[14])
            percentage2ndMTL.append(line[15])

    dailyDoses = open(DailyDoses, "a")

    for x in dateVaccination:
        dailyDoses.write(x + ",")

    dailyDoses.writelines(["\n|y1="])
    for x in dailyDoses1st:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n|y2="])
    for x in dailyDoses2nd:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n|y3="])
    for x in dailyDoses3rd:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n|y4="])
    for x in dailyDosesTotal:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv "
                           "CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] "
                           "website.</div>"])
    dailyDoses.close()

    totalDoses = open(TotalDoses, "a")

    for x in dateVaccination:
        totalDoses.write(x + ",")

    totalDoses.writelines(["\n|y1="])
    for x in totalDoses1st:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n|y2="])
    for x in totalDoses2nd:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n|y3="])
    for x in totalDoses3rd:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n|y4="])
    for x in totalDosesTotal:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] website.</div>"])
    totalDoses.close()

    percentage = open(PercentageVaccinated, "a")

    for x in dateVaccination:
        percentage.write(x + ",")

    percentage.writelines(["\n|y1="])
    for x in percentage1st:
        percentage.write(str(x) + ",")

    percentage.writelines(["\n|y2="])
    for x in percentage2nd:
        percentage.write(str(x) + ",")

    percentage.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] website.</div>"])
    percentage.close()


def vaccinationInfobox():
    refs = ["<ref name=\"inspqVacc\">{{cite web |title=Données de " \
            "vaccination contre la COVID-19 au Québec " \
            "|url=https://www.inspq.qc.ca/covid-19/donnees/vaccination |website=INSPQ " \
            "|publisher=Gouvernement |access-date=2021-03-19|language=fr}}</ref>",
            "<ref name=\"inspqVacc\"/>"
            ]

    vaxPathName = "infoboxes/vaccination.txt"
    vaxFile = openFile(vaxPathName)

    currentDate = datetime.strptime(dateVaccination[-1], '%Y-%m-%d')
    currentDate = datetime.strftime(currentDate, '%B %d, %Y')
    currentDate = smallDate(currentDate)

    totalAdministered = f"'''{int(totalDosesTotal[-1]):,}''' doses administered {currentDate}{refs[0]}<br>"
    total2Administered = f"'''{int(totalDoses2nd[-1]):,}''' second doses administered {currentDate}{refs[1]}"
    participants = createAttribute("participants", totalAdministered + total2Administered)

    outcome1 = f"'''{float(percentage1st[-1]):.1f}%''' of the population has received at least one dose of a vaccine {currentDate}{refs[1]}"
    outcome = createAttribute("outcome", outcome1)

    infobox = [participants, outcome]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}          = {attribute['value']}\n"

    vaxFile.write(text)
    vaxFile.close()


def vaccinationPiechart():
    quebecPopulation = 8585523  # Stats Can estimate Q2 2021
    currentDate = datetime.strptime(dateVaccination[-1], '%Y-%m-%d')
    currentDate = datetime.strftime(currentDate, '%B %d, %Y')

    vaxPathName = "infoboxes/PiechartQuebecVaccination.txt"
    vaxFile = openFile(vaxPathName)

    # Calculations for piechart

    unvaccinated = int(((100 - float(percentage1st[-1])) / 100) * quebecPopulation)
    unvaccinatedPercentage = round((unvaccinated / quebecPopulation) * 100, 1)

    oneDose = int(((float(percentage1st[-1]) / 100) * quebecPopulation) - int(totalDoses2nd[-1]))
    oneDosePercentage = round((oneDose / quebecPopulation) * 100, 1)

    secondDosePercentage = round(float(percentage1st[-1]) - oneDosePercentage, 1)

    caption = createAttribute("caption", f"Total number of people receiving vaccinations in Quebec as of {currentDate}")
    ref = createAttribute("ref", "https://www.inspq.qc.ca/covid-19/donnees/vaccination")

    label1 = createAttribute("label1",
                             f"Unvaccinated population: ~{unvaccinated:,} people <!-- Quebec population estimate as of Q2 2021: 8,585,523 -->")
    value1 = createAttribute("value1", unvaccinatedPercentage)
    color1 = createAttribute("color1", "#BFBFBF")

    label2 = createAttribute("label2", f" Population who has received only one dose of a vaccine: {oneDose:,} people")
    value2 = createAttribute("value2", oneDosePercentage)
    color2 = createAttribute("color2", "#42f5da")

    label3 = createAttribute("label3",
                             f" Population who has been fully vaccinated (both doses): {int(totalDoses2nd[-1]):,} people")
    value3 = createAttribute("value3", secondDosePercentage)
    color3 = createAttribute("color3", "#008")

    infobox = [caption, ref, label1, value1, color1, label2, value2, color2, label3, value3, color3]

    text = ""
    for attribute in infobox:
        text += f"| {attribute['name']}              = {attribute['value']}\n"

    vaxFile.write(text)
    vaxFile.close()


if __name__ == "__main__":
    # Generate all files
    vaccination()
    quebec()
    montreal()
