import DataManager
import Score
import Evaluation

if __name__ == "__main__":


    DataManager.data_setup()
    data = DataManager.data_load()

    func = input("Enter e to evaluate system | Enter q to query")

    if func == "e":
        query_rels = Evaluation.sort_query_rels()
        ndcg = Evaluation.get_system_ndcg(data[0], query_rels)
        print("System NDCG:: " + ndcg)
    elif func == "q":
        user_query = input("Enter Query")
        #Take user query and convert to bow and total length
        top_docs = Score.get_top_docs('''THIS IS WHERE THE CONVERTY QUERY GOES''', data[0])
        #Do something with those documents returned


        




