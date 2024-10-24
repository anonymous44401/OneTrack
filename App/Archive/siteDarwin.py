from nredarwin.webservice import DarwinLdbSession
from dotenv import load_dotenv

import os

class Darwin():
    def __init__(self):
        load_dotenv()
        self.__api_token = os.getenv('API_TOKEN')

        self.darwin_runner = DarwinLdbSession(wsdl = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key = str(self.__api_token))
        #self.darwin_runner = DarwinLdbSession(wsdl = "realtime.nationalrail.co.uk", api_key = self.__api_token)
        

    def get_dep_board(self, code):
        #print(code)
        self.code = str(code).upper()
        #print("Here A")

        if self.code != "NONE" and self.code != "":
            self.board = self.darwin_runner.get_station_board(self.code, rows = 20) 

            #print("Here B")
            self.dep_board = []
            self.etd = "00:00"
            #x = 0
            #print(self.x, "Here")


            for service in self.board.train_services:
                #x +=1

                self.platform = str(service.platform)

                if self.platform == "None" and str(service.etd) == "Cancelled":
                    self.platform = ""

                elif self.platform == "None" and str(service.etd) != "Cancelled":
                    self.platform = "TBC"

                
                if str(service.etd) == "Delayed":
                    self.etd = str(service.etd)

                elif str(service.etd) != "On time" and str(service.etd) != "Cancelled":
                    self.etd  = "Exp " + str(service.etd)
                    
                else:
                    self.etd  = str(service.etd)

                

                self.dep_board.append([str(service.std), str(service.destination_text), str(self.platform), str(self.etd)])
                #print(x, self.dep_board)

            return self.dep_board
        else:
            return "None"

        
    def get_advanced_dep_board(self, code):
        #print(code)
        self.code = str(code).upper()
        #print("Here A")

        if self.code != "NONE":
            self.board = self.darwin_runner.get_station_board(self.code) 

            #print("Here B")
            self.dep_board = []
            self.etd = "00:00"
            x = 0
            #print(self.x, "Here")


            for service in self.board.train_services:
                x +=1

                self.platform = str(service.platform)

                if self.platform == "None" and str(service.etd) == "Cancelled":
                    self.platform = ""

                elif self.platform == "None" and str(service.etd) != "Cancelled":
                    self.platform = "TBC"

                
                if str(service.etd) == "Delayed":
                    self.etd = str(service.etd)

                elif str(service.etd) != "On time" and str(service.etd) != "Cancelled":
                    self.etd  = "Exp " + str(service.etd)
                    
                else:
                    self.etd  = str(service.etd)

                

                self.dep_board.append([str(service.std), str(service.destination_text), str(service.operator_code), str(self.platform), str(self.etd)])
                #print(x, self.depBoard)

            print(self.dep_board)
            return self.dep_board
        else:
            return "None"