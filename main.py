# cartouche

from Model.MasterList import MasterList
import pickle
from Model import Const
import os.path


def setExportFilePath():
    pathName = ""
    if os.path.isfile(Const.PARAMETERS_FILE):
        pathName = loadPathName()
    else:
        savePathName(pathName) # Creates an empty file

    if pathName == "":
        pathName = input("Collez le chemin du dossier dans lequel sera créé le fichier d'exportation \n"
                         "ex: C:/Users/Quentin/Desktop\nRetour: 0 ou Entrée\n")
        if pathName != ("" or "0"):
            savePathName(pathName)
            print("Le nouveau chemin a bien été enregistré.")

def savePathName(pathName:str):
    with open(Const.PARAMETERS_FILE, "wb") as file:
        pickle.dump(pathName, file)

def loadPathName():
    with open(Const.PARAMETERS_FILE, "rb") as file:
        pathName = pickle.load(file)
    return pathName

def mainMenu():
    # Get user input
    while True:
        print("Menu principal :")
        if len(mlists) == 0:
            print("1: Etablir une Master List")
        else:
            print("1: Gérer les Master Lists")
        print("2: Etablir la liste de courses")
        print("3: Paramètres")
        print("0: Quitter l'application")
        choice = getIntInputFromUser(0, 3)

        # Routing
        if choice == 0:
            return
        elif choice == 1:
            consultMasterLists()
        elif choice == 2:
            newList = createListBasedOnMasterList()
        elif choice == 3:
            setExportFilePath()



def consultMasterLists():
    choice = -1
    while choice != 0:
        lengthList = len(mlists)
        printMasterLists()
        print(f"{lengthList + 1}: Créer une nouvelle liste")
        print("0: Retour au menu précédent")
        choice = getIntInputFromUser(0, lengthList + 1)
        if choice == lengthList+1:
            createNewMasterList()
        elif 1 <= choice <= lengthList:
            manageMasterList(mlists[choice-1])

def printMasterLists():
    for k in range(1, len(mlists) + 1):
        print(f"{k}: {mlists[k - 1].getName()}")


def createNewMasterList():
    name = input("Nom de la Master List: ")
    masterList = MasterList(name)
    mlists.append(masterList)
    addNewElements(masterList.getItems())
    saveMasterLists()


def manageMasterList(masterList:MasterList):
    choice = -1
    while choice != (0 and 5):
        print(f'Master List "{masterList.getName()}" actuelle :')
        print(masterList.printItems())
        print("1: Ajouter des éléments")
        print("2: Modifier des quantités")
        print("3: Supprimer des éléments")
        print("4: Vider la liste")
        print("5: Supprimer la liste")
        print("0: Retour au menu précédent")
        choice = getIntInputFromUser(0, 5)

        if choice == 1:
            addItemsToMasterList(masterList)
        elif choice == 2:
            editQuantities(masterList)
        elif choice == 3:
            removeItems(masterList)
        elif choice == 4:
            clearList(masterList)
        elif choice == 5:
            deleteList(masterList)



def getIntInputFromUser(min:int, max:int):
    while True:
        choice = input()
        try:
            choice = int(choice)
            if min <= choice <= max:
                return choice
        except:
            print("Saisie incorrecte.")

def addItemsToMasterList(masterList:MasterList):
    itemList = dict()
    itemList, change = addNewElements(itemList)
    for item, amount in itemList.items():
        masterList.addItem(item, amount)
    saveMasterLists()

def editQuantities(masterList:MasterList):
    print(masterList.printItems())
    while True:
        item = input("Saisir le nom exact de l'élément à modifier (menu précédent : 0) : ")
        if item.lower() == ("0" or "q" or "quitter"):
            return
        print("Saisir la nouvelle quantité : ")
        amount = getIntInputFromUser(1, 100)
        masterList.editItem(item, amount)
        saveMasterLists()

def removeItems(masterList:MasterList):
    print(masterList.printItems())
    while True:
        item = input("Saisir le nom exact de l'élément à supprimer (menu précédent : 0) : ")
        if item.lower() != ("0" or "q" or "quitter"):
            return
        masterList.removeItem(item)
        saveMasterLists()

def clearList(masterList:MasterList):
    masterList.clear()
    saveMasterLists()

def deleteList(masterList):
    mlists.remove(masterList)
    saveMasterLists()


def askUserForExport(list):
    choice = input("Exporter la liste au format .txt ? (o/n")
    if choice.lower() != ("n" or "q" or "0"):
        pathName = loadPathName()
        if pathName != "":
            try:
                exportList(list, pathName)
                print("Liste exportée au chemin" + pathName)
            except:
                print("Echec de l'export. Merci de vérifier le chemin dans la rubrique 'Paramètres'.")
        else:
            print("Aucun chemin enregistré.")



def createListBasedOnMasterList():
    print("Choisissez la Master List de référence :")
    printMasterLists()
    masterList = mlists[getIntInputFromUser(1, len(mlists))-1]
    allItems = masterList.getItems().items()
    newList = dict()
    for item, amountNeeded in allItems:
        ok = False
        stock = -1
        while not ok:
            stock = input(f"Combien de {item} en stock ?\n")
            try:
                stock = int(stock)
                if 0 <= stock < 50:
                    ok = True
            except:
                ok = False

        if stock < amountNeeded and amountNeeded > 0:
            newList[item] = amountNeeded - stock

    printList(newList)
    newList, change = addNewElements(newList)
    if change:
        printList(newList)
    askUserForExport(newList)
    return newList

def addNewElements(list):
    item = input("Ajouter des éléments à la liste de course ? (o/n)\n")
    if item.lower() == ("n" or "non" or "no" or "0"):
        return list, False
    change = False
    while True:
        item = input("Saisir l'élément à ajouter (Quitter : 0)\n")
        if item == ("0" or "q" or "quitter"):
            return list, change
        amount = input("Quantité :\n")
        try:
            amount = int(amount)
            list[item] = amount
            change = True
        except:
            print("L'élément n'a pas pu être ajouté : Format de quantité incorrect.")


def printList(list):
    print("Liste de courses :")
    if len(list.items()) > 0:
        for item, amountToBuy in list.items():
            print(f"{item} : {amountToBuy}")
    else:
        print("(liste vide)")

def saveMasterLists():
    file = open(Const.DATA_FILE, "wb")
    pickle.dump(mlists, file)
    file.close()

def loadMasterList():
    if os.path.isfile(Const.DATA_FILE):
        file = open(Const.DATA_FILE, "rb")
        mlists = pickle.load(file)
        file.close()
        return mlists
    else:
        file = open(Const.DATA_FILE, "wb")
        mlists = []
        pickle.dump(mlists, file)
        file.close()
        return mlists

def exportList(masterList:MasterList, path:str):
    if not os.path.exists(path):
        os.makedirs(path)

    filename = Const.LIST_FILE_NAME
    with open(os.path.join(path, filename), 'w') as listFile:
        for k, v in masterList.getItems().items():
            listFile.write(masterList.printItems())

global mlists
mlists = loadMasterList()

mainMenu()