import requests
import re
from os import path
from datetime import date

todaysDate = date.today()
todaysDate = todaysDate.strftime("%Y-%m-%d")


# For the 7-day moving average computation
def computeAverage(lst):
    return sum(lst) / len(lst)


def downloadCSV(url, fileName):
    # Download and save file
    r = requests.get(url, allow_redirects=True)
    open(fileName, 'wb').write(r.content)


def montreal():
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
    montrealCasesCSV = open("covid19-hist.csv", "r")
    montrealCasesCSV.readline()  # Skip first line

    # Open file for writing
    if path.exists("CasQuotidiensMontreal.txt"):
        montrealDailyCases = open("CasQuotidiensMontreal.txt", "w")
    else:  # Create file if it doesn't exist
        montrealDailyCases = open("CasQuotidiensMontreal.txt", "x")

    if path.exists("CasTotauxMontreal.txt"):
        montrealTotalCases = open("CasTotauxMontreal.txt", "w")
    else:  # Create file if it doesn't exist
        montrealTotalCases = open("CasTotauxMontreal.txt", "x")

    # Open file for writing
    if path.exists("DecesQuotidiensMontreal.txt"):
        montrealDailyDeaths = open("DecesQuotidiensMontreal.txt", "w")
    else:  # Create file if it doesn't exist
        montrealDailyDeaths = open("DecesQuotidiensMontreal.txt", "x")

    if path.exists("DecesTotauxMontreal.txt"):
        montrealTotalDeaths = open("DecesTotauxMontreal.txt", "w")
    else:  # Create file if it doesn't exist
        montrealTotalDeaths = open("DecesTotauxMontreal.txt", "x")

    montrealDailyCases.writelines(["=== Cas quotidiens ===\n",
                                   "{{Graph:Chart\n",
                                   "| height =\n",
                                   "|width=800\n",
                                   "| xAxisTitle=Date\n",
                                   "| yAxisTitle=Cas\n",
                                   "| xType = date\n",
                                   "| xAxisAngle=-40\n",
                                   "| yGrid= 1\n",
                                   "| xGrid= 1\n",
                                   "| xAxisFormat=%Y-%m\n",
                                   "| colors= #ff8000\n",
                                   "|type=line\n",
                                   "| yTitle=Cas quotidien\n",
                                   "|x = "])

    montrealTotalCases.writelines(["=== Cas totaux ===\n",
                                   "{{Graph:Chart\n",
                                   "| height =\n",
                                   "|width=800\n",
                                   "| xAxisTitle=Date\n",
                                   "| yAxisTitle=Cas\n",
                                   "| xType = date\n",
                                   "| xAxisAngle=-40\n",
                                   "| yGrid= 1\n",
                                   "| xGrid= 1\n",
                                   "| xAxisFormat=%Y-%m\n",
                                   "| colors= #ff8000\n",
                                   "|type=line\n",
                                   "| yTitle=Cas totaux\n",
                                   "|x = "])

    montrealDailyDeaths.writelines(["=== Décès quotidiens ===\n",
                                    "{{Graph:Chart\n",
                                    "| height =\n",
                                    "|width=800\n",
                                    "| xAxisTitle=Date\n",
                                    "| xType = date\n",
                                    "| xAxisAngle=-40\n",
                                    "| yGrid= 1\n",
                                    "| xGrid= 1\n",
                                    "| xAxisFormat=%Y-%m\n",
                                    "| yAxisTitle=Décès\n",
                                    "| colors= #ff8000, #f0be8b\n",
                                    "| legend=Légende\n",
                                    "| y1Title=Décès quotidien\n",
                                    "| y2Title=Décès quotidien CHSLD\n",
                                    "|type=line\n",
                                    "|x = "])

    montrealTotalDeaths.writelines(["=== Décès totaux ===\n",
                                    "{{Graph:Chart\n",
                                    "| height =\n",
                                    "|width=800\n",
                                    "| xAxisTitle=Date\n",
                                    "| xType = date\n",
                                    "| xAxisAngle=-40\n",
                                    "| yGrid= 1\n",
                                    "| xGrid= 1\n",
                                    "| xAxisFormat=%Y-%m\n",
                                    "| yAxisTitle=Décès\n",
                                    "| colors= #ff8000, #f0be8b\n",
                                    "| legend=Légende\n",
                                    "| y1Title=Totaux\n",
                                    "| y2Title=CHSLD\n",
                                    "|type=area\n",
                                    "|x = "])

    date = []

    dailyCases = []
    totalCases = []

    dailyDeaths = []
    dailyDeathsCHSLD = []

    totalDeaths = []
    totalDeathsCHSLD = []

    # Parse file
    for x in montrealCasesCSV:
        line = re.split(',', x)
        if (not line[0]) or (len(line) <= 1):
            break

        if line[0] == 'Date inconnue':
            continue

        if line[2] == 'RSS06':
            date.append(line[0])
            dailyCases.append(line[11])
            totalCases.append(line[6])
            dailyDeaths.append(line[25])
            dailyDeathsCHSLD.append(line[26])
            totalDeaths.append(line[18])
            totalDeathsCHSLD.append(line[21])

    montrealDailyCases = open("CasQuotidiensMontreal.txt", "a")

    for x in date:
        montrealDailyCases.write(x + ",")

    montrealDailyCases.writelines(["\n|y="])
    for x in dailyCases:
        montrealDailyCases.write(str(x) + ",")

    montrealDailyCases.writelines(["\n}}\n",
                                   "<div style=\"font-size:80%; line-height:1.2em;\">",
                                   "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv Fichier CSV] sur le site de l'[https://www.inspq.qc.ca/covid-19/donnees INSPQ] récupéré en date du ",
                                   todaysDate,
                                   ".</div>"])
    montrealDailyCases.close()

    montrealTotalCases = open("CasTotauxMontreal.txt", "a")

    for x in date:
        montrealTotalCases.write(x + ",")

    montrealTotalCases.writelines(["\n|y="])
    for x in totalCases:
        montrealTotalCases.write(str(x) + ",")

    montrealTotalCases.writelines(["\n}}\n",
                                   "<div style=\"font-size:80%; line-height:1.2em;\">",
                                   "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv Fichier CSV] sur le site de l'[https://www.inspq.qc.ca/covid-19/donnees INSPQ] récupéré en date du ",
                                   todaysDate,
                                   ".</div>"])
    montrealTotalCases.close()

    montrealDailyDeaths = open("DecesQuotidiensMontreal.txt", "a")

    for x in date:
        montrealDailyDeaths.write(x + ",")

    montrealDailyDeaths.writelines(["\n|y1="])
    for x in dailyDeaths:
        montrealDailyDeaths.write(str(x) + ",")

    montrealDailyDeaths.writelines(["\n|y2="])
    for x in dailyDeathsCHSLD:
        montrealDailyDeaths.write(str(x) + ",")

    montrealDailyDeaths.writelines(["\n}}\n",
                                   "<div style=\"font-size:80%; line-height:1.2em;\">",
                                   "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv Fichier CSV] sur le site de l'[https://www.inspq.qc.ca/covid-19/donnees INSPQ] récupéré en date du ",
                                   todaysDate,
                                   ".</div>"])
    montrealDailyDeaths.close()

    montrealTotalDeaths = open("DecesTotauxMontreal.txt", "a")

    for x in date:
        montrealTotalDeaths.write(x + ",")

    montrealTotalDeaths.writelines(["\n|y1="])
    for x in totalDeaths:
        montrealTotalDeaths.write(str(x) + ",")

    montrealTotalDeaths.writelines(["\n|y2="])
    for x in totalDeathsCHSLD:
        montrealTotalDeaths.write(str(x) + ",")

    montrealTotalDeaths.writelines(["\n}}\n",
                                   "<div style=\"font-size:80%; line-height:1.2em;\">",
                                   "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv Fichier CSV] sur le site de l'[https://www.inspq.qc.ca/covid-19/donnees INSPQ] récupéré en date du ",
                                   todaysDate,
                                   ".</div>"])
    montrealTotalDeaths.close()


def quebec():
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
    quebecCasesCSV = open("covid19-hist.csv", "r")

    quebecCasesCSV.readline()  # Skip first line

    # Open file for writing
    if path.exists("QuebecNewCases.txt"):
        quebecCases = open("QuebecNewCases.txt", "w")
    else:  # Create file if it doesn't exist
        quebecCases = open("QuebecNewCases.txt", "x")

    # Open file for writing
    if path.exists("QuebecNewDeaths.txt"):
        quebecDeaths = open("QuebecNewDeaths.txt", "w")
    else:  # Create file if it doesn't exist
        quebecDeaths = open("QuebecNewDeaths.txt", "x")

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

    date = []
    dateDeaths = []
    newCases = []
    movingAverage = []
    deaths = []

    casesFlag = False
    deathsFlag = False

    # Parse file
    for x in quebecCasesCSV:
        line = re.split(',', x)
        if (not line[0]) or (len(line) <= 1):
            break

        if (not casesFlag) and (line[0] == '2020-02-24'):
            casesFlag = True

        if (not deathsFlag) and (line[0] == '2020-03-15'):
            deathsFlag = True

        # Gather data and add to arrays
        if casesFlag and (line[1] == 'Sexe') and (line[2] == 'TOT'):
            date.append(line[0])  # Add dates into array
            newCases.append(int(line[11]))  # Add new cases into array

        if deathsFlag and (line[1] == 'Sexe') and (line[2] == 'TOT'):
            dateDeaths.append(line[0])  # Add dates into array
            deaths.append(line[25])  # Add deaths into array

    # Calculate 7-day moving average
    i = 0
    j = 7

    for iterate in range(len(newCases)):
        if len(newCases[i:j]) == 7:
            movingAverage.append(computeAverage(newCases[i:j]))
            i += 1
            j += 1

    # Write to file
    quebecCases = open("QuebecNewCases.txt", "a")

    for x in date:
        quebecCases.write(x + ",")

    quebecCases.writelines(["\n|y1Title=Daily new cases\n", "|y1="])
    for x in newCases:
        quebecCases.write(str(x) + ",")

    quebecCases.writelines(["\n|y2Title=7-day moving average\n", "|y2="])
    for x in movingAverage:
        quebecCases.write(str(x) + ",")

    quebecCases.writelines(["\n}}\n", "</div>"])
    quebecCases.close()

    quebecDeaths = open("QuebecNewDeaths.txt", "a")

    for x in dateDeaths:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(["\n|y1Title=Deaths\n", "|y1="])
    for x in deaths:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(["\n}}\n", "</div>"])
    quebecDeaths.close()


def vaccinations():
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv', "vaccination.csv")
    vaccinationsCSV = open("vaccination.csv", "r")

    vaccinationsCSV.readline()  # Skip first line

    # Open file for writing
    if path.exists("DailyDoses.txt"):
        dailyDoses = open("DailyDoses.txt", "w")
    else:  # Create file if it doesn't exist
        dailyDoses = open("DailyDoses.txt", "x")

    # Open file for writing
    if path.exists("TotalDoses.txt"):
        totalDoses = open("TotalDoses.txt", "w")
    else:  # Create file if it doesn't exist
        totalDoses = open("TotalDoses.txt", "x")

    # Open file for writing
    if path.exists("PercentageVaccinated.txt"):
        percentage = open("PercentageVaccinated.txt", "w")
    else:  # Create file if it doesn't exist
        percentage = open("PercentageVaccinated.txt", "x")

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
                           "| colors= #72B8B1, #196165, #929292,\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| y3Title= Total\n",
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
                           "| colors= #72B8B1, #196165, #929292\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| y3Title= Total\n",
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
                           "| colors= #72B8B1, #196165, #929292\n",
                           "| legend=Legend\n",
                           "| y1Title=1st dose\n",
                           "| y2Title=2nd dose\n",
                           "| yAxisTitle =  Percentage of the population vaccinated (%)\n",
                           "| x="
                           ])

    date = []

    dailyDoses1st = []
    dailyDoses2nd = []
    dailyDosesTotal = []

    totalDoses1st = []
    totalDoses2nd = []
    totalDosesTotal = []

    percentage1st = []
    percentage2nd = []

    # Parse file
    for x in vaccinationsCSV:
        line = re.split(',', x)
        if (not line[0]) or (len(line) <= 1):
            break

        # Gather data and add to arrays
        if line[2] == 'RSS99':
            date.append(line[0])  # Add dates into array

            dailyDoses1st.append(line[4])
            dailyDoses2nd.append(line[5])
            dailyDosesTotal.append(line[8])

            totalDoses1st.append(line[6])
            totalDoses2nd.append(line[7])
            totalDosesTotal.append(line[9])

            percentage1st.append(line[10])
            percentage2nd.append(line[11])

    dailyDoses = open("DailyDoses.txt", "a")

    for x in date:
        dailyDoses.write(x + ",")

    dailyDoses.writelines(["\n|y1="])
    for x in dailyDoses1st:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n|y2="])
    for x in dailyDoses2nd:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n|y3="])
    for x in dailyDosesTotal:
        dailyDoses.write(str(x) + ",")

    dailyDoses.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] website.</div>"])
    dailyDoses.close()

    totalDoses = open("TotalDoses.txt", "a")

    for x in date:
        totalDoses.write(x + ",")

    totalDoses.writelines(["\n|y1="])

    for x in totalDoses1st:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n|y2="])

    for x in totalDoses2nd:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n|y3="])

    for x in totalDosesTotal:
        totalDoses.write(str(x) + ",")

    totalDoses.writelines(["\n}}\n",
                           "<div style=\"font-size:80%; line-height:1.2em;\">",
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] website.</div>"])
    totalDoses.close()

    percentage = open("PercentageVaccinated.txt", "a")

    for x in date:
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


# Generate all files
montreal()
quebec()
vaccinations()
