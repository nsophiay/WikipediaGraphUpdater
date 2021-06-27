import requests
import re
from os import path
from datetime import date

# Download and save file
r = requests.get("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv", allow_redirects=True)
open("covid19-download.csv", 'wb').write(r.content)
canadaCSV = open("covid19-download.csv", "r")
canadaCSV.readline()  # Skip first line

# Open file for writing
if path.exists("CanadaCases.txt"):
    cases = open("CanadaCases.txt", "w")
else:  # Create file if it doesn't exist
    cases = open("CanadaCases.txt", "x")

today = date.today()
currentDate = today.strftime("%B %d, %Y")

dateString = "<small>Updated " + currentDate + "</small><br>'''Western Canada'''</div>\n"

cases.writelines(["===Provincial and territorial===\n",
                  "<div class=\"toccolours\" style=\"display:inline-block; width:800px; margin:1em "
                  "0;\"><div style=\"text-align:center\">'''Daily new cases by province and territory ("
                  "7-day moving average)'''<br>\n",
                  dateString,
                  "{{#invoke:Graph:Chart|\n",
                  "|width=700\n",
                  "|type=line\n",
                  "|linewidth=1\n",
                  "|colors=#1f77b4,#ff7f0e,#2ca02c,#ff9896\n",
                  "|xType=date\n",
                  "|xAxisTitle=Date\n",
                  "|x="
                  ])


def westernCanada():
    dates = []
    newCasesAB = []
    newCasesBC = []
    newCasesSK = []
    newCasesMB = []

    datesNotIncluded = ["2020-"]

    # Parse file
    for x in canadaCSV:
        line = re.split(',', x)

        if not line[0]:
            break

        # Gather data
        dates.append(line[3])

        province = line[1]

        if province == 'Alberta':
            newCasesAB.append(line[15])

        if province == 'British Columbia':
            newCasesBC.append(line[15])

        if province == 'Saskatchewan':
            newCasesSK.append(line[15])

        if province == 'Manitoba':
            newCasesMB.append(line[15])

        # TO DO #
        # Manually (or figure out another way) to handle for the fact that the provinces
        # aren't listed in the CSV until they've had 1 case
        # Then do the 7-day moving average thing

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
