# Description of Program: Takes a file of flights and reads it into a list of cities and a dictionary of all of the cities with their connections and its prices.
# Defined a few getters, a string function, a function that returns a list of direct connections to a given city, a function that gets a route between two cities recursively with a helper,
# and two functions to find the price of a route given a route list or two cities.

import os.path

class Flights:
    def __init__(self):
        fName=input("Enter a file name: ")
        if not os.path.isfile(fName):
            print("Cannot find file: ",fName)
            return

        self.__cities = None
        self.__flights = {}
        
        infile=open(fName)
        line = infile.readline()
        
        lStrip = line.strip()
        self.__cities=lStrip.split(', ')

        line = infile.readline()

        for city in self.__cities:
            self.__flights[city]=[]
            
        while line:
            lStrip = line.strip()
            flightInfo =lStrip.split(', ')

            city1= flightInfo[0]
            city2= flightInfo[1]
            price= int(flightInfo[2])

            if city1 in self.__flights:
                city_list= self.__flights.get(city1)
                city_list.append((city2, price))
                self.__flights[city1]= city_list
            else:
                self.__flights[city1]=[(city2, price)]

            if city2 in self.__flights:
                city_list= self.__flights.get(city2)
                city_list.append((city1, price))
                self.__flights[city2]= city_list
            else:
                self.__flights[city2]=[(city1, price)] 
                
            line=infile.readline()
        
        infile.close()
        return

    def getCities(self):
        return self.__cities

    def getFlights(self):
        return self.__flights

    def __str__(self):
        output=""
        for city in self.__cities:
            output+= "  "+str((city, self.__flights.get(city)))+"\n"
        return "Cities: "+str(self.__cities)+"\nFlights: \n"+str(output)

    def getNeighboringCities(self,city):
        if city in self.__cities:
            neighbors = self.__flights[city]
            neighborList = []
            for neighbor in neighbors:
                neighborList= [neighbor[0]] + neighborList
            return neighborList
        else:
            print("City "+city+" not found")
         
    def getRoute(self, startCity, endCity):
        if startCity in self.__cities and endCity in self.__cities:
            return self.getRouteHelper(startCity, endCity, set())
        else:
            if startCity not in self.__cities:
                print("City",startCity,"not found")
            else:
                print("City",endCity,"not found")

    def getRouteHelper(self, startCity, endCity, visitedCities=set()):
        if startCity == endCity:
            return [startCity]
        else:
            visitedCities.add(startCity)
            for city in self.getNeighboringCities(startCity):
                if city in visitedCities:
                    continue
                else:
                    temp= self.getRouteHelper(city, endCity, visitedCities)
                    if len(temp) > 0:
                        return [startCity]+temp
            return []
        
    def getRoutePrice(self, route):
        routePrice=0
        if route == []:
            return -1
        else:
            for i in range(len(route)-1):
                startCity= route[i]
                endCity=route[i+1]

                for j in self.__flights[startCity]:
                    if j[0] == endCity:
                        routePrice+=j[1]

            return routePrice

    def getPrice(self, cityA, cityB):
        if cityA in self.__cities and cityB in self.__cities:
            t= self.getRoute(cityA,cityB)
            if len(t)>0:
                return self.getRoutePrice(t)
            else:
                return 0
        else:
            if cityA not in self.__cities:
                print("City",cityA,"not found")
            else:
                print("City",cityB,"not found")
        return
