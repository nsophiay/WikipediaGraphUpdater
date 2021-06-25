import requests
import re
from os import path


# For the 7-day moving average computation
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

    # Open file for writing
    if path.exists("MontrealNewCases.txt"):
        montrealCases = open("MontrealNewCases.txt", "w")
    else:  # Create file if it doesn't exist
        montrealCases = open("MontrealNewCases.txt", "x")

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
    montrealCases = open("MontrealNewCases.txt", "a")
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


# Generate all files
montreal()
quebec()
