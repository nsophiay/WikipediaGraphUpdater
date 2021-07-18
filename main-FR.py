import requests
import re
from os import path
import os
from datetime import date

# Global variables

todaysDate = date.today()
todaysDate = todaysDate.strftime("%Y-%m-%d")

fileDir = os.path.dirname(os.path.realpath('__file__'))

closingStatement = "\n}}\n<div style=\"font-size:80%; line-height:1.2em;\">\n* Source: [" \
                   "https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv Fichier CSV] sur le " \
                   "site de l'[https://www.inspq.qc.ca/covid-19/donnees INSPQ] récupéré en date du " \
                   ""+todaysDate+".</div> "

closingStatementVacc = "\n}}\n<div style=\"font-size:80%; line-height:1.2em;\">\n* Source: [" \
                   "https://inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv?prout=1626376027 Fichier CSV] sur le " \
                   "site de l'[https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] récupéré en date du " \
                   ""+todaysDate+".</div> "


def downloadCSV(url, fileName):
    # Download and save file
    r = requests.get(url, allow_redirects=True)
    open(fileName, 'wb').write(r.content)


def montreal():
    montrealCasesCSV = open("covid19-hist.csv", "r")
    montrealCasesCSV.readline()  # Skip first line

    # File names
    CasQuotidiensMontreal = "Fichiers_Montreal/CasQuotidiensMontreal.txt"
    CasTotauxMontreal = "Fichiers_Montreal/CasTotauxMontreal.txt"
    DecesQuotidiensMontreal = "Fichiers_Montreal/DecesQuotidiensMontreal.txt"
    DecesTotauxMontreal = "Fichiers_Montreal/DecesTotauxMontreal.txt"

    if not path.exists("Fichiers_Montreal"):
        os.makedirs("Fichiers_Montreal")

    # Open file for writing
    if path.exists(CasQuotidiensMontreal):
        fileName = os.path.join(fileDir, CasQuotidiensMontreal)
        montrealDailyCases = open(fileName, "w")
    else:  # Create file if it doesn't exist
        fileName = os.path.join(fileDir, CasQuotidiensMontreal)
        montrealDailyCases = open(fileName, "x")

    if path.exists(CasTotauxMontreal):
        montrealTotalCases = open(CasTotauxMontreal, "w")
    else:  # Create file if it doesn't exist
        montrealTotalCases = open(CasTotauxMontreal, "x")

    # Open file for writing
    if path.exists(DecesQuotidiensMontreal):
        montrealDailyDeaths = open(DecesQuotidiensMontreal, "w")
    else:  # Create file if it doesn't exist
        montrealDailyDeaths = open(DecesQuotidiensMontreal, "x")

    if path.exists(DecesTotauxMontreal):
        montrealTotalDeaths = open(DecesTotauxMontreal, "w")
    else:  # Create file if it doesn't exist
        montrealTotalDeaths = open(DecesTotauxMontreal, "x")

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

    montrealDailyCases = open(CasQuotidiensMontreal, "a")

    for x in date:
        montrealDailyCases.write(x + ",")

    montrealDailyCases.writelines(["\n|y="])
    for x in dailyCases:
        montrealDailyCases.write(str(x) + ",")

    montrealDailyCases.writelines(closingStatement)
    montrealDailyCases.close()

    montrealTotalCases = open(CasTotauxMontreal, "a")

    for x in date:
        montrealTotalCases.write(x + ",")

    montrealTotalCases.writelines(["\n|y="])
    for x in totalCases:
        montrealTotalCases.write(str(x) + ",")

    montrealTotalCases.writelines(closingStatement)
    montrealTotalCases.close()

    montrealDailyDeaths = open(DecesQuotidiensMontreal, "a")

    for x in date:
        montrealDailyDeaths.write(x + ",")

    montrealDailyDeaths.writelines(["\n|y1="])
    for x in dailyDeaths:
        montrealDailyDeaths.write(str(x) + ",")

    montrealDailyDeaths.writelines(["\n|y2="])
    for x in dailyDeathsCHSLD:
        montrealDailyDeaths.write(str(x) + ",")

    montrealDailyDeaths.writelines(closingStatement)
    montrealDailyDeaths.close()

    montrealTotalDeaths = open(DecesTotauxMontreal, "a")

    for x in date:
        montrealTotalDeaths.write(x + ",")

    montrealTotalDeaths.writelines(["\n|y1="])
    for x in totalDeaths:
        montrealTotalDeaths.write(str(x) + ",")

    montrealTotalDeaths.writelines(["\n|y2="])
    for x in totalDeathsCHSLD:
        montrealTotalDeaths.write(str(x) + ",")

    montrealTotalDeaths.writelines(closingStatement)
    montrealTotalDeaths.close()


def quebec():
    quebecCasesCSV = open("covid19-hist.csv", "r")

    quebecCasesCSV.readline()  # Skip first line
    
    # File names
    CasQuotidiensQuebec = "Fichiers_Quebec/CasQuotidiensQuebec.txt"
    CasTotauxQuebec = "Fichiers_Quebec/CasTotauxQuebec.txt"
    DecesQuotidiensQuebec = "Fichiers_Quebec/DecesQuotidiensQuebec.txt"
    DecesTotauxQuebec = "Fichiers_Quebec/DecesTotauxQuebec.txt"

    if not path.exists("Fichiers_Quebec"):
        os.makedirs("Fichiers_Quebec")

    # Open file for writing
    if path.exists(CasQuotidiensQuebec):
        quebecCases = open(CasQuotidiensQuebec, "w")
    else:  # Create file if it doesn't exist
        quebecCases = open(CasQuotidiensQuebec, "x")

    if path.exists(CasTotauxQuebec):
        quebecTotalCases = open(CasTotauxQuebec, "w")
    else:  # Create file if it doesn't exist
        quebecTotalCases = open(CasTotauxQuebec, "x")

    # Open file for writing
    if path.exists(DecesQuotidiensQuebec):
        quebecDeaths = open(DecesQuotidiensQuebec, "w")
    else:  # Create file if it doesn't exist
        quebecDeaths = open(DecesQuotidiensQuebec, "x")

    # Open file for writing
    if path.exists(DecesTotauxQuebec):
        quebecTotalDeaths = open(DecesTotauxQuebec, "w")
    else:  # Create file if it doesn't exist
        quebecTotalDeaths = open(DecesTotauxQuebec, "x")

    quebecCases.writelines(["=== Cas quotidiens ===\n",
                            "{{Graph:Chart\n",
                            "|width=800\n",
                            "|xAxisTitle=Date (YYYY-MM)\n",
                            "|xType = date\n",
                            "|xAxisAngle=-40\n",
                            "|xAxisFormat=%Y-%m\n",
                            "|yGrid= 1\n",
                            "|xGrid= 1\n",
                            "|colors= #ff8000, #f0be8b\n",
                            "|yTitle=Cas quotidien\n",
                            "|yAxisTitle=Nombre de cas\n",
                            "|x = "])

    quebecTotalCases.writelines(["=== Cas totaux ===\n",
                                 "{{Graph:Chart\n",
                                 "|width=800\n",
                                 "|xAxisTitle=Date (YYYY-MM)\n",
                                 "|xType = date\n",
                                 "|xAxisAngle=-40\n",
                                 "|xAxisFormat=%Y-%m\n",
                                 "|yGrid= 1\n",
                                 "|xGrid= 1\n",
                                 "|colors= #ff8000, #f0be8b\n",
                                 "|yTitle=Cas totaux\n",
                                 "|yAxisTitle=Nombre de cas\n",
                                 "|x = "])

    quebecDeaths.writelines(["=== Décès quotidiens ===\n",
                             "{{Graph:Chart\n",
                             "|width=800\n",
                             "|xAxisTitle=Date (YYYY-MM)\n",
                             "|xType = date\n",
                             "|xAxisAngle=-40\n",
                             "|xAxisFormat=%Y-%m\n",
                             "|yGrid= 1\n",
                             "|xGrid= 1\n",
                             "|colors= #ff8000, #f0be8b\n",
                             "|yAxisTitle=Décès\n",
                             "| y1Title=Décès quotidien\n",
                             "| y2Title=Décès quotidien CHSLD\n",
                             "| type=line\n",
                             "| legend=Légende\n",
                             "|x = "])

    quebecTotalDeaths.writelines(["=== Décès totaux ===\n",
                                  "{{Graph:Chart\n",
                                  "|width=800\n",
                                  "|xAxisTitle=Date (YYYY-MM)\n",
                                  "|xType = date\n",
                                  "|xAxisAngle=-40\n",
                                  "|xAxisFormat=%Y-%m\n",
                                  "|yGrid= 1\n",
                                  "|xGrid= 1\n",
                                  "|colors= #ff8000, #f0be8b\n",
                                  "|yAxisTitle=Décès\n",
                                  "| y1Title=Totaux\n",
                                  "| y2Title=CHSLD\n",
                                  "| type=area\n",
                                  "| legend=Légende\n",
                                  "|x = "])

    date = []
    dateDeaths = []
    newCases = []
    totalCases = []

    deaths = []
    totalDeaths = []
    deathsCHSLD = []
    totalDeathsCHSLD = []

    casesFlag = False
    deathsFlag = False

    # Parse file
    for x in quebecCasesCSV:
        line = re.split(',', x)
        if (not line[0]) or (len(line) <= 1):
            break

        if line[0] == 'Date inconnue':
            continue

        # Gather data and add to arrays
        if (line[1] == 'Sexe') and (line[2] == 'TOT'):
            date.append(line[0])  # Add dates into array
            newCases.append(int(line[11]))  # Add new cases into array
            totalCases.append(int(line[6]))  # Add new cases into array

            deaths.append(line[25])
            deathsCHSLD.append(line[26])
            totalDeaths.append(line[18])
            totalDeathsCHSLD.append(line[21])

    # Write to file
    quebecCases = open(CasQuotidiensQuebec, "a")

    for x in date:
        quebecCases.write(x + ",")

    quebecCases.writelines(["\n|y="])
    for x in newCases:
        quebecCases.write(str(x) + ",")

    quebecCases.writelines(closingStatement)

    quebecCases.close()

    # Write to file
    quebecTotalCases = open(CasTotauxQuebec, "a")

    for x in date:
        quebecTotalCases.write(x + ",")

    quebecTotalCases.writelines(["\n|y="])
    for x in totalCases:
        quebecTotalCases.write(str(x) + ",")

    quebecTotalCases.writelines(closingStatement)
    quebecTotalCases.close()

    quebecDeaths = open(DecesQuotidiensQuebec, "a")

    for x in date:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(["\n|y1="])
    for x in deaths:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(["\n|y2="])
    for x in deathsCHSLD:
        quebecDeaths.write(x + ",")

    quebecDeaths.writelines(closingStatement)
    quebecDeaths.close()

    quebecTotalDeaths = open(DecesTotauxQuebec, "a")

    for x in date:
        quebecTotalDeaths.write(x + ",")

    quebecTotalDeaths.writelines(["\n|y1="])
    for x in totalDeaths:
        quebecTotalDeaths.write(x + ",")

    quebecTotalDeaths.writelines(["\n|y2="])
    for x in totalDeathsCHSLD:
        quebecTotalDeaths.write(x + ",")

    quebecTotalDeaths.writelines(closingStatement)
    quebecTotalDeaths.close()


def vaccinations():
    vaccinationsCSV = open("vaccination.csv", "r")

    vaccinationsCSV.readline()  # Skip first line

    # File names
    DosesQuotidiennes = "Fichiers_Vaccination/DosesQuotidiennes.txt"
    DosesTotales = "Fichiers_Vaccination/DosesTotales.txt"
    PourcentageVaccine = "Fichiers_Vaccination/PourcentageVacciné.txt"

    if not path.exists("Fichiers_Vaccination"):
        os.makedirs("Fichiers_Vaccination")

    # Open file for writing
    if path.exists(DosesQuotidiennes):
        dailyDoses = open(DosesQuotidiennes, "w")
    else:  # Create file if it doesn't exist
        dailyDoses = open(DosesQuotidiennes, "x")

    # Open file for writing
    if path.exists(DosesTotales):
        totalDoses = open(DosesTotales, "w")
    else:  # Create file if it doesn't exist
        totalDoses = open(DosesTotales, "x")

    # Open file for writing
    if path.exists(PourcentageVaccine):
        percentage = open(PourcentageVaccine, "w")
    else:  # Create file if it doesn't exist
        percentage = open(PourcentageVaccine, "x")

    dailyDoses.writelines(["=== Doses quotidiennes  ===\n",
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
                           "| legend=Légende\n",
                           "| y1Title=1ere dose\n",
                           "| y2Title=2e dose\n",
                           "| y3Title= Total\n",
                           "| yAxisTitle = Nombre de doses\n",
                           "| x="
                           ])

    totalDoses.writelines(["=== Doses totales ===\n",
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
                           "| legend=Légende\n",
                           "| y1Title=1ere dose\n",
                           "| y2Title=2e dose\n",
                           "| y3Title= Total\n",
                           "| yAxisTitle = Nombre cumulatif de doses\n",
                           "| x="
                           ])
    percentage.writelines(["=== Pourcentage de la population vaccinée ===\n",
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
                           "| y1Title=1 dose\n",
                           "| y2Title=2 doses\n",
                           "| yAxisTitle =  Pourcentage de la population vaccinée  (%)\n",
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

    dailyDoses = open(DosesQuotidiennes, "a")

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

    dailyDoses.writelines(closingStatementVacc)
    dailyDoses.close()

    totalDoses = open(DosesTotales, "a")

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

    totalDoses.writelines(closingStatementVacc)
    totalDoses.close()

    percentage = open(PourcentageVaccine, "a")

    for x in date:
        percentage.write(x + ",")

    percentage.writelines(["\n|y1="])
    for x in percentage1st:
        percentage.write(str(x) + ",")

    percentage.writelines(["\n|y2="])
    for x in percentage2nd:
        percentage.write(str(x) + ",")

    percentage.writelines(closingStatementVacc)
    percentage.close()


downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
# Generate all files
montreal()
quebec()
vaccinations()