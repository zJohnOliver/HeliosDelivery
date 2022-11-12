import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from teste import verificacao
from funçoesImplementar import MostrarTabela
conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
   if not session.get("name"):
      return redirect("/login")
   return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "GET":
      return render_template("login.html")
   else:
      session["name"] = request.form.get("name")
      session["senha"] = request.form.get("senha")
      if verificacao(session["name"], session["senha"]):
         return redirect("/")
   return render_template("login.html")
      

@app.route("/estoque")
def estoque():
   db = MostrarTabela()
   return render_template("estoque.html", db = db)



@app.route("/logout")
def logout():
   session["name"] = None
   return redirect("/")



#ativar quando o site for ao Ar
#if __name__ == "__main__":
app.run(debug=True)