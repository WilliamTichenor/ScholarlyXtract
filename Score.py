#Enum
ID = 0
AUTHORBOW = 1
TITLEBOW = 2
BODYBOW = 3
AUTHORLEN = 4
TITLELEN = 5
BODYLEN = 6


#Weights
k1 = 1.6 #Typically between 1.2-2

B_body = 0.1
B_title = 0.4
B_author = 0.5

W_body = 1
W_title = 2
W_author = 5


#How many documents we want to return
n = 1400


#Gets score for one document based on query
def get_score(query, doc, data):
	doc_score = 0
	avg_body_len = data[2][2]
	avg_title_len = data[2][1]
	avg_author_len = data[2][0]
    
	for query_word in query[1]:

		word_score = 0

		body_score = 0
		title_score = 0
		author_score = 0

		#Body
		if query_word in doc[BODYBOW]:
			body_num = doc[BODYBOW][query_word]
			body_denom = ((1-B_body) + B_body * (doc[BODYLEN]/avg_body_len))
			body_score = body_score + (body_num/body_denom)

		#Title
		if query_word in doc[TITLEBOW]:
			title_num = doc[TITLEBOW][query_word]
			title_denom = ((1-B_title) + B_title * (doc[TITLELEN]/avg_title_len))
			title_score = title_score + (title_num/title_denom)

		#Author
		if query_word in doc[AUTHORBOW]:
			author_num = doc[AUTHORBOW][query_word]
			author_denom = ((1-B_author) + B_author * (doc[AUTHORLEN]/avg_author_len))
			author_score = author_score + (author_num/author_denom)

		word_score = (body_score * W_body) + (title_score * W_title) + (author_score * W_author)

		idf = 0
		if(query_word in data[1][2]):
			idf = data[1][2][query_word]


		doc_score = doc_score + ((word_score/(k1+word_score)) * idf) #This could cause problems if word doesnt appear
	return doc_score




def get_top_docs(query, docs, data):
	doc_scores = {}

	for doc in docs:
		doc_score = get_score(query,doc,data)
		doc_scores[int(doc[ID])] = doc_score

	sorted_doc_scores = dict(sorted(doc_scores.items(), key=lambda item: item[1], reverse=True))
	return dict(list(sorted_doc_scores.items())[:n]) #Only want list of top n documents
		
			




