import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from funcaopessoas import verificacao
from funcoesSQL import MostrarTabela, DeletarProduto, Marcas, RegistrarSite, Montante
from auxiliares import login_required
#conn = sqlite3.connect('produtos.db')
#cursor = conn.cursor()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
   if not session.get("name"):
      return redirect("/login")
   return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
   session.clear()

   if request.method == "GET":
      return render_template("login.html")
   else:
      session["name"] = request.form.get("name")
      session["senha"] = request.form.get("senha")
      if verificacao(session["name"], session["senha"]):
         return redirect("/")
   return render_template("login.html")
      

@app.route("/estoque")
@login_required
def estoque():
   db = MostrarTabela("produtos")
   return render_template("estoque.html", db = db)

@app.route("/excluir", methods=["GET", "POST"])
@login_required
def excluir():
   if request.method == "GET":
      marcas = Marcas()
      return render_template("excluir.html", marcas = [row[0] for row in marcas])
   else:
      marca = request.form.get("marca")
      DeletarProduto(marca)
      #vol = request.form.get("marca")
      #quantidade = request.form.get("marca")
      #preco = request.form.get("marca")
   return redirect("/estoque")

@app.route("/adicionar", methods=["GET", "POST"])
@login_required
def adicionar():
   if request.method == "GET":
      return render_template("adicionar.html")
   else:
      marca = request.form.get("marca")
      vol = request.form.get("volume")
      quantidade = request.form.get("quantidade")
      preco = request.form.get("preco")
      RegistrarSite(marca, vol, quantidade, preco)
      return redirect("/estoque")


@app.route("/atualizar")
@login_required
def atualizar():
   return render_template("atualizar.html")


@app.route("/carrinho")
@login_required
def carrinho():
   db = MostrarTabela("carrinho")
   total = Montante()
   return render_template("carrinho.html", db = db, montante=total)

@app.route("/logout")
def logout():
   session["name"] = None
   return redirect("/")


#ativar quando o site for ao Ar
#if __name__ == "__main__":
app.run(debug=True)