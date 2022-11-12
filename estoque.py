from funçoesImplementar import MostrarTabela

db = MostrarTabela()
for row in db:
    print(row["Marca"])
    print(row["Volume"])
    print(row["Quantidade"])
    print(row["Preco"])