import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from funcaopessoas import verificacao
from funcoesSQL import MostrarTabela, DeletarProduto, Marcas, RegistrarSite, Montante, Vendas, MostrarLinha, AtualizarDados
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
   name = request.form.get("name")
   session.clear()

   if request.method == "GET":
      return render_template("login.html")
   else:
      session["name"] = request.form.get("name")
      session["senha"] = request.form.get("senha")
      
      if verificacao(session["name"], session["senha"]):
         return render_template("/index.html", nome = name)
   return render_template("login.html")
      

@app.route("/estoque", methods=["GET", "POST"])
@login_required
def estoque():
   if request.method == "GET":
      db = MostrarTabela("produtos")
      return render_template("estoque.html", db = db)
   else:
      print('hello')
      global XYz
      XYz = request.form.get("quantidade")
      return redirect("addcarrinho", quantidade = XYz)


@app.route("/excluir/<id_produto>", methods=["GET", "POST"])
@login_required
def excluir(id_produto):
   if request.method == "GET":
      DeletarProduto(id_produto)
   #else:
      #marca = request.form.get("marca")
      #DeletarProduto(id_produto)
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
      return redirect("/adicionar")


@app.route("/atualizar/<id_produto>", methods=["GET", "POST"])
@login_required
def atualizar(id_produto):
   if request.method == "GET":
      idproduto = id_produto
      marca = MostrarLinha(id_produto)[1]
      volume = MostrarLinha(id_produto)[2]
      quantidade = MostrarLinha(id_produto)[3]
      preco = MostrarLinha(id_produto)[4]
      return render_template("atualizar.html", marca=marca, preco=preco, volume=volume, quantidade=quantidade, id_produto = idproduto)

   if request.method == "POST":   
      updMarca = request.form.get("Marca")
      updVolume = request.form.get("Volume")
      updQuantidade = request.form.get("Quantidade")
      updPreco = request.form.get("Preco")   
      AtualizarDados(id_produto, updMarca, updVolume, updQuantidade, updPreco)
      return redirect("/estoque")
      


@app.route("/carrinho", methods=["GET", "POST"])
@login_required
def carrinho():
   db = MostrarTabela("carrinho")
   total = Montante()
   return render_template("carrinho.html", db = db, montante=total)

@app.route("/addcarrinho/<id_produto>", methods=["GET", "POST"])
@login_required
def adccarrinho(id_produto):
   if request.method == "GET":
      
      Vendas(id_produto, XYz)
      
   return redirect("/carrinho")

@app.route("/logout")
def logout():
   session["name"] = None
   return redirect("/")


#ativar quando o site for ao Ar
#if __name__ == "__main__":
app.run(debug=True)