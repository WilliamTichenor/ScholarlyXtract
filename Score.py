'''
    Document{

	id: 
	Authorbow: BOW 
    titlebow: BOW
	Bodybow: BOW
	Authorlength: int
	Titlelength: int
	Bodylength: int

    }

Query {
	bodybow: BOW
	bodylength: 
}

'''

#Weights
k1 = 1.6 #Typically between 1.2-2

B_body = 0.5
B_title = 0.5
B_author = 0.5

W_body = 0.5
W_title = 0.5
W_author = 0.5


#Doc statistics
doc_freq = {} #List of words and how many documents they appear in
avg_body_len = 0
avg_title_len = 0
avg_author_len = 0

#How many documents we want to return
n = 10


#Gets score for one document based on query
def get_score(query,doc):

	doc_score = 0

	for query_word, query_freq in query["bodybow"]:


		word_score = 0

		body_score = 0
		title_score = 0
		author_score = 0


		#Body
		if query_word in doc["bodybow"]:
			body_num = doc["bodybow"][query_word]
			body_denom = ((1-B_body) + B_body * (doc["bodylength"]/avg_body_len))
			body_score = body_score + (body_num/body_denom)

		#Title
		if query_word in doc["titlebow"]:
			title_num = doc["titlebow"][query_word]
			title_denom = ((1-B_title) + B_title * (doc["titlelength"]/avg_title_len))
			title_score = title_score + (title_num/title_denom)

		#Author
		if query_word in doc["authorbow"]:
			author_num = doc["authorbow"][query_word]
			author_denom = ((1-B_author) + B_author * (doc["authorlength"]/avg_author_len))
			author_score = author_score + (author_num/author_denom)

		word_score = (body_score * B_body) + (title_score * B_title) + (author_score * B_author)

		score = score + ((word_score/(k1+word_score)) * doc_freq[query_word])

	return doc_score


#Gets top n documents based on query
def get_top_docs(query, docs):

	doc_scores = {} #Dictionary that holds doc id with associated score

	for doc in docs:
		doc_score = get_score(query,doc)
		doc_scores[doc["id"]] = doc_score

	sorted_doc_scores = dict(sorted(doc_scores.items(), key=lambda item: item[1], reverse=True))


	return dict(list(sorted_doc_scores.items())[:n]) #Only want list of top n documents

	#return sorted_doc_scores

