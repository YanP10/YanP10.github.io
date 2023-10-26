#Code to make sure the right file name is written
def openFile():
    goodFile = False
    while goodFile == False:
        fname = input("Please enter a file name: ")
        try:
            dataFile = open(fname, 'r')
            goodFile = True
        except IOError:
            print("Invalid filename try again ...")
    return dataFile
            
                
def getChoice():
    # This function displays the menu of choices for the user
    # It reads in the user's choice and returns it as an integer
    print("")
    print("Please choose one of the following options:")
    print("1 -- Find flight information by airline and flight number")
    print("2 -- Find flights shorter than a specified duration")
    print("3 -- Find the cheapest flight by a given airline")
    print("4 -- Find flight departing after a specified time")
    print("5 -- Find the average price of all flights")
    print("6 -- Write a file with flights sorted by departure time")
    print("7 -- Quit")
    choice = getOption()
    print("")
    return choice

def getOption():
#makes sure that the user actually chooses a possible option
    option = False
    while option == False:
        try:
            choice = int(input("Choice ==> "))
            if choice > 0 and choice < 8:
                option = True
                return choice
            else:
                print("Entry must be between 1 and 7")
        except:
            print("Entry must be a number")
            
def splitTime(startTime):
#Makes the time format into minutes so its easier to add/subtract, and track
    hrs1, min1 = startTime.split(':')
    hrs1 = int(hrs1)
    min1 = int(min1)
    newhrs1 = hrs1 * 60
    totalTime1 = newhrs1 + min1
    totalTIme1 = int(totalTime1)
    return totalTime1

def getName(flights):
#gets airline name from user
    name = False
    airline = input("Enter airline name: ")
    while name == False:
        if airline in flights:
            return airline
            name = True
        else:
            print("Invalid input -- try again")
            airline = input("Enter airline name: ")


def getNumber(flightNum):
#Gets airline number from user
    number = False
    flightNumber = input("Enter flight number: ")
    while number == False:
        if flightNumber in flightNum:
            return flightNumber
            number = True
        else:
            print("Invalid input -- try again")
            flightNumber = input("Enter flight number: ")

def getLim():
#get the time limit of flights from user
    limit = False
    while limit == False:
        try:
            limit = True
            timeLim = int(input("Enter maximum duration (in minutes): "))
        except:
            print("Entry must be a number")
            timeLim = int(input("Enter maximum duration (in minutes): "))
    return timeLim

def timeLimit():
#Gets earliest departure time from user
    time = False
    earliest = input("Enter earliest departure time: ")
    while time == False:
        if len(earliest) == 5 and ":" in earliest:
            try:
                h,m = earliest.split(':')
                int(h)
                int(m)
                time = True
            except ValueError:
                earliest = input("Invalid time - Try again ")
        else:
            earliest = input("Invalid time - Try again ")
    return earliest

def getFlights():
#Makes all the lists and fills them
    infile = openFile()
    flights = []
    flightNum = []
    startTime = []
    endTime = []
    cost = []
    for line in infile:
        line = line.strip()
        flight, number, start, end, price = line.split(',')
        flights.append(flight)
        flightNum.append(number)
        startTime.append(start)
        endTime.append(end)
        cost.append(price)
    infile.close
    return flights, flightNum, startTime, endTime, cost

def flightInfo(flights, flightNum, startTime, endTime, cost):
#Code for option 1, gets the flight info
    airline = getName(flights)
    flightNumber = getNumber(flightNum)
    found = 0
    i = 0
    for i in range(len(flights)):
        if flights[i] == airline and flightNum[i] == flightNumber:
            found = 1
            AIRLINE = flights[i]
            FLT = flightNum[i]
            DEPART = startTime[i]
            ARRIVE = endTime[i]
            PRICE = cost[i]
    if found == 0:
        AIRLINE = ""
        FLT = ""
            
    return AIRLINE, FLT, DEPART, ARRIVE, PRICE

def shortTime(flights, flightNum, startTime, endTime, cost):
#Code to find the shortest flights
    finalList = []
    i = 0
    j = 0
    amountTime = []
    totalTime1 = 0
    totalTime2 = 0
    finalTime = 0
    timeLim = getLim()
    for i in range(len(startTime)):
        hrs1, min1 = startTime[i].split(':')
        hrs2, min2 = endTime[i].split(':')
        hrs1 = int(hrs1)
        hrs2 = int(hrs2)
        min1 = int(min1)
        min2 = int(min2)
        newhrs1 = hrs1 * 60
        totalTime1 = newhrs1 + min1
        newhrs2 = hrs2 * 60
        totalTime2 = newhrs2 + min2
        totalTime2 = int(totalTime2)
        totalTIme1 = int(totalTime1)
        finalTime = totalTime2 - totalTime1
        amountTime.append(finalTime)
    for j in range(len(amountTime)):
        if timeLim > amountTime[j]:
            finalList.append(j)
    return finalList

def cheapestFlights(flights, flightNum, startTime, endTime, cost):
#Code to find the cheapest flights
    price = 500
    newCost= []
    specificAirline = []
    finalAirline = []
    for i in range(len(cost)):
        newCost.append(int(cost[i].replace('$',"")))
    chosenName = getName(flights)
    for i in range(len(flights)):
        if chosenName == flights[i]:
            specificAirline.append(i)
    for i in range(len(specificAirline)):
        newCost[specificAirline[i]] = int(newCost[(specificAirline[i])])
        if newCost[specificAirline[i]] < price:
            price = newCost[specificAirline[i]]
            finalAirline.append(specificAirline[i])
    return finalAirline

def specifiedTime(flights, flightNum, startTime, endTime, cost):
#Code to find the index list
    indexList = []
    earliest = timeLimit()
    for i in range(len(flights)):
        if  splitTime(startTime[i]) > splitTime(earliest):
            indexList.append(i)
            splitTime(startTime[i])
    return indexList


def avgPrice(cost):
#Code to find the average cost of all the flights
    totalCost = 0
    newCost= []
    j = 0
    for i in range(len(cost)):
        newCost.append(int(cost[i].replace('$',"")))
    for x in range(len(newCost)):
        totalCost = totalCost + newCost[x]
        j = j + 1
    avg = totalCost/j
    avg = round(avg,2)
    
    return avg

def newFile(flights, flightNum, startTime, endTime, cost):
#Code to make the new file
    indexList = sortTime(startTime)
    outfile = open("time-sorted-flights.csv",'w')
    for i in range(len(indexList)):
        outfile.write(flights[indexList[i]]+ "," + flightNum[indexList[i]]+ "," + startTime[indexList[i]] + "," + endTime[indexList[i]]+ "," + cost[indexList[i]] + '\n')
    return
def sortTime(startTime):
#Code to sort all the times for the new file
    indexList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    newList = startTime.copy()
    for i in range(1, len(newList)):
        save2 = indexList[i]
        save = newList[i]
        j = i
        while j > 0 and splitTime(str(newList[j - 1])) > splitTime(save):
            # comparison
            indexList[j] = indexList[j-1]
            newList[j] = newList[j - 1]
            j = j - 1
	    # swap
        newList[j] = save
        indexList[j] = save2
    return indexList


def main():
#Main function
    flights, flightNum, startTime, endTime, cost = getFlights()
    choice = getChoice()
    while choice != 7:
        if choice == 1:
            AIRLINE, FLT, DEPART, ARRIVE, PRICE = flightInfo(flights, flightNum, startTime, endTime, cost)
            print("The flight that meets your criteria is:")
            print("")
            print("AIRLINE  FLT#  DEPART  ARRIVE PRICE")
            print(AIRLINE," ", FLT," ", DEPART, ARRIVE," ", PRICE)
            choice = getChoice()

        elif choice == 2:
            finalList = shortTime(flights, flightNum, startTime, endTime, cost)
            if len(finalList) < 1:
                print("No flights meet your criteria")
            else:
                print("The flights that meet your criteria are: ")
                print("")
                print("AIRLINE  FLT#  DEPART  ARRIVE PRICE")
                for i in range(len(finalList)):
                    print(flights[finalList[i]]," ", flightNum[finalList[i]]," ", startTime[finalList[i]], endTime[finalList[i]]," ", cost[finalList[i]])
            choice = getChoice()


        elif choice == 3:
            finalAirline = cheapestFlights(flights, flightNum, startTime, endTime, cost)
            print("The flight that meets your criteria is:")
            print("")
            print("AIRLINE  FLT#  DEPART  ARRIVE PRICE")
            for i in range(len(finalAirline)):
                    print(flights[finalAirline[i]]," ", flightNum[finalAirline[i]]," ", startTime[finalAirline[i]], endTime[finalAirline[i]]," ", cost[finalAirline[i]])
            choice = getChoice()


        elif choice == 4:
            indexList = specifiedTime(flights, flightNum, startTime, endTime, cost)
            if len(indexList) < 1:
                print("No flights meet your criteria")
            else:
                print("")
                print("The flights that meet your criteria are:")
                print("")
                print("AIRLINE  FLT#  DEPART  ARRIVE PRICE")
                for i in range(len(indexList)):
                    print(flights[indexList[i]]," ", flightNum[indexList[i]]," ", startTime[indexList[i]], endTime[indexList[i]]," ", cost[indexList[i]])
            choice = getChoice()


        elif choice == 5:
            avg = avgPrice(cost)
            print("The average price is $ ", avg)
            choice = getChoice()


        elif choice == 6:
            newFile(flights, flightNum, startTime, endTime, cost)
            print("Sorted data has been written to file: time-sorted-flights.csv")
            choice = getChoice()


        else:
            print("Error in your choice")
            choice = getChoice()
    print("Thank you for flying with us")




