import requests
import re
from os import path
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))


# Helper function to compute the average of a list
def computeAverage(lst):
    return sum(lst) / len(lst)


def downloadCSV(url, fileName):
    # Download and save file
    r = requests.get(url, allow_redirects=True)
    open(fileName, 'wb').write(r.content)


def montreal():
    downloadCSV('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/courbe.csv',
                "courbe.csv")
    montrealCasesCSV = open("courbe.csv", "r")
    montrealCasesCSV.readline()  # Skip first line

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

    date = []
    newCases = []
    totalCases = []

    # Parse file
    for x in montrealCasesCSV:
        line = re.split(';', x)
        if not line[0]:
            break
        # Gather data
        date.append(line[0])
        newCases.append(line[1])
        totalCases.append(line[2])

    # Write to file
    montrealCases = open(MontrealNewCases, "a")
    for x in date:
        montrealCases.write(x + ",")

    montrealCases.writelines(["\n|yAxisTitle=New Cases\n", "|y1="])
    for x in newCases:
        montrealCases.write(x + ",")

    montrealCases.writelines(["\n\n|y1Title=New cases per day\n",
                              "|yGrid= |xGrid=\n",
                              "}}\n",
                              "<!-- https://santemontreal.qc.ca/en/public/coronavirus-covid-19/situation-of-the-coronavirus-covid-19-in-montreal/#c43710 -->\n",
                              "<!-- Note that you should check numbers a few days back since numbers in the last few days might be increased -->"])
    montrealCases.close()


def quebec():
    downloadCSV('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv', "covid19-hist.csv")
    quebecCasesCSV = open("covid19-hist.csv", "r")

    quebecCasesCSV.readline()  # Skip first line

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
    quebecCases = open(QuebecNewCases, "a")

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

    quebecDeaths = open(QuebecNewDeaths, "a")

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

    dailyDoses = open(DailyDoses, "a")

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
                           "\n* Source: [https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv "
                           "CSV file] on the [https://www.inspq.qc.ca/covid-19/donnees/vaccination INSPQ] "
                           "website.</div>"])
    dailyDoses.close()

    totalDoses = open(TotalDoses, "a")

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

    percentage = open(PercentageVaccinated, "a")

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


if __name__ == "__main__":
    # Generate all files
    montreal()
    quebec()
    vaccinations()
