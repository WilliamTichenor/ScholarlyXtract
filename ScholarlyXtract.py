import DataManager
import Score
import Evaluation
import re

if __name__ == "__main__":


    DataManager.data_setup()
    data = DataManager.data_load()

    func = input("Enter e to evaluate system | Enter q to query")

    if func == "e":
        query_rels = Evaluation.sort_query_rels()
        ndcg = Evaluation.get_system_ndcg(data[0],query_rels,data)
        print("System NDCG:: ", ndcg)


    elif func == "q":
        user_query = input("Enter Query")



        




