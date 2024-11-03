import Score
import ir_datasets
from collections import Counter
from collections import defaultdict
import math
import string
import re

#Enum
ID = 0
AUTHORBOW = 1
TITLEBOW = 2
BODYBOW = 3
AUTHORLEN = 4
TITLELEN = 5
BODYLEN = 6


def convert_query_bow(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    query_split = s.split()
    bow = {}
    for w in query_split:
        if w in bow:
            bow[w] += 1
        else:
            bow[w] = 1
    return [-1, bow, len(query_split)]


#Need organized way to filter queries, documents, and relevance
def sort_query_rels():
    query_rels = defaultdict(lambda: defaultdict(dict)) #Nested Diconary to store query and associated document relvency values
    dataset = ir_datasets.load("cranfield")
    for qrel in dataset.qrels_iter():
        query_rels[qrel[0]][qrel[1]] = qrel[2]

    return query_rels


#Get ndcg for a single query
def get_ndcg(query, query_rels, docs, data):
    top_docs = Score.get_top_docs(query,docs,data)

    ndcg_score = 0

    for i, (doc_id, score) in enumerate(top_docs.items()):
        if doc_id in query_rels[query[0]]:
            rel = query_rels[query[0][doc_id]]
            num = pow(2, rel) - 1
            denom = math.log2(1 + i)
            ndcg_score = ndcg_score + (num/denom)
    
    return ndcg_score


#Get average ndcg for all queries in dataset
def get_system_ndcg(docs, query_rels, data):
    dataset = ir_datasets.load("cranfield")

    total_score = 0
    num_queries = 0


    for q in dataset.queries_iter():
        query = convert_query_bow(q[1])
        query[0] = q[0]
        query_ndcg = get_ndcg(query,query_rels,docs, data)
        total_score = total_score + query_ndcg
        num_queries+=1
    
    system_ndcg = total_score/num_queries

    return system_ndcg



