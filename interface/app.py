import pandas as pd
from flask import Flask, make_response, render_template, request
from pymongo import MongoClient

client = MongoClient(host="db", port=27017)
db = client['db']
col_id = db['id']
col_com = db['commentaire']
col_meta = db["meta"]
col_analyse = db["analyse"]
col_link = db["link"]

#### from flask import Flask, request, render_template

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
    liste1 =['id','thumbnail','title','channel',"categories", "date","description","duration","like_count","view_count", "upload_date" ]
    n1 = len(liste1)
    return render_template('meta.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur, liste1 = liste1,n1 = n1 , data= df )

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

@app.route('/analyse', methods=['GET','POST'])
def analyse():
    nombre_ligne = len(list(col_analyse.find({})))
    cur = col_analyse.find({})
    cur = list(cur)
    valeur=[]
    for dic in cur:
        m = []
        element = []
        for cle,val in dic.items():
            m.append(cle)
            if cle=="links" and val==None:
                val = "pas de lien"
            element.append(val)
        if m.count("links") == 0:
            m.insert(len(m)-1,"links")
            element.insert(len(element)-1,"pas de lien")
    
        valeur.append(element)
        nbr_cle = len(m)
    return render_template('analyse.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur)

@app.route('/link', methods=['GET','POST'])
def link():
    nombre_ligne = len(list(col_link.find({})))
    cur = col_link.find({})
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
    return render_template('link.html', n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur)


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

@app.route('/req/<vari>')
def page_detail(vari):
    
    a = 'https://www.youtube.com/embed/'
    a+=vari
    
    nombre_ligne = len(list(col_meta.find({'id':vari})))
    cur = col_meta.find({'id':vari})
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
    liste1 =['title','channel',"categories","description","duration","like_count","view_count", "upload_date","age_limit","tags" ]
    n1 = len(liste1)
    
    
    nombre_ligne2 = len(list(col_com.find({'video_id':vari})))
    cur = col_com.find({'video_id':vari})
    cur = list(cur)
    valeur2=[]
    for dic in cur:
        m2 = []
        element2 = []
        for cle,val in dic.items():
            m2.append(cle)
            element2.append(val)
        valeur2.append(element2)
        nbr_cle2 = len(m2)
        
    return render_template('page.html',a = a, n = nombre_ligne, cle = m, nbr_col = nbr_cle, liste = valeur, liste1 = liste1,n1 = n1 , data= df,n2 = nombre_ligne2, cle2 = m2, nbr_col2 = nbr_cle2, liste2 = valeur2 )

@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

if __name__ == '__main__':
    app.run(debug=True)