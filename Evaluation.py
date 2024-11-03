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
        if query_rels[qrel[0]][qrel[1]] == -1:
            query_rels[qrel[0]][qrel[1]] = 0

    return query_rels

def prun_top_docs(top_docs, query, query_rels):
    pruned_top_docs = {}
    for doc_id in top_docs:
        if str(doc_id) in query_rels[query[0]]:
            pruned_top_docs[doc_id] = top_docs[doc_id]
    sorted_pruned_scores = dict(sorted(pruned_top_docs.items(), key=lambda item: item[1], reverse=True))
    return sorted_pruned_scores

def get_ideal_top_docs(query, query_rels):
    ideal_top_docs = {}

    for doc_id in query_rels[query[0]]:
        ideal_top_docs[doc_id] = query_rels[query[0]][doc_id]
        if ideal_top_docs[doc_id] == -1:
            ideal_top_docs[doc_id] = 0

    sorted_ideal = dict(sorted(ideal_top_docs.items(), key=lambda item: item[1], reverse=True))

    return sorted_ideal


#Get ndcg for a single query
def get_ndcg(query, query_rels, docs, data):
    top_docs = Score.get_top_docs(query,docs,data)
    pruned_top_docs = prun_top_docs(top_docs,query, query_rels)
    ndcg_score = 0

    #----------------------------------------------

    for i, (doc_id, score) in enumerate(pruned_top_docs.items()):
        if str(doc_id) in query_rels[query[0]]:
            rel = query_rels[query[0]][str(doc_id)]
            num = pow(2, rel) - 1
            denom = math.log2(1 + (i+1))
            ndcg_score = ndcg_score + (num/denom)

    #-----------------------------------------------

    ideal_top_docs = get_ideal_top_docs(query, query_rels)

    #print(ideal_top_docs)

    #print("Ideal entries:: ", len(ideal_top_docs))
    #print("Pruned", len(pruned_top_docs))
    #print("------------------------------------------")


    #-----------------------------------------------
    indcg_score = 0
    for i, (doc_id, score) in enumerate(ideal_top_docs.items()):
        rel = score
        num = pow(2, rel) - 1
        denom = math.log2(1 + (i+1))
        indcg_score = indcg_score + (num/denom)

    #----------------------------------------------

    if ndcg_score > indcg_score:
        print("ndcg is higher than ideal")

    return ndcg_score/indcg_score



#Get average ndcg for all queries in dataset
def get_system_ndcg(docs, query_rels, data):
    dataset = ir_datasets.load("cranfield")

    total_score = 0
    num_queries = 0


    for q in dataset.queries_iter():
        if q[0] not in query_rels:
            continue
        query = convert_query_bow(q[1])
        query[0] = q[0]
        query_ndcg = get_ndcg(query,query_rels,docs,data)
        total_score = total_score + query_ndcg
        num_queries+=1
    
    
    system_ndcg = total_score/num_queries

    return system_ndcg



