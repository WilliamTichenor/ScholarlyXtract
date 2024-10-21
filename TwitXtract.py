import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

#To run: `python TwitXtract.py`

def make_plots(df):
    #User verification plot
    plt.figure(figsize=(6, 6))
    df['user_verified'].value_counts().plot.pie(autopct='%1.1f%%', colors=['skyblue', 'lightgreen'])
    plt.title('Verified vs Unverified Users')
    plt.savefig('figures/verified_users_pie.png')
    plt.show()

    #Most popular hashtags excluding ChatGPT (ie the one required to be in the data set)
    df['hashtags'] = df['hashtags'].fillna('[]').apply(lambda x: safe_literal_eval(x) if isinstance(x, str) else [])
    all_hashtags = df['hashtags'].explode()
    top_hashtag = all_hashtags.value_counts().idxmax()
    filtered_hashtags = all_hashtags[all_hashtags != top_hashtag]
    plt.figure(figsize=(12, 6))
    filtered_hashtags.value_counts().nlargest(10).plot(kind='bar', color='orange')
    plt.title(f'Top 10 Hashtags Used (Excluding #{top_hashtag})')
    plt.xlabel('Hashtags')
    plt.ylabel('Count')
    plt.savefig('figures/filtered_hashtag_distribution.png')
    plt.show()


def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []

if __name__ == "__main__":
    # Example usage
    df = pd.read_csv('data/ProjectData.csv', encoding='utf8')
    df.tail(2)

    query = input("Enter query:: ")
    print("User Query:: " + query)

    print(len(df[df['user_followers'] < 1000]), 'users with less than 1000 followers')
    print(len(df[df['user_followers'] > 1000]), 'userss with more than 1000 followers')

    make_plots(df)



