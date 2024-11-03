import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import DataManager

#To run: `python TwitXtract.py`

def make_plots(a):
    #enum
    ID = 0
    AUTHORBOW = 1
    TITLEBOW = 2
    BODYBOW = 3
    AUTHORLEN = 4
    TITLELEN = 5
    BODYLEN = 6

    bodylens = list(map(lambda x: x[6], a[0]))
    plt.hist(bodylens, bins=30, edgecolor='black')
    plt.title("Histogram of Body Lengths")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig('figures/bodylen_distribution.png')
    plt.show()

    sorted_data = dict(sorted(a[1][0].items(), key=lambda item: item[1], reverse=True))
    sorted_data = {k: v for k, v in sorted_data.items() if len(k)>1}
    sorted_data = {x: sorted_data[x] for x in list(sorted_data)[:15]}
    keys = list(sorted_data.keys())
    values = list(sorted_data.values())
    plt.figure(figsize=(8, 6))
    plt.bar(keys, values, color='skyblue', edgecolor='black')
    plt.title("Top 15 Authors by References")
    plt.xlabel("Authors")
    plt.ylabel("References")
    plt.xticks(rotation=45)
    plt.savefig('figures/authorscores.png')
    plt.show()

if __name__ == "__main__":
    DataManager.data_setup()
    a = DataManager.data_load()

    make_plots(a)



