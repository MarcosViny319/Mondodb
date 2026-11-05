from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://Marcos:senha@cluster0.ksslytw.mongodb.net/"

cliente = MongoClient(
    uri,
    serverSelectionTimeoutMS=5000
)

banco = cliente["loja_db"]
produtos = banco["produtos"]

try:
    cliente.admin.command("ping")
    print("Conexao realizada com sucesso!")
    print("\n--- CADASTRAR PRODUTO ---")

    nome = input("Nome do produto: ")
    categoria = input("Categoria: ")
    preco = float(input("Preco: "))
    quantidade = int(input("Quantidade: "))

    produto = {
        "nome": nome,
        "categoria": categoria,
        "preco": preco,
        "quantidade": quantidade
    }

    resultado = produtos.insert_one(produto)

    print("Produto cadastrado com sucesso!")
    print("ID:", resultado.inserted_id)
    print("\n--- PRODUTOS CADASTRADOS ---")

    registros = produtos.find()

    for produto in registros:
        print("-------------------------")
        print("ID:", produto["_id"])
        print("Nome:", produto["nome"])
        print("Categoria:", produto["categoria"])
        print("Preco:", produto["preco"])
        print("Quantidade:", produto["quantidade"])

    print("\n--- FILTRAR POR CATEGORIA ---")

    categoria_busca = input("Digite a categoria: ")

    registros = produtos.find({
        "categoria": categoria_busca
    })

    encontrou = False

    for produto in registros:
        encontrou = True
        print("-------------------------")
        print("Nome:", produto["nome"])
        print("Categoria:", produto["categoria"])
        print("Preco:", produto["preco"])
        print("Quantidade:", produto["quantidade"])

    if not encontrou:
        print("Nenhum produto encontrado nessa categoria.")

    print("\n--- FILTRAR POR NOME ---")

    nome_busca = input("Digite o nome do produto: ")

    registros = produtos.find({
        "nome": {
            "$regex": nome_busca,
            "$options": "i"
        }
    })

    encontrou = False

    for produto in registros:
        encontrou = True
        print("-------------------------")
        print("Nome:", produto["nome"])
        print("Categoria:", produto["categoria"])
        print("Preco:", produto["preco"])
        print("Quantidade:", produto["quantidade"])

    if not encontrou:
        print("Nenhum produto encontrado pelo nome.")
    
    
    # FILTRAR - Por faixa de preco
    print("\n--- FILTRAR POR PRECO ---")

    preco_minimo = float(input("Digite o preco minimo: "))
    preco_maximo = float(input("Digite o preco maximo: "))

    registros = produtos.find({
        "preco": {
            "$gte": preco_minimo,
            "$lte": preco_maximo
        }
    })

    encontrou = False

    for produto in registros:
        encontrou = True
        print("-------------------------")
        print("Nome:", produto["nome"])
        print("Categoria:", produto["categoria"])
        print("Preco:", produto["preco"])
        print("Quantidade:", produto["quantidade"])

    if not encontrou:
        print("Nenhum produto encontrado nessa faixa de preco.")


    print("\n--- ATUALIZAR PRODUTO ---")

    identificador = input("Digite o ID do produto: ")
    novo_preco = float(input("Digite o novo preco: "))

    resultado = produtos.update_one(
        {"_id": ObjectId(identificador)},
        {"$set": {"preco": novo_preco}}
    )

    if resultado.modified_count > 0:
        print("Produto atualizado com sucesso!")
    else:
        print("Produto nao encontrado ou preco sem alteracao.")

    print("\n--- EXCLUIR PRODUTO ---")

    identificador = input(
        "Digite o ID do produto que deseja excluir: "
    )

    resultado = produtos.delete_one(
        {"_id": ObjectId(identificador)}
    )

    if resultado.deleted_count > 0:
        print("Produto excluido com sucesso!")
    else:
        print("Produto nao encontrado.")

except Exception as erro:
    print("Erro:", erro)

finally:
    cliente.close()
