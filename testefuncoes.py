from funcoesSQL import MostrarTabela, Marcas, RegistrarProduto
import sqlite3

conn = sqlite3.connect('deposit.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM vendasmensais")
conn.commit()
