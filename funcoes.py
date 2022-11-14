import sqlite3
from flask import render_template

con = sqlite3.connect("deposito.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS produtos(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Marca TEXT, Volume TEXT, Quantidade INTEGER, Preco REAL)")

res = cur.execute("SELECT name FROM sqlite_master")

def RegistrarProduto():
    # Se o id já estiver cadastrado, não cadastrar
    marca = str(input("Marca: ")).capitalize()
    volume = float(input("Volume: "))
    quantidade = int(input("Quantidade: "))
    precoUnit = float(input("Preço Unitário: "))
    cur.execute("""INSERT INTO produtos (Marca, Volume, Quantidade, Preco) VALUES
            (?,?,?,?)
    """,(marca, volume, quantidade, precoUnit))
    con.commit()

def RegistrarSite(marca, volume, quantidade, preco):
    # Se o id já estiver cadastrado, não cadastrar
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO produtos (Marca, Volume, Quantidade, Preco) VALUES
            (?,?,?,?)
    """,(marca, volume, quantidade, preco))
    con.commit()

def  AtualizarDados(id):
    # quantidade | Apresentada no .frame
    # comprado |  Quantia a ser retirada da variável quantidade
    # quantidade -= comprado
    # idI | id automaticamente capturado na hora da alteração
    
    vari = input('O que você quer mudar? ')
    variavel = input("Digite a mudança: ")
    cur.execute(f"""
    UPDATE produtos
    SET {vari} = ?
    WHERE id = ?
    """,(variavel, id))
    con.commit()

def DeletarProduto(marca):
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    cur.execute("""
    DELETE FROM produtos
    WHERE Marca = ?
    """, (marca,))
    con.commit()

def DeletartProduto(id):
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    cur.execute("""
    DELETE FROM produtos
    WHERE id = ?
    """, (id,))
    con.commit()


def Vendas(id):
    cur.execute("CREATE TABLE IF NOT EXISTS carrinho(id INTEGER NOT NULL PRIMARY KEY, Marca TEXT, Volume TEXT, Quantidade INTEGER, Preco REAL)")
    
    quantidadeAtual = cur.execute("SELECT Quantidade FROM produtos WHERE id = ?",(id,)).fetchone()
    quantidadeRetirar = int(input("Quantidade a retirar: "))
    qtd = (quantidadeAtual[0] - quantidadeRetirar)
    while qtd < 0:
        print(qtd)
        quantidadeRetirar = int(input("Quantidade requisitada maior do que a em estoque: "))
        qtd = (quantidadeAtual[0] - quantidadeRetirar)
        
    if quantidadeRetirar > 0:
        escolhas = cur.execute("SELECT id,Marca,Volume,Quantidade,Preco FROM produtos WHERE id = ?",(id,)).fetchone()
        cur.execute("INSERT OR REPLACE INTO carrinho (id,Marca,Volume,Quantidade,Preco) VALUES (?,?,?,?,?)", (escolhas[0],escolhas[1],escolhas[2],quantidadeRetirar,escolhas[4]))
        con.commit()

def Carrin(marca):
    cur.execute("CREATE TABLE IF NOT EXISTS carrinho(id INTEGER NOT NULL PRIMARY KEY, Marca TEXT, Volume TEXT, Quantidade INTEGER, Preco REAL)")
    
    quantidadeAtual = cur.execute("SELECT Quantidade FROM produtos WHERE id = ?",(id,)).fetchone()
    quantidadeRetirar = int(input("Quantidade a retirar: "))
    qtd = (quantidadeAtual[0] - quantidadeRetirar)
    while qtd < 0:
        print(qtd)
        quantidadeRetirar = int(input("Quantidade requisitada maior do que a em estoque: "))
        qtd = (quantidadeAtual[0] - quantidadeRetirar)
        
    if quantidadeRetirar > 0:
        escolhas = cur.execute("SELECT id,Marca,Volume,Quantidade,Preco FROM produtos WHERE id = ?",(id,)).fetchone()
        cur.execute("INSERT OR REPLACE INTO carrinho (id,Marca,Volume,Quantidade,Preco) VALUES (?,?,?,?,?)", (escolhas[0],escolhas[1],escolhas[2],quantidadeRetirar,escolhas[4]))
        con.commit()
    
def Montante():
    montanteTotal = 0
    montante = cur.execute("SELECT Quantidade,Preco FROM carrinho").fetchall()
    print(montante[0][0])
    for i in range(len(montante)):
        montanteTotal += montante[i][0]*montante[i][1]
    return montanteTotal

def MostrarTabela():
    #print('\nData in produtos table:')
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    data = cur.execute('''SELECT * FROM produtos''').fetchall()
    cur.close()
    return data

def erro(mensagem):
    return render_template("erro.html", mensagem = mensagem)

def ConfirmarCompra():
    qtd = cur.execute("SELECT id,Quantidade FROM carrinho").fetchone()
    allIDS = cur.execute("SELECT id FROM carrinho").fetchall()
    for i in range(len(allIDS)):
        cur.execute("UPDATE produtos SET Quantidade = Quantidade - ? WHERE id = ?",(qtd[1], allIDS[i][0],))
        cur.execute("DELETE FROM carrinho WHERE id = ?", (allIDS[i][0],))
    con.commit()

def Marcas():
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    marcas = cur.execute('''SELECT Marca FROM produtos GROUP BY Marca''').fetchall()
    cur.close()
    return marcas

def id(marca):
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    id = cur.execute('''SELECT id FROM produtos WHERE Marca = ?''', (marca,)).fetchone()
    cur.close()
    return id[0]

def Quantidade(marca):
    con = sqlite3.connect("deposito.db")
    cur = con.cursor()
    quant = cur.execute('''SELECT Quantidade FROM produtos WHERE Marca = ? GROUP BY Quantidade''', (marca,)).fetchall()
    cur.close()
    return quant

DeletartProduto(2)
Marcas()

# Registro de produtos
# Registro de vendas
# Aplicação de desconto personalizado
# Calculadora simples