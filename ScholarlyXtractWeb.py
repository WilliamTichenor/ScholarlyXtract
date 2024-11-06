import DataManager
import Score
import Evaluation
from flask import Flask
from flask import request, render_template
from markupsafe import escape



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('search') == 'Search':
            print("Search: "+request.form.get("query", ""))
        elif request.form.get('eval') == 'Test System':
            query_rels = Evaluation.sort_query_rels()
            ndcg = Evaluation.get_system_ndcg(data[0],query_rels,data)
            print("System NDCG:: ", ndcg)
        elif request.form.get('setup') == 'Parse Dataset':
            DataManager.data_setup()
            data = DataManager.data_load()
        else:
            print("Error!")
    elif request.method == 'GET':
        return render_template("indexForm.html")
    
    return render_template("indexForm.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    data = DataManager.data_load()