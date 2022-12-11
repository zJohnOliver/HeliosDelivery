import sqlite3
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from funcaopessoas import verificacao
from funcoesSQL import MostrarTabela, DeletarProduto, formatarVolume, RegistrarSite, Montante, Vendas, MostrarLinha, AtualizarDados, ConfirmarCompra, DeletarCarrinho, Desconto, formatarNum
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


@app.route("/excluir/<id_produto>", methods=["GET", "POST"])
@login_required
def excluir(id_produto):
   if request.method == "GET":
      DeletarProduto(id_produto, "produtos")
      flash("Produto excluído!")
   return redirect("/estoque")

@app.route("/excluirC/<id_produto>", methods=["GET", "POST"])
@login_required
def excluirC(id_produto):
   if request.method == "GET":
      DeletarProduto(id_produto, "carrinho")
   return redirect("/carrinho")

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
      vol = formatarVolume(vol)
      preco = formatarNum(preco)
      RegistrarSite(marca, vol, quantidade, preco)
      flash("Adicionado!")   
      return redirect("/adicionar")


@app.route("/atualizar/<id_produto>", methods=["GET", "POST"])
@login_required
def atualizar(id_produto):
   if request.method == "GET":
      idproduto = id_produto
      x = MostrarLinha(id_produto)
      marca = x[1]
      volume = x[2]
      quantidade = x[3]
      preco = x[4]
      return render_template("atualizar.html", marca=marca, preco=preco, volume=volume, quantidade=quantidade, id_produto = idproduto)

   if request.method == "POST":   
      updMarca = request.form.get("Marca")
      updVolume = request.form.get("Volume")
      updQuantidade = request.form.get("Quantidade")
      updPreco = request.form.get("Preco")
      updPreco = formatarNum(updPreco)
      updVolume = formatarVolume(updVolume)   
      AtualizarDados(id_produto, updMarca, updVolume, updQuantidade, updPreco)
      flash("Atualizado!")
      return redirect("/estoque")
      
@app.route("/carrinho", methods=["GET", "POST"])
@login_required
def carrinho():
   db = MostrarTabela("carrinho")
   dbP = MostrarTabela("produtos")
   global totalC 
   totalC = Montante()

   if request.method == "POST":
      desconto = request.form.get("desconto")
      tipo = request.form.get("tipo")
      str(tipo)
      if tipo == "on":
         tipo = 1

      if desconto == '':
         print(totalC)
         return render_template("carrinho.html", db = db, montante=totalC, dbP = dbP)

      else:
         x = totalC - Desconto(totalC,tipo,int(desconto))

         return render_template("carrinho.html", db = db, montante=x, dbP = dbP)
   else:
      return render_template("carrinho.html", db = db, montante=totalC, dbP = dbP)

@app.route("/addcarrinho", methods=["GET", "POST"])
@login_required
def adccarrinho():
   if request.method == "POST":
      qtd = request.form.get("Quantidade")
      marca = request.form.get("marca")
      Vendas(marca, int(qtd))
      
   return redirect("/carrinho")

@app.route("/logout")
def logout():
   session["name"] = None
   return redirect("/")

@app.route("/confirma", methods=["GET", "POST"])
def confirma():
   ConfirmarCompra()

   return redirect("/estoque")

@app.route("/cancelarCompra", methods=["GET", "POST"])
def cancelarCompra():
   DeletarCarrinho()
   return redirect("/carrinho")

@app.route("/vendas", methods=["GET", "POST"])
def vendas():
   if request.method == "GET":
      db = MostrarTabela("vendasmensais")
      return render_template("vendas.html", db = db)


#ativar quando o site for ao Ar
#if __name__ == "__main__":
app.run(debug=True)