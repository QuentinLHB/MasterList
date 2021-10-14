class MasterList:

    def __init__(self, name:str):
        self.__id = self.__GetMaxId()
        self.__name = name
        self.__items = dict()


    def getName(self):
        return self.__name

    def addItem(self, name:str, amount:int):
        if name in self.__items:
            return False
        self.__items[name] = amount
        return True

    def editItem(self, name:str, amount:int):
        if name in self.__items:
            self.__items[name] = amount
            return True
        return False

    def removeItem(self, name:str):
        if name in self.__items:
            del self.__items[name]

    def clear(self):
        self.__items.clear()

    def printItems(self):
        string = ""
        if len(self.__items) > 0:
            for item, amount in self.__items.items():
                string += f"{item} : {amount}\n"
        else:
            string += "(liste vide)"
        return string

    def getItems(self):
        return self.__items

    def isEmpty(self):
        if len(self.__items.items()) == 0:
            return True
        return False

    @staticmethod
    def __GetMaxId():
        return 0;