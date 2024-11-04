from App.siteDatabase import Database
from datetime import datetime
from dotenv import load_dotenv

import os
import requests


class Service():
    def __init__(self, trainID, operator, origin, destination, all_calling_points, start_time, colour):
        self.trainID = trainID
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.all_calling_points = all_calling_points
        self.start_time = start_time
        self.colour = colour

class Departures():
    def __init__(self, wtt_departure, terminus, platform, exp_departure, service_uid):
        self.wtt_departure = wtt_departure
        self.terminus = terminus
        self.platform = platform
        self.exp_departure = exp_departure
        self.service_uid = service_uid

# Package for communicating with the RTT API
class RTT():
    def __init__(self) -> None:  
        self.__database = Database()

        load_dotenv()
        # Get the credentials from a dotenv file
        self.__rtt_user = os.getenv('RTT_USER')
        self.__rtt_token = os.getenv('RTT_TOKEN')

        self.__location_api_url = "https://api.rtt.io/api/v1/json/search/"
        self.__service_api_url = "https://api.rtt.io/api/v1/json/service/" #https://api.rtt.io/api/v1/json/service/G54046/2024/10/17


    def _get_station_board(self, __code) -> list:
        #Gets the station departure board of a given station with CRS `code`
        
        departure_board: list = []

        search_query = self.__location_api_url + str(__code)
        response = requests.get(search_query, auth=(self.__rtt_user, self.__rtt_token))

        if response.status_code == 200:
            data_json = response.json()
            #print(data_json)

            #try:
            services = data_json["services"]
        
            #get the details of all services 
            for service in services:
                __destinations = service["locationDetail"]["destination"]
                __displayAs = service["locationDetail"]["displayAs"]
                #print(displayAs)
                __wtt_departure = service["locationDetail"]["gbttBookedDeparture"]
                try:    
                    __platform = service["locationDetail"]["platform"]
                
                except:
                    __platform = "Unknown"

                try:
                    __exp_departure = service["locationDetail"]["realtimeDeparture"]

                except:
                    __exp_departure = "Unknown"

                try:    
                    __service_uid = service["serviceUid"]
                    #print("Service UID" + str(__service_uid))
                
                except:
                    __service_uid = None


                if __displayAs != "CANCELLED_CALL":
                    if __wtt_departure == __exp_departure:
                        __exp_departure = "On time"
                        __wtt_departure = self.__format_time(__wtt_departure)

                    elif __exp_departure =="Unknown":
                        __wtt_departure = self.__format_time(__wtt_departure)

                    else:
                        __exp_departure = self.__format_time(__exp_departure)
                        __exp_departure = "Exp " + __exp_departure
                        __wtt_departure = self.__format_time(__wtt_departure)

                else:
                    __exp_departure = "Cancelled"
                    __wtt_departure = self.__format_time(__wtt_departure)
                

                #for platform in platforms:
                    #print(platform)

                for destination in __destinations:
                    __terminus = destination["description"]
                    #print(terminus)
                    #print(__wtt_departure, __terminus, __platform, __exp_departure, __service_uid)
                    departure_board.append(Departures(__wtt_departure, __terminus, __platform, __exp_departure, __service_uid))

            #print(departure_board)

            return departure_board
            
                #get 1) Booked Arrival, 2) realTimeArrival, 3) Operator, 4) Platform

            #except:
                #return "No services found"
        
        else:
            print(f"Error: {response.status_code}")
            raise ConnectionRefusedError("The API refused to connect.")


    def _get_advanced_board(self, __code): #Gets the station departure board of a given station with CRS `code`
        
        __departure_board: list = []

        __search_query = self.__location_api_url + str(__code)
        __response = requests.get(__search_query, auth=(self.__rtt_user, self.__rtt_token))

        if __response.status_code == 200:
            __data_json = __response.json()
            #print(data_json)

            __services = __data_json["services"]

            #get the details of all services 
            for service in __services:
                __destinations = service["locationDetail"]["destination"]
                __displayAs = service["locationDetail"]["displayAs"]
                #print(displayAs)
                __wtt_departure = service["locationDetail"]["gbttBookedDeparture"]
                
                try:    
                    __platform = service["locationDetail"]["platform"]
                except:
                    __platform = "Unknown"

                try:
                    __exp_departure = service["locationDetail"]["realtimeDeparture"]
                except:
                    __exp_departure = "Unknown"

                try:
                    __toc = service["atocName"]
                except:
                    __toc = "Unknown"


                if __displayAs != "CANCELLED_CALL":
                    if __wtt_departure == __exp_departure:
                        __exp_departure = "On time"

                    elif __exp_departure =="Unknown":
                        pass
                    
                    else:
                        __exp_departure = "Exp " + __exp_departure

                else:
                    __exp_departure = "Cancelled"
                

                #for platform in platforms:
                    #print(platform)

                for destination in __destinations:
                    __terminus = destination["description"]
                    #print(terminus)

                    __departure_board.append([__wtt_departure, __terminus, __toc, __platform, __exp_departure])

            #print(departure_board)

            return __departure_board
            
                #get 1) Booked Arrival, 2) realTimeArrival, 3) Operator, 4) Platform

        
        
        else:
            print(f"Error: {__response.status_code}")
            raise ConnectionRefusedError("The API refused to connect.")
        

    def _get_service_info(self, service_uid: str) -> Service:
        now = datetime.now()
        year = str(now.strftime("%Y"))
        month = str(now.strftime("%m"))
        day = str(now.strftime("%d"))

        all_calling_points: list = []

        search_query = self.__service_api_url + str(service_uid) + "/" + year + "/" + month + "/" + day
        #print(search_query)
        response = requests.get(search_query, auth=(self.__rtt_user, self.__rtt_token))

        if response.status_code == 200:
            data_json = response.json()
            #print(data_json)

            trainID = data_json["trainIdentity"]
            operator = data_json["atocName"]
            colour = self.__database._get_values("opColour", "tblOperators", "OpName", operator)
            #print(colour)
            
            origins = data_json["origin"]
            origin = origins.pop()["description"]
            start_time = "None"

            #print(origin)

            destinations = data_json["destination"]
            destination = destinations.pop()["description"]

            #print(destination)                

            calling_points = data_json["locations"]

            for locations in calling_points:
                stop_name = locations["description"]
                if "realtimeArrival" in locations:
                    expected_arrival = locations["realtimeArrival"]
                    expected_arrival = self.__format_time(expected_arrival)
                else:
                    expected_arrival = ""

                if "gbttBookedArrival" in locations:
                    booked_arrival = locations["gbttBookedArrival"]
                    booked_arrival = self.__format_time(booked_arrival)
                else:
                    booked_arrival = ""

                if "realtimeDeparture" in locations:
                    expected_departure = locations["realtimeDeparture"]
                    expected_departure = self.__format_time(expected_departure)
                else:
                    expected_departure = ""

                if "gbttBookedDeparture" in locations:
                    booked_departure = locations["gbttBookedDeparture"]
                    booked_departure = self.__format_time(booked_departure)
                else:
                    booked_departure = ""

                if start_time == "None":
                    start_time = booked_departure

                if "platform" in locations:
                    platform = locations["platform"]
                else:
                    platform = "Unknown"

                all_calling_points.append([stop_name, booked_arrival, expected_arrival, platform, booked_departure, expected_departure])
                


            return Service(trainID, operator, origin, destination, all_calling_points, start_time, colour)
            

    def __format_time(self, time: str):
        new_time = time[0] + time[1] + ":" + time[2] + time[3]
        #print(new_time)
        return new_time
    




#rtt = RTT()

#rtt._format_time("1155")
#rtt.get_station_board("MCV")

#rtt._get_service_info("G54046")