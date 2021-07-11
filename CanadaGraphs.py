import requests
import re
from os import path
from datetime import date
import datetime


def computeAverage(lst):
    return sum(lst) / len(lst)


# Download and save file
r = requests.get("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv", allow_redirects=True)
open("covid19-download.csv", 'wb').write(r.content)

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
                  "|xAxisFormat=%m-%Y\n",
                  "|xType=date\n",
                  "|xAxisTitle=Date\n",
                  "|yAxisMin=0\n",
                  "|xAxisAngle=-40\n",
                  "|x="
                  ])
cases.close()


def westernCanada():
    canadaCSV = open("covid19-download.csv", "r")
    canadaCSV.readline()  # Skip first line

    dates = []

    newCasesAB = []
    newCasesBC = []
    newCasesSK = []
    newCasesMB = []

    movingAverageBC = []
    movingAverageAB = []
    movingAverageSK = []
    movingAverageMB = []

    provinceFlags = [0, 0, 0, 0]

    dateCurrent = datetime.datetime(2020, 1, 31)

    # Parse file
    for x in canadaCSV:
        line = re.split(',', x)

        if not line[0]:
            break

        province = line[1]

        # Check if date was even there
        if province == 'Canada':
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateCurrent += datetime.timedelta(days=1)  # Increment day
            # Check if all provinces were accounted for
            if provinceFlags[0] == 0:
                newCasesBC.append(0)
            if provinceFlags[1] == 0:
                newCasesAB.append(0)
            if provinceFlags[2] == 0:
                newCasesSK.append(0)
            if provinceFlags[3] == 0:
                newCasesMB.append(0)
            continue

        if line[3] != dateCurrent.strftime("%Y-%m-%d"):
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateA = datetime.datetime.strptime(line[3], "%Y-%m-%d")
            difference = abs((dateA - dateCurrent).days)
            for l in range(difference):
                dateCurrent += datetime.timedelta(days=1)  # Increment day
                dates.append(dateCurrent.strftime("%Y-%m-%d"))
                newCasesAB.append(0)
                newCasesBC.append(0)
                newCasesSK.append(0)
                newCasesMB.append(0)

        # Add provincial data
        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'British Columbia':
            provinceFlags[0] = 1
            newCasesBC.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Alberta':
            provinceFlags[1] = 1
            newCasesAB.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Saskatchewan':
            provinceFlags[2] = 1
            newCasesSK.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Manitoba':
            provinceFlags[3] = 1
            newCasesMB.append(int(line[15]))

    # Calculate 7-day moving average
    i = 0
    j = 7

    for iterate in range(len(newCasesBC)):
        if len(newCasesBC[i:j]) == 7:
            movingAverageBC.append(computeAverage(newCasesBC[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesAB)):
        if len(newCasesAB[i:j]) == 7:
            movingAverageAB.append(computeAverage(newCasesAB[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesSK)):
        if len(newCasesSK[i:j]) == 7:
            movingAverageSK.append(computeAverage(newCasesSK[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesMB)):
        if len(newCasesMB[i:j]) == 7:
            movingAverageMB.append(computeAverage(newCasesMB[i:j]))
            i += 1
            j += 1

    # Write to file
    writeData = open("CanadaCases.txt", "a")

    for x in dates:
        writeData.write(x + ",")

    writeData.writelines(["\n|yAxisTitle=New cases by province and territory\n", "|y1="])
    for x in movingAverageBC:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y1Title=British Columbia\n", "|y2="])
    for x in movingAverageAB:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y2Title=Alberta\n", "|y3="])
    for x in movingAverageSK:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y3Title=Saskatchewan\n", "|y4="])
    for x in movingAverageMB:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y4Title=Manitoba\n",
                          "|yGrid= |xGrid=\n",
                          "}}\n",
                          "<div style=\"text-align:center\">\n",
                          "{{legend_inline|#1f77b4|British Columbia}}\n",
                          "{{legend_inline|#ff7f0e|Alberta}}\n",
                          "{{legend_inline|#2ca02c|Saskatchewan}}\n",
                          "{{legend_inline|#ff9896|Manitoba}}",
                          "</div>"
                          ])

    writeData.close()
    canadaCSV.close()


def centralCanada():
    canadaCSV = open("covid19-download.csv", "r")
    canadaCSV.readline()  # Skip first line

    writeData = open("CanadaCases.txt", "a")
    writeData.writelines(["<br><div style=\"text-align:center\">'''Central Canada'''</div>\n",
                          "{{#invoke:Graph:Chart|\n",
                          "|width=700\n",
                          "|type=line\n",
                          "|linewidth=1\n",
                          "|colors=#1f77b4,#ff7f0e,#2ca02c,#ff9896\n",
                          "|xAxisFormat=%m-%Y\n",
                          "|xType=date\n",
                          "|xAxisTitle=Date\n",
                          "|yAxisMin=0\n",
                          "|xAxisAngle=-40\n",
                          "|x="
                          ])

    dates = []

    newCasesON = []
    newCasesQC = []

    movingAverageON = []
    movingAverageQC = []

    provinceFlags = [0, 0]

    dateCurrent = datetime.datetime(2020, 1, 31)

    # Parse file
    for x in canadaCSV:
        line = re.split(',', x)

        if not line[0]:
            break

        province = line[1]

        # Check if date was even there
        if province == 'Canada':
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateCurrent += datetime.timedelta(days=1)  # Increment day
            # Check if all provinces were accounted for
            if provinceFlags[0] == 0:
                newCasesON.append(0)
            if provinceFlags[1] == 0:
                newCasesQC.append(0)
            continue

        if line[3] != dateCurrent.strftime("%Y-%m-%d"):
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateA = datetime.datetime.strptime(line[3], "%Y-%m-%d")
            difference = abs((dateA - dateCurrent).days)
            for l in range(difference):
                dateCurrent += datetime.timedelta(days=1)  # Increment day
                dates.append(dateCurrent.strftime("%Y-%m-%d"))
                newCasesON.append(0)
                newCasesQC.append(0)

        # Add provincial data
        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Ontario':
            provinceFlags[0] = 1
            newCasesON.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Quebec':
            provinceFlags[1] = 1
            newCasesQC.append(int(line[15]))

    # Calculate 7-day moving average
    i = 0
    j = 7

    for iterate in range(len(newCasesON)):
        if len(newCasesON[i:j]) == 7:
            movingAverageON.append(computeAverage(newCasesON[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesQC)):
        if len(newCasesQC[i:j]) == 7:
            movingAverageQC.append(computeAverage(newCasesQC[i:j]))
            i += 1
            j += 1

    # Write to file
    for j in dates:
        print(j)

    for x in dates:
        writeData.write(x + ",")

    writeData.writelines(["\n|yAxisTitle=New cases by province and territory\n", "|y1="])
    for x in movingAverageON:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y1Title=Ontario\n", "|y2="])
    for x in movingAverageQC:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y2Title=Quebec\n",
                          "|yGrid= |xGrid=\n",
                          "}}\n",
                          "<div style=\"text-align:center\">\n",
                          "{{legend_inline|#1f77b4|Ontario}}\n",
                          "{{legend_inline|#ff7f0e|Quebec}}\n",
                          "</div>"
                          ])

    writeData.close()
    canadaCSV.close()


def atlanticCanada():
    canadaCSV = open("covid19-download.csv", "r")
    canadaCSV.readline()  # Skip first line

    writeData = open("CanadaCases.txt", "a")
    writeData.writelines(["<br><div style=\"text-align:center\">'''Atlantic Canada'''</div>\n",
                          "{{#invoke:Graph:Chart|\n",
                          "|width=700\n",
                          "|type=line\n",
                          "|linewidth=1\n",
                          "|colors=#1f77b4,#ff7f0e,#2ca02c,#ff9896\n",
                          "|xAxisFormat=%m-%Y\n",
                          "|xType=date\n",
                          "|xAxisTitle=Date\n",
                          "|yAxisMin=0\n",
                          "|xAxisAngle=-40\n",
                          "|x="
                          ])

    dates = []

    newCasesNB = []
    newCasesPEI = []
    newCasesNS = []
    newCasesNL = []

    movingAverageNB = []
    movingAveragePEI = []
    movingAverageNS = []
    movingAverageNL = []

    provinceFlags = [0, 0, 0, 0]

    dateCurrent = datetime.datetime(2020, 1, 31)

    # Parse file
    for x in canadaCSV:
        line = re.split(',', x)

        if not line[0]:
            break

        province = line[1]

        # Check if date was even there
        if province == 'Canada':
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateCurrent += datetime.timedelta(days=1)  # Increment day
            # Check if all provinces were accounted for
            if provinceFlags[0] == 0:
                newCasesNB.append(0)
            if provinceFlags[1] == 0:
                newCasesPEI.append(0)
            if provinceFlags[2] == 0:
                newCasesNS.append(0)
            if provinceFlags[3] == 0:
                newCasesNL.append(0)
            continue

        if line[3] != dateCurrent.strftime("%Y-%m-%d"):
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateA = datetime.datetime.strptime(line[3], "%Y-%m-%d")
            difference = abs((dateA - dateCurrent).days)
            for l in range(difference):
                dateCurrent += datetime.timedelta(days=1)  # Increment day
                dates.append(dateCurrent.strftime("%Y-%m-%d"))
                newCasesPEI.append(0)
                newCasesNB.append(0)
                newCasesNS.append(0)
                newCasesNL.append(0)

        # Add provincial data
        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'New Brunswick':
            provinceFlags[0] = 1
            newCasesNB.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Prince Edward Island':
            provinceFlags[1] = 1
            newCasesPEI.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Nova Scotia':
            provinceFlags[2] = 1
            newCasesNS.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Newfoundland and Labrador':
            provinceFlags[3] = 1
            newCasesNL.append(int(line[15]))

    # Calculate 7-day moving average
    i = 0
    j = 7

    for iterate in range(len(newCasesNB)):
        if len(newCasesNB[i:j]) == 7:
            movingAverageNB.append(computeAverage(newCasesNB[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesPEI)):
        if len(newCasesPEI[i:j]) == 7:
            movingAveragePEI.append(computeAverage(newCasesPEI[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesNS)):
        if len(newCasesNS[i:j]) == 7:
            movingAverageNS.append(computeAverage(newCasesNS[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesNL)):
        if len(newCasesNL[i:j]) == 7:
            movingAverageNL.append(computeAverage(newCasesNL[i:j]))
            i += 1
            j += 1

    # Write to file

    for x in dates:
        writeData.write(x + ",")

    writeData.writelines(["\n|yAxisTitle=New cases by province and territory\n", "|y1="])
    for x in movingAverageNB:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y1Title=New Brunswick\n", "|y2="])
    for x in movingAveragePEI:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y2Title=Prince Edward Island\n", "|y3="])
    for x in movingAverageNS:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y3Title=Nova Scotia\n", "|y4="])
    for x in movingAverageNL:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y4Title=Newfoundland and Labrador\n",
                          "|yGrid= |xGrid=\n",
                          "}}\n",
                          "<div style=\"text-align:center\">\n",
                          "{{legend_inline|#1f77b4|New Brunswick}}\n",
                          "{{legend_inline|#ff7f0e|Prince Edward Island}}\n",
                          "{{legend_inline|#2ca02c|Nova Scotia}}\n",
                          "{{legend_inline|#ff9896|Newfoundland and Labrador}}",
                          "</div>"
                          ])

    writeData.close()
    canadaCSV.close()

def northernCanada():
    canadaCSV = open("covid19-download.csv", "r")
    canadaCSV.readline()  # Skip first line

    writeData = open("CanadaCases.txt", "a")
    writeData.writelines(["<br><div style=\"text-align:center\">'''Northern Canada'''</div>\n",
                          "{{#invoke:Graph:Chart|\n",
                          "|width=700\n",
                          "|type=line\n",
                          "|linewidth=1\n",
                          "|colors=#1f77b4,#ff7f0e,#2ca02c,#ff9896\n",
                          "|xAxisFormat=%m-%Y\n",
                          "|xType=date\n",
                          "|xAxisTitle=Date\n",
                          "|yAxisMin=0\n",
                          "|xAxisAngle=-40\n",
                          "|x="
                          ])

    dates = []

    newCasesYK = []
    newCasesNT = []
    newCasesNU = []

    movingAverageYK = []
    movingAverageNT = []
    movingAverageNU = []

    provinceFlags = [0, 0, 0]

    dateCurrent = datetime.datetime(2020, 1, 31)

    # Parse file
    for x in canadaCSV:
        line = re.split(',', x)

        if not line[0]:
            break

        province = line[1]

        # Check if date was even there
        if province == 'Canada':
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateCurrent += datetime.timedelta(days=1)  # Increment day
            # Check if all provinces were accounted for
            if provinceFlags[0] == 0:
                newCasesYK.append(0)
            if provinceFlags[1] == 0:
                newCasesNT.append(0)
            if provinceFlags[2] == 0:
                newCasesNU.append(0)
            continue

        if line[3] != dateCurrent.strftime("%Y-%m-%d"):
            dates.append(dateCurrent.strftime("%Y-%m-%d"))
            dateA = datetime.datetime.strptime(line[3], "%Y-%m-%d")
            difference = abs((dateA - dateCurrent).days)
            for l in range(difference):
                dateCurrent += datetime.timedelta(days=1)  # Increment day
                dates.append(dateCurrent.strftime("%Y-%m-%d"))
                newCasesNT.append(0)
                newCasesYK.append(0)
                newCasesNU.append(0)

        # Add provincial data
        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Yukon':
            provinceFlags[0] = 1
            newCasesYK.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Northwest Territories':
            provinceFlags[1] = 1
            newCasesNT.append(int(line[15]))

        if line[3] == dateCurrent.strftime("%Y-%m-%d") and province == 'Nunavut':
            provinceFlags[2] = 1
            newCasesNU.append(int(line[15]))


    # Calculate 7-day moving average
    i = 0
    j = 7

    for iterate in range(len(newCasesYK)):
        if len(newCasesYK[i:j]) == 7:
            movingAverageYK.append(computeAverage(newCasesYK[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesNT)):
        if len(newCasesNT[i:j]) == 7:
            movingAverageNT.append(computeAverage(newCasesNT[i:j]))
            i += 1
            j += 1

    i = 0
    j = 7

    for iterate in range(len(newCasesNU)):
        if len(newCasesNU[i:j]) == 7:
            movingAverageNU.append(computeAverage(newCasesNU[i:j]))
            i += 1
            j += 1


    # Write to file

    for x in dates:
        writeData.write(x + ",")

    writeData.writelines(["\n|yAxisTitle=New cases by province and territory\n", "|y1="])
    for x in movingAverageYK:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y1Title=Yukon\n", "|y2="])
    for x in movingAverageNT:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y2Title=Northwest Territories\n", "|y3="])
    for x in movingAverageNU:
        writeData.write(str(x) + ",")

    writeData.writelines(["\n\n|y3Title=Nunavut\n",
                          "|yGrid= |xGrid=\n",
                          "}}\n",
                          "<div style=\"text-align:center\">\n",
                          "{{legend_inline|#1f77b4|Yukon}}\n",
                          "{{legend_inline|#ff7f0e|Northwest Territories}}\n",
                          "{{legend_inline|#2ca02c|Nunavut}}\n",
                          "</div>\n</div>"
                          ])

    writeData.close()
    canadaCSV.close()

westernCanada()
centralCanada()
atlanticCanada()
northernCanada()