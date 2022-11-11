from random import randint, random
import sqlite3

con = sqlite3.connect("deposito.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS produtos(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Marca TEXT, Volume TEXT, Quantidade INTEGER, Preco REAL)")

res = cur.execute("SELECT name FROM sqlite_master")

def RegistrarProduto():
    # Se o id já estiver cadastrado, não cadastrar
    marca = str(input("Marca: ")).capitalize()
    volume = float(input("Volume: "))
    precoUnit = float(input("Preço Unitário: "))
    quantidade = int(input("Quantidade: "))
    cur.execute("""INSERT INTO produtos (Marca, Volume, Quantidade, Preco) VALUES
            (?,?,?,?)
    """,(marca, volume, precoUnit, quantidade))
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

def DeletarProduto(id):
    cur.execute("""
    DELETE FROM produtos
    WHERE id = ?
    """, (id,))
    con.commit()

def vendas(id):
    cur.execute("CREATE TABLE IF NOT EXISTS carrinho(id INTEGER NOT NULL PRIMARY KEY, Marca TEXT, Volume TEXT, Quantidade INTEGER, Preco REAL)")
    x = 1
    while x != 0:
        cur.execute("SELECT Quantidade,Preco FROM produtos WHERE id = ?")
        cur.execute("UPDATE FROM ")
        
        #escolhas = cur.execute("SELECT id,Marca,Volume,Quantidade,Preco FROM produtos WHERE id = ?",(id,)).fetchone()
        #print(escolhas)

        #cur.execute("INSERT INTO carrinho (id,Marca,Volume,Quantidade,Preco) VALUES (?,?,?,?,?)", (escolhas[0],escolhas[1],escolhas[2],quantidade,escolhas[4]))
        #con.commit()
        #x = 0







# Registro de produtos
# Registro de vendas
# Aplicação de desconto personalizado
# Calculadora simples