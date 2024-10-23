import pickle
import pandas as pd
import ast
import re

def data_setup():
    df = pd.read_csv('data/ProjectData.csv', encoding='utf8')
    df.tail(2)
    data = []

    #enum
    TEXT = 0
    BOW = 1
    TAGS = 2
    FOLLOWERS = 3
    FRIENDS = 4
    VERIFICATION = 5
    USERNAME = 6
    DATE = 7

    for i, row in df.iterrows():
        txt = row['text']
        txt = txt.lower()
        txt = txt.replace('\n', ' ')
        txt = re.sub(r'[^a-z0-9\s]', '', txt)
        dict = {}
        for w in txt.split():
            if w in dict:
                dict[w] += 1
            else:
                dict[w] = 1
        try:
            data.append([
                row['text'], 
                dict, 
                safe_literal_eval(row['hashtags']), 
                int(row['user_followers']), 
                int(row['user_friends']), 
                (True if (row['user_verified'] == "True") else False), 
                row['user_name'], 
                row['date']
            ])
        except:
            print("Line",i,"invalid")
    saveFile = open("index", 'wb')
    pickle.dump(data, saveFile)
    saveFile.close
    print("data ready!")

def data_load():
    file = open("index", 'rb')
    dataLoad = pickle.load(file)
    file.close()
    return dataLoad

def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []