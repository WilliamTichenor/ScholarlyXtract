# ScholarlyXtract

## Overview
Our information retreival system performs ranked retreival on a dataset that contains data relating to many scientific papers during the 20th century, including the authors, title, body, bibliography, along with sample queries and their relevance scores.

Our system has 2 functions, evaluation and query. Our system is evaluated on a typical NDCG scale and a rating is displayed when a user requests evaluation. User also has ability to search for documents. The returned documents can be viewed in full by the user once returned.

## Setup & Run

### Setup
Have specific imports need to be able to interact with our data and perform specific functions
The following imports and libaries are found in `requirements.txt`

To install the nessesary libaries `pip install -r requirements.txt`

### Run
- To run `python ScholarlyXtractWeb.py`
- From there will be greeted with simple UI
    - Type into the search bar and click `Search` to query
         - If no documents found system will display `No Results!`
         - If documents are found system will display the documents with the ability to view them in full
    - Click `Test System` to get NDCG score of the system
         - System will display `System Average NDCG: x`
  
