import sqlite3
from flask import Flask, redirect, render_template, request, session
from teste import verificacao
conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/")
def index():
   
   return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
      name = request.form.get("name")
      senha = request.form.get("senha")
      
      if verificacao(str(name), str(senha)) == True:
         return redirect("/")

   return render_template("login.html")

@app.route("/estoque")
def estoque():
   
   return render_template("estoque.html")

@app.route("/logout")
def logout():
   session["name"] = None
   return redirect("/")



#ativar quando o site for ao Ar
#if __name__ == "__main__":
app.run(debug=True)