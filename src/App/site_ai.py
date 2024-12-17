from App.site_database import Database

from datetime import datetime


class AI():
    def __init__(self):
        self.__priority_queue = PriorityQueue(6)
        self.__database = Database()

        self.__max_suggestions = 6

    def __get_user_suggestions(self, __username):
        #raise NotImplementedError("Service unavailable")
    
        collected_suggestions = self.__database._get_values("Suggestions", "tblSearchInfo", "Username", __username)

        if len(collected_suggestions) > self.__max_suggestions:
            collected_suggestions = collected_suggestions[:6]
        
        collected_suggestions


    def __insert_new_suggestions(self, __username):
        raise NotImplementedError("Service unavailable")
    
    def _update_current_suggestions(self, __username):
        pass

    def _add_me_to_suggestions_queue():
        pass
        # adds a value to the queue for suggestions


class PriorityQueue():
    # Class for a priority queue with a static length (chosen by user upon init)
    def __init__(self, __max_length: int):
        self.__max_length: int = __max_length
        self.__queue: list = []

        for i in self.__max_length:
            self.__queue.append("")
            #print(self.__queue)


    def _add_item(self, __priority: int, __item: str) -> list | None:
        if __priority > (self.__max_length - 1) or __priority < 0:
            raise IndexError("Priority must be between 0 and", (self.__max_length - 1))

        else:
            self.__queue.insert(__priority, __item)
            self.__queue = self.__queue[:self.__max_length]
            #print(self.__queue)

    def _remove_item(self, __item) -> list | None:
        self.__queue.remove(__item)

        while len(self.__queue) != self.__max_length:
            #print(self.__queue)
            self.__queue.append("")
            #print(self.__queue)
        
        #print(self.__queue)


queue = PriorityQueue(8)

#queue._add_item(0, "KGX")
#queue._add_item(0, "LDS")
#queue._remove_item("KGX")