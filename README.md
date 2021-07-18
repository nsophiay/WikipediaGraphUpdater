This Python program generates text files for the graphs on the following Wikipedia articles / ce programme Python génère des fichiers .txt pour les graphiques dans ces articles de Wikipedia:
* EN
  * https://en.wikipedia.org/wiki/COVID-19_vaccination_in_Quebec
  * https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Montreal
  * https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Quebec
  * https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Canada
* FR
  * https://fr.wikipedia.org/wiki/Statistiques_sur_la_pand%C3%A9mie_de_Covid-19_au_Qu%C3%A9bec
  * https://fr.wikipedia.org/wiki/Pand%C3%A9mie_de_Covid-19_%C3%A0_Montr%C3%A9al
  * https://fr.wikipedia.org/wiki/Campagne_de_vaccination_contre_la_Covid-19_au_Qu%C3%A9bec

## HOW TO RUN / EXECUTER LE PROGRAMME

1. [Download main.exe](https://github.com/nsophiay/WikipediaGraphUpdater/raw/main/main.exe) if you are updating the graphs for any Quebec/Montreal related articles, or [CanadaGraphs.exe](https://github.com/nsophiay/WikipediaGraphUpdater/raw/main/CanadaGraphs.exe) if you are updating the graphs for *COVID-19 pandemic in Canada* / [télécharger main-FR.exe](https://github.com/nsophiay/WikipediaGraphUpdater/raw/main/main-FR.exe).
2. Double-click to run it / double-cliquer sur le fichier afin de l'exécuter.
3. Several folders should be generated in the directory in which you downloaded main.exe / de nombreux dossiers seront génerés où vous avez téléchargé main-FR.exe.
4. Go to the folder you want, select the desired text file, and press CTRL+A to select the entire file / aller au bon dossier, selectionner le fichier .txt souhaité, et appuyer sur le CTRL+A afin de selectionner le fichier entier.
5. Copy and paste the selection into the source editor in Wikipedia / copier et coller la selection dans l'éditeur de code de Wikipedia.

## DESCRIPTIONS OF TEXT FILES / DESCRIPTIONS DES FICHIERS .TXT

### Files_Montreal / Fichiers_Montreal
#### MontrealNewCases.txt / CasQuotidiensMontreal.txt
This file contains the updated graph showing daily new COVID-19 cases in Montreal / ce fichier contient le graphique qui montre les cas quotidiens à Montréal.
#### CasTotauxMontreal.txt
Ce fichier contient le graphique qui montre les cas totaux à Montréal.
#### DecesQuotidiens.txt
Ce fichier contient le graphique qui montre les décès quotidiens à Montréal.
#### DecesTotaux.txt
Ce fichier contient le graphique qui montre les décès totaux à Montréal.

### Files_Quebec / Fichiers_Quebec
#### QuebecNewCases.txt / CasQuotidiensQuebec.txt
This file contains the updated graph showing daily new COVID-19 cases in Quebec, as well as the 7-day moving average / ce fichier contient le graphique qui montre les cas quotidiens au Québec, ainsi que la moyenne mobile de 7 jours.

#### CasTotauxQuebec.txt
Ce fichier contient le graphique qui montre les cas totaux au Québec.

#### QuebecNewDeaths.txt / DecesQuotidiensQuebec.txt
This file contains the graph showing daily new COVID-19 deaths in Quebec / ce fichier contient le graphique qui montre les déces quotidiens au Québec.

#### DecesTotauxQuebec.txt
Ce fichier contient le graphique qui montre les décès totaux au Québec.

### Files_Vaccination / Fichiers_Vaccination
#### DailyDoses.txt / DosesQuotidiennes.txt
This file contains the updated graph showing daily vaccinations in Quebec, including the first, second, and total number of doses / ce fichier contient le graphique qui montre les vaccinations quotidiennes au Québec, dont la prémière, deuxième, et de doses.

#### PercentageVaccinated.txt / PourcentageVacciné.txt
This file contains the updated graph showing the percentage of the Quebec population that is vaccinated with one or two doses / ce fichier contient le graphique qui montre le pourcentage de la population vacciné au Québec avec une ou deux doses.

#### TotalDoses.txt / DosesTotales.txt
This file contains the graph showing the cumulative number of first, second, and total doses in Quebec / ce fichier contient le graphique qui montre le nombre cumulatif de prémières et deuxièmes doses au Québec.

### Files_Canada
#### CanadaCases.txt
This file contains the updated graphs showing the 7-day moving averages of daily new cases in each region of Canada / ce fichier contient les graphiques qui montrent les moyennes mobiles de nouveaux cas quotidiens dans chaque région du Canada.
