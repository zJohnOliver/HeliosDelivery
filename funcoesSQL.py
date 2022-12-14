import sqlite3

#--------------------------------------------------------BANCO PURO----------------------------------------------------------------------------------#

def RegistrarSite(marca, volume, quantidade, preco):
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO produtos (Marca, Volume, Quantidade, Preco) VALUES
            (?,?,?,?)
    """,(marca.upper(), volume, quantidade, preco))
    con.commit()
    cur.close()
    con.close()
    
def  AtualizarDados(id, marca, volume, quantidade, preco):
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    cur.execute(f"""
    UPDATE produtos
    SET Marca = ?, Volume = ?, Quantidade = ?, Preco = ?
    WHERE id = ?
    """, (marca.upper(), volume, quantidade, preco, id,))
    con.commit()

def DeletarProduto(id, tabela):
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    cur.execute("""
    DELETE FROM '%s'
    WHERE id = ?
    """%tabela,(id,))
    con.commit()
    cur.close()
    con.close()


def MostrarTabela(tabela):
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM '%s' "%tabela).fetchall()
    cur.close()
    con.close()
    return data

def ConversorMes(iddata):
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    anoMes = cur.execute("SELECT Mes FROM vendasmensais WHERE iddata = ?", (iddata))
    index = anoMes[5:7]

    return meses[int(index)-1]

def MostrarLinha(id):
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    linha = cur.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()

    return linha

def DeletarCarrinho():
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    cur.execute("""
    DELETE FROM carrinho
    """)
    con.commit()
    cur.close()
    con.close()

def formatarNum(x):
    str(x)
    y = []

    for i in range(len(x)):
        if x[i] in "0123456789,.":
            y.append(x[i])
    y = ''.join(y)

    y = y.replace(',' , ".")

    ponto = y.count('.')

    y = y.replace('.', '' , (ponto-1))

    try:
        return f"{float(y):.2f}"
    except ValueError as error:
        return 0
    
def formatarVolume(x):
    try:
        if "L" or "ml" in x:
            if "ml" in x:
                x = int(x.replace("ml",''))
            elif "L" in x:
                x = int(x.replace("L",""))*1000
        x = int(x)

        if x >= 1000:
            vol = x/1000
            volR = int(vol)
            if vol == volR:
                return str(f"{vol:.0f}L")
            else:
                vol = str(vol).replace(".",",")
            return vol+"L"
        else:
            return str(x)+"ml"
    except ValueError as error:
        return x
#--------------------------------------------------------ÁREA DE VENDA------------------------------------------------------------------------------#

def Vendas(id, quantidadeRetirar):
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS carrinho(id INTEGER NOT NULL PRIMARY KEY, Marca TEXT, Volume TEXT, Quantidade INTEGER, Preco REAL)")
    quantidadeAtual = cur.execute("SELECT Quantidade FROM produtos WHERE Marca = ?" ,(id, )).fetchone()
    #quantidadeRetirar = int(input("Quantidade a retirar: "))
    qtd = (quantidadeAtual[0] - quantidadeRetirar)
    
    if qtd < 0:
        return
    else:
        if quantidadeRetirar > 0:
            escolhas = cur.execute("SELECT id,Marca,Volume,Quantidade,Preco FROM produtos WHERE Marca = ?",(id, )).fetchone()
            cur.execute("INSERT OR REPLACE INTO carrinho (id,Marca,Volume,Quantidade,Preco) VALUES (?, ?, ?, ?, ?)", (escolhas[0], escolhas[1], escolhas[2], quantidadeRetirar, escolhas[4]))
            con.commit()

def ConfirmarCompra():
    import datetime
    x = datetime.datetime.now() 
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    qtd = cur.execute("SELECT id,Quantidade FROM carrinho").fetchone()
    allIDS = cur.execute("SELECT id FROM carrinho").fetchall()
    for i in range(len(allIDS)):
        cur.execute("UPDATE produtos SET Quantidade = Quantidade - ? WHERE id = ?",(qtd[1], allIDS[i][0], ))
        cur.execute("CREATE TABLE IF NOT EXISTS vendasmensais (iddata TEXT PRIMARY KEY , Mes TEXT NOT NULL, id INTEGER NOT NULL, Marca TEXT, Volume TEXT, Quantidade INTEGER, PrecoUnit REAL, PrecoTotal REAL)")
        vendas = cur.execute("SELECT id,Marca,Volume,Quantidade,Preco FROM carrinho WHERE id = ?", (allIDS[i][0], )).fetchone()

        mes = x.strftime("%m") #<- mês com "0" (01, 02, 03...)

        data = (f"{x.year}-{mes}") #<- Ano e mês

        
        iddata = (f"{x.year}{mes}{vendas[0]}") #<- Criando um id junto com a data para permitir repetições com meses diferentes na mesma tabela 
        precoT = (vendas[3] * vendas[4]) #<- Preço total da compra para o a tabela de registro de vendas

        try:
            cur.execute("INSERT INTO vendasmensais (iddata, Mes, id,Marca,Volume,Quantidade,PrecoUnit,PrecoTotal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (iddata, data, vendas[0], vendas[1], vendas[2], vendas[3], vendas[4], f'{precoT:.2f}'))

        except sqlite3.IntegrityError as error: 
            cur.execute("UPDATE vendasmensais SET Quantidade = Quantidade + ?, PrecoUnit = ?, PrecoTotal = PrecoTotal + ? WHERE iddata = ? ", (vendas[3], vendas[4], f'{precoT:.2f}', iddata))
            
        cur.execute("DELETE FROM carrinho WHERE id = ?", (allIDS[i][0], ))
    con.commit()
    cur.close()
    con.close()

def Montante():
    con = sqlite3.connect("deposit.db")
    cur = con.cursor()
    montanteTotal = 0
    montante = cur.execute("SELECT Quantidade,Preco FROM carrinho").fetchall()
    for i in range(len(montante)):
        montanteTotal += montante[i][0] * montante[i][1]
    cur.close()
    con.close()
    return montanteTotal

def Desconto(valor, tipo, desconto):

    if tipo == 1:
        return valor*(desconto/100)
        
    else:
        return desconto

#--------------------------------------------------------GABRIEL QUE FEZ------------------------------------------------------------------------------#


