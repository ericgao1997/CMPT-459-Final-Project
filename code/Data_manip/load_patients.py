# encoding: utf-8
import sys

dates = []

def readCSV(fileLocal):
    sheet = {}
    with open(fileLocal,errors='ignore') as f:
        for line in f:
            currLine = line.strip().split(',')
            for num in range(len(currLine)):
                try:
                    currLine[num] = int(currLine[num])
                except:
                    continue
            if currLine[0] in sheet:
                sheet[currLine[0]].append([currLine[1],currLine[2],currLine[4],currLine[5]])
            else:
                sheet[currLine[0]] = [[currLine[1],currLine[2],currLine[4],currLine[5]]]
                dates.append(currLine[0])
    return sheet

def main(argv):
    table = readCSV("us-counties.csv")
    print (table.keys())
    recent = dates[len(dates)-1]
    print (recent)
    state_deaths = {}
    state_sick = {}
    for county in table[recent]:
        if county[1] in state_deaths.keys():
            state_deaths[county[1]] += county[3]
            state_sick[county[1]] += county[2]
        else:
            state_deaths[county[1]] = county[3]
            state_sick[county[1]] = county[2]

    for key in state_deaths.keys():
        print (key, " cases =\t", state_sick[key])
        print (key, "deaths =\t", state_deaths[key])
    return 

if __name__=="__main__":
    main(sys.argv)