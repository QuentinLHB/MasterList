# cartouche

from Model.MasterList import MasterList

from Model import Const
from Serialization.Serialize import *
import os.path


def setExportFilePath():
    pathName = ""
    if os.path.isfile(Const.PARAMETERS_FILE):
        pathName = load(Const.PARAMETERS_FILE)
    else:
        save(Const.PARAMETERS_FILE, pathName)  # Creates an empty file

    if pathName == "":
        pathName = input("Collez le chemin du dossier dans lequel sera créé le fichier d'exportation \n"
                         "ex: C:/Users/Quentin/Desktop\nRetour: 0 ou Entrée\n")
        if pathName != ("" and "0"):
            save(Const.PARAMETERS_FILE, pathName)
            print("Le nouveau chemin a bien été enregistré.")


def menu_main():
    """
    Prints main menu and routes to functionalities
    """
    initData()
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
            menu_consultMasterLists()
        elif choice == 2:
            newList = createListBasedOnMasterList()
        elif choice == 3:
            setExportFilePath()


def initData():
    """
    Retrieves the data from the data files.
    If the file is none existent, creates it.
    """
    global mlists
    mlists = load(Const.DATA_FILE)
    if mlists == None:
        mlists = []
        save(Const.DATA_FILE, mlists)


def menu_consultMasterLists():
    """
    Displays all the created Master Lists and routes to submenus.
    """
    while True:
        lengthList = len(mlists)
        print("Gérer les Master Listes :")
        printMasterLists()
        print(f"{lengthList + 1}: Créer une nouvelle liste")
        print("0: Retour au menu précédent")
        choice = getIntInputFromUser(0, lengthList + 1)
        if choice == 0:
            return
        if choice == lengthList + 1:
            createNewMasterList()
        elif 1 <= choice <= lengthList:
            menu_manageMasterList(mlists[choice - 1])


def printMasterLists():
    """
    Prints every Master List.
    Format : "1: List Name"
    """
    for k in range(1, len(mlists) + 1):
        print(f"{k}: {mlists[k - 1].getName()}")


def createNewMasterList():
    """
    Creates a Master List based on the user's inputs.
    Saves it into the data file.
    """
    name = input("Nom de la Master List: ")
    masterList = MasterList(name)
    mlists.append(masterList)
    addNewItems(masterList.getItems())
    save(Const.DATA_FILE, mlists)


def menu_manageMasterList(masterList: MasterList):
    """
    Master List management menu. Displays submenus and routes to them.
    :param masterList: Master List selected.
    :return:
    """
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


def getIntInputFromUser(minInput: int, maxInput: int):
    """
    Loops until the user inputs a correct integer between the two bounds.
    :param minInput: Minimum bound (included)
    :param maxInput: Maximum bound (included)
    :return: User's integer input.
    """
    while True:
        choice = input()
        try:
            choice = int(choice)
            if minInput <= choice <= maxInput:
                return choice
        except:
            print("Saisie incorrecte, merci de saisir une valeur valide.")


def addItemsToMasterList(masterList: MasterList):
    """
    Asks user for new items to add.
    Saves them in the data file.
    :param masterList: Master List in which to store the new items.
    """
    itemList = dict()
    itemList, change = addNewItems(itemList)
    for item, amount in itemList.items():
        masterList.addItem(item, amount)
    save(Const.DATA_FILE, mlists)


def editQuantities(masterList: MasterList):
    """
    Asks user for items to edit, and saves the new quantity.
    :param masterList: Master in which to save the new quantity.
    """
    print(masterList.printItems())
    while True:
        item = input("Saisir le nom exact de l'élément à modifier (menu précédent : 0) : ")
        if item.lower() == ("0" or "q" or "quitter"):
            return
        print("Saisir la nouvelle quantité : ")
        amount = getIntInputFromUser(1, 100)
        masterList.editItem(item, amount)
        save(Const.DATA_FILE, mlists)


def removeItems(masterList: MasterList):
    """
    Asks user which items to remove from the Master List and saves the updated list.
    :param masterList: Master List to update.
    :return:
    """
    print(masterList.printItems())
    while True:
        item = input("Saisir le nom exact de l'élément à supprimer (menu précédent : 0) : ")
        if item.lower() != ("0" and "q" and "quitter"):
            return
        masterList.removeItem(item)
        save(Const.DATA_FILE, mlists)


def clearList(masterList: MasterList):
    """
    Deletes every item from the Master List, without deleting the list itself.
    Saves the empty list.
    :param masterList: Master List to clear.
    """
    masterList.clear()
    save(Const.DATA_FILE, mlists)


def deleteList(masterList):
    """
    Deletes the entire list.
    :param masterList: Master List to delete.
    :return:
    """
    mlists.remove(masterList)
    save(Const.DATA_FILE, mlists)


def askUserForExport(list):
    """
    Asks the user if they want to export list.
    If they do, tries to export it in the saved path.
    :param list: List to export.
    :return:
    """
    choice = input("Exporter la liste au format .txt ? (o/n)\n")
    if choice.lower() != ("n" and "q" and "0"):
        pathName = load(Const.PARAMETERS_FILE)
        if pathName != "":
            try:
                exportList(list, pathName)
                print("Liste exportée au chemin " + pathName)
            except:
                print("Echec de l'export. Merci de vérifier le chemin dans la rubrique 'Paramètres'.")
        else:
            print("Aucun chemin enregistré.")


def createListBasedOnMasterList():
    """
    The users chooses a master list and does the inventory of its stock.
    A grocery list is generated based on the difference between the stock and the master list.
    The list can then be exported.
    """
    print("Choisissez la Master List de référence :")
    printMasterLists()
    masterList = mlists[getIntInputFromUser(1, len(mlists)) - 1]
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
    item = input("Ajouter des éléments à la liste de course ? (o/n)\n")
    if item.lower() != ("n" and "non" and "no" and "0"):
        newList, change = addNewItems(newList)
        if change:
            printList(newList)

    if os.path.isfile(Const.PARAMETERS_FILE):
        askUserForExport(newList)
    else:
        print("Pensez à paramétrer l'export de liste dans la rubrique 'Paramètres'. :)")
    return newList


def addNewItems(list):
    """
    Adds items to a list, independently from the master list.
    :param list: List in which the user adds new items.
    :return: Two values :
        Updated List.
        Boolean value: True if the list has changed, false otherwise.
    """
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
    """
    Prints a list.
    :param list: List to print.
    """
    print("Liste de courses :")
    if len(list.items()) > 0:
        for item, amountToBuy in list.items():
            print(f"{item} : {amountToBuy}")
    else:
        print("(liste vide)")


def exportList(groceryList, path: str):
    """
    Export a grocery list in a .txt file.
    :param groceryList: Dictionary (Item Name:str ; Amount:int)
    :param path: Path used to export the list.
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)

    filename = Const.EXPORTED_LIST_FILENAME
    with open(os.path.join(path, filename), 'w') as listFile:
        for k, v in groceryList.items():
            listFile.write(f"{k}: {v}\n")


menu_main()