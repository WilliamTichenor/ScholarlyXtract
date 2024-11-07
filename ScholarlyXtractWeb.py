import DataManager
import Score
import Evaluation
from flask import Flask
from flask import request, render_template, g
from markupsafe import escape



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    g.data = DataManager.data_load()
    ret = ""
    if request.method == 'POST':
        if request.form.get('search') == 'Search':
            ret = "Search: "+request.form.get("query", "")
        elif request.form.get('eval') == 'Test System':
            query_rels = Evaluation.sort_query_rels()
            ndcg = Evaluation.get_system_ndcg(g.data[0],query_rels,g.data)
            #print("System NDCG:: ", ndcg)
            ret = "System Average NDCG: "+str(ndcg)[:5]
        elif request.form.get('setup') == 'Parse Dataset':
            DataManager.data_setup()
            g.data = DataManager.data_load()
            ret = "Dataset updated!"
        else:
            print("Error!")
    elif request.method == 'GET':
        return render_template("indexForm.html")
    
    return render_template("indexForm.html")+ret

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)