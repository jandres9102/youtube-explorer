import pandas as pd
from flask import Flask, make_response, render_template, request
from pymongo import MongoClient

client = MongoClient(host="db", port=27017)
db = client['db']
col_id = db['id']
col_com = db['commentaire']
col_meta = db["meta"]

#### from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/choix', methods=['GET','POST'])
def choix():
    return render_template('choix.html')

@app.route('/id', methods=['GET','POST'])
def id():
    
    nombre_ligne = len(list(col_id.find({})))
    cur = col_id.find({})
    cur = list(cur)
    valeur=[]
    for dic in cur:
        m = []
        element = []
        for cle,val in dic.items():
            m.append(cle)
            element.append(val)
        valeur.append(element)
        nbr_cle = len(m)
    return render_template('id.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur)

@app.route('/meta', methods=['GET','POST'])
def meta():
    
    nombre_ligne = len(list(col_meta.find({})))
    cur = col_meta.find({})
    cur = list(cur)
    valeur=[]
    for dic in cur:
        m = []
        element = []
        for cle,val in dic.items():
            m.append(cle)
            element.append(val)
        valeur.append(element)
        nbr_cle = len(m)
    df = pd.DataFrame (valeur, columns = m)
    liste1 =['id','thumbnail','title','channel',"categories", "date","description" ]
    n1 = len(liste1)
    liste2=[]
    for k in m:
        if k in liste1:
            next
        else:
            liste2.append(k)
    n2 = len(liste2)
    return render_template('meta.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur, liste1 = liste1, liste2 = liste2,n1 = n1 , n2=n2, data= df )

@app.route('/com', methods=['GET','POST'])
def com():
    
    nombre_ligne = len(list(col_com.find({})))
    cur = col_com.find({})
    cur = list(cur)
    valeur=[]
    for dic in cur:
        m = []
        element = []
        for cle,val in dic.items():
            m.append(cle)
            element.append(val)
        valeur.append(element)
        nbr_cle = len(m)
    return render_template('com.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur)

@app.route('/requete/<valider>')
def requete(valider):
    try :
        nombre_ligne = len(list(eval(valider)))
        cur = eval(valider)
        cur = list(cur)
        valeur=[]
        for dic in cur:
            m = []
            element = []
            for cle,val in dic.items():
                m.append(cle)
                element.append(val)
            valeur.append(element)
            nbr_cle = len(m)
        return render_template('com.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur)
    except:
        next


@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

if __name__ == '__main__':
    app.run()