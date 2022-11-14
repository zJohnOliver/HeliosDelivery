import sqlite3

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()



def verificacao(email,senha):

    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    verificacao = cursor.execute(f"""
    SELECT email,senha FROM clientes WHERE email = '%s'
    """%email).fetchone()
    
    if verificacao is not None:
        getSenha = verificacao[1]
    else:
        getSenha = None

    if senha == getSenha:
        return True
    else:
        return False

def cadastroPessoa(email,senha):
    cursor.execute(f"""
    INSERT INTO clientes (email, senha)
    VALUES (?, ?)
    """,(email,senha))
    
    conn.commit()

def tabelaCadastro():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE clientes (
            email TEXT NOT NULL PRIMARY KEY,
            senha TEXT NOT NULL
    );
    """)


