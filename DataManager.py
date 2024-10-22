import pickle

# Main method only for testing! this won't exist.
if __name__ == "__main__":
    """
    print("hi!")
    arr = ["asdf", "testing", 5]
    saveFile = open("index", 'ab')
    pickle.dump(arr, saveFile)
    saveFile.close
    """
    saveFile = open("index", 'rb')
    testing = pickle.load(saveFile)
    print(testing)
    print(testing[1])