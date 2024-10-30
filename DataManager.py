import pickle
import pandas as pd
import ast
import re
import ir_datasets

def data_setup():
    dataset = ir_datasets.load("cranfield")
    data = []

    #enum
    ID = 0
    AUTHORBOW = 1
    TITLEBOW = 2
    BODYBOW = 3
    AUTHORLEN = 4
    TITLELEN = 5
    BODYLEN = 6

    for row in dataset.docs_iter():
        txt = row.title
        txt = txt.lower()
        txt = txt.replace('\n', ' ')
        txt = re.sub(r'[^a-z0-9\s]', '', txt)
        dictTitle = {}
        for w in txt.split():
            if w in dictTitle:
                dictTitle[w] += 1
            else:
                dictTitle[w] = 1
        txt = row.author
        txt = txt.lower()
        txt = txt.replace('\n', ' ')
        txt = re.sub(r'[^a-z0-9\s]', '', txt)
        dictAuthor = {}
        for w in txt.split():
            if w in dictAuthor:
                dictAuthor[w] += 1
            else:
                dictAuthor[w] = 1
        txt = row.text
        txt = txt.lower()
        txt = txt.replace('\n', ' ')
        txt = re.sub(r'[^a-z0-9\s]', '', txt)
        dictBody = {}
        for w in txt.split():
            if w in dictBody:
                dictBody[w] += 1
            else:
                dictBody[w] = 1
        data.append([
                row.doc_id, 
                dictAuthor,
                dictTitle,
                dictBody, 
                sum(dictAuthor.values()),
                sum(dictTitle.values()),
                sum(dictBody.values()),
            ])
    saveFile = open("index", 'wb')
    pickle.dump(data, saveFile)
    saveFile.close
    print("data ready!")

def data_load():
    file = open("index", 'rb')
    dataLoad = pickle.load(file)
    file.close()
    return dataLoad

if __name__ == "__main__":
    a = data_load()
    print(a[0])