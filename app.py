from flask import Flask, render_template, request, redirect, session
#from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from flask_pymongo import PyMongo   # pip install Flask-PyMongo

app = Flask(__name__)
app.secret_key = 'ELAAROUB DAMOU'

app.config["MONGO_URI"] = "mongodb://localhost:27017/gestion_stock"
mongo = PyMongo(app)

def isEmpty(word):
    if word:
        return False
    return True

def getLastIdProduct():
    products, d = mongo.db.produit.find(), {}
    for p in products:
        pass
    d = p
    return int(d["_id"])
    




@app.route('/', methods = ['GET'] )
def loginGet():    
    return render_template('login.html')

@app.route('/', methods = ['POST'] )
def loginPost():
    login = request.form['login']
    password = request.form['password']
    admin = mongo.db.admin.find_one({"gmail":login, "password": password})

    #login_user(adminEmail)

    if isEmpty(admin): 
        return redirect('/')
    else :
        session["prenom"] = admin["prenom"]
        session["nom"] = admin["nom"]
        return redirect('/ourStock')
 

@app.route('/logout', methods = ['GET'] )
def logout():    
    return render_template('login.html')

@app.route('/ourStock', methods = ['GET'] )
def ourStock():
    produits = mongo.db.produit.find()
    admins = mongo.db.admin.find()
    if "nom" and "prenom" in session:
        nomAdmin = session["nom"] + " " + session["prenom"]
    else:
        nomAdmin = "Admin"
    return render_template('home.html', produits = produits, admins = admins, nomAdmin = nomAdmin)



#add produit----------------------------------------------------
@app.route('/addproduit', methods = ['POST'])
def addproduit():
	if request.method == 'POST':

	    id  = getLastIdProduct() + 1
        categorie = request.form['categorie']
        nomProduit = request.form['nomProduit']
        img = request.form['img']
        Qte = request.form['Qte']
        prix = request.form['prix']
        description = request.form['description']

        mongo.db.produit.insert_one({
            "_id": id,
            "categorie": categorie,
            "nomProduit": nomProduit,
            "img" : img,
            "Qte": Qte,
            "prix": prix,
            "description" : description
        })

    redirect('/ourStock')

if __name__ == "__main__" :
    app.run(debug=True)
