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
            if w == "and": continue
            if w == "et": continue
            if w == "al": continue
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
    
    totalBOW = [{}, {}, {}]
    for row in data:
        for key in row[AUTHORBOW]:
            if key in totalBOW[0]:
                totalBOW[0][key] += 1
            else: totalBOW[0][key] = 1
        for key in row[TITLEBOW]:
            if key in totalBOW[1]:
                totalBOW[1][key] += 1
            else: totalBOW[1][key] = 1
        for key in row[BODYBOW]:
            if key in totalBOW[2]:
                totalBOW[2][key] += 1
            else: totalBOW[2][key] = 1
    
    authoravg = sum(doc[AUTHORLEN] for doc in data) / len(data)
    titleavg = sum(doc[TITLELEN] for doc in data) / len(data)
    bodyavg = sum(doc[BODYLEN] for doc in data) / len(data)


    saveFile = open("index", 'wb')
    pickle.dump((data, totalBOW, [authoravg, titleavg, bodyavg]), saveFile)
    saveFile.close
    print("data ready!")

def data_load():
    file = open("index", 'rb')
    dataLoad = pickle.load(file)
    file.close()
    return dataLoad