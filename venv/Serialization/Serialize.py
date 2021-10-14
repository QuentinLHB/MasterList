import pickle
import os.path

def save(fileName:str, obj:object):
    with open(fileName, "wb") as file:
        pickle.dump(obj, file)

def load(fileName:str):
    if os.path.isfile(fileName):
        with open(fileName, "rb") as file:
            obj = pickle.load(file)
            return obj
    return None