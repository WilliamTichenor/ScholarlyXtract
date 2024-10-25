import Score
import ir_datasets
from collections import Counter
from collections import defaultdict
import math



#Converting dataset queries to our generic query object
def convert_query(query): #MAY NEED TO REMOVE PUNCUATION
    words = query[1].lower()
    words = words.split()
    bodylen = len(words)
    term_freq = dict(Counter(words))

    altered_query = {
        "id": query[0],
        "bodybow": term_freq,
        "bodylen": bodylen
    }

    return altered_query


#Need organized way to filter queries, documents, and relevance
def sort_query_rels():
    query_rels = defaultdict(lambda: defaultdict(dict)) #Nested Diconary to store query and associated document relvency values
    dataset = ir_datasets.load("cranfield")
    for qrel in dataset.qrels_iter():
        query_rels[qrel[0]][qrel[1]] = qrel[2]

    return query_rels


#Get ndcg for a single query
def get_ndcg(query, query_rels, docs):
    top_docs = Score.get_top_docs(query,docs)

    ndcg_score = 0

    for i, (doc_id, score) in enumerate(top_docs.items()):
        if doc_id in query_rels[query["id"]]:
            rel = query_rels[query["id"][doc_id]]
            num = pow(2, rel) - 1
            denom = math.log2(1 + i)
            ndcg_score = ndcg_score + (num/denom)
    
    return ndcg_score


#Get average ndcg for all queries in dataset
def get_system_ndcg(docs, query_rels):
    dataset = ir_datasets.load("cranfield")

    total_score = 0
    num_queries = 0


    for q in dataset.queries_iter():
        query = convert_query(q)
        query_ndcg = get_ndcg(query,query_rels, docs)
        total_score = total_score + query_ndcg
        num_queries+=1
    
    system_ndcg = total_score/num_queries

    return system_ndcg

