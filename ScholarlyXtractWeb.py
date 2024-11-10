import DataManager
import Score
import Evaluation
import ir_datasets
from flask import Flask
from flask import request, render_template, g, url_for
from markupsafe import escape



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    g.data = DataManager.data_load()
    ret = ""
    if request.method == 'POST':
        if request.form.get('search') == 'Search':
            ret = "<h2>Search: "+request.form.get("query", "")+"</h2>"
            qBOW = Evaluation.convert_query_bow(request.form.get("query", ""))
            results = Score.get_top_docs(qBOW, g.data[0], g.data, 10)
            dataset = ir_datasets.load("cranfield")
            docstore = dataset.docs_store()
            first_key = next(iter(results))  # Get the first key
            first_value = results[first_key]
            if first_value <= 0:
                ret += "<h3>No Results!</h3>"
            else:
                ret+="<ol>"
                for id in results.keys():
                    #print(results[id])
                    if results[id] <= 0:
                        continue
                    doc = docstore.get(str(id))
                    ret+="<li><a href="+url_for("show_doc", doc_id=id)+">"+str(doc.title)+"</a></li>"
                ret+="</ol>"
        elif request.form.get('eval') == 'Test System':
            query_rels = Evaluation.sort_query_rels()
            ndcg = Evaluation.get_system_ndcg(g.data[0],query_rels,g.data)
            #print("System NDCG:: ", ndcg)
            ret = "System Average NDCG: "+str(ndcg)[:5]
        else:
            print("Error!")
    elif request.method == 'GET':
        return render_template("indexForm.html")
    
    return render_template("indexForm.html")+ret

@app.route('/docs/<int:doc_id>')
def show_doc(doc_id):
    dataset = ir_datasets.load("cranfield")
    docstore = dataset.docs_store()
    doc = docstore.get(str(doc_id))
    #return "This is document "+str(doc_id)
    return "<h1>"+doc.title+"</h1>" + "<h2>"+doc.author+"</h2>" + "<p>"+doc.text+"</p>" + "<p>"+doc.bib+"</p>"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)