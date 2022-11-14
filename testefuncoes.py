from funcoes import MostrarTabela, Marcas, DeletartProduto, RegistrarProduto

print(Marcas())
marca = input("Marca: ")
DeletartProduto(id(marca))
print(Marcas())