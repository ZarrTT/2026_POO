import streamlit as st
from models import (EmailDuplicadoError, ProdutoSemCategoriaError, 
                    PromocaoInvalidaError, ProdutoVendidoError)

def cadastrar_cliente(nome, email, senha):
    for u in st.session_state.usuarios:
        if u["email"] == email:
            raise EmailDuplicadoError(email)
    st.session_state.usuarios.append({"email": email, "senha": senha, "perfil": "Cliente", "nome": nome})

def cadastrar_produto(nome, preco, category, imagem_url):
    if not category or category == "Selecione...":
        raise ProdutoSemCategoriaError(nome) 
    
    novo_id = max([p["id"] for p in st.session_state.produtos]) + 1 if st.session_state.produtos else 1
    st.session_state.produtos.append({
        "id": novo_id, 
        "nome": nome, 
        "preco": preco, 
        "categoria": category, 
        "estoque": 10, 
        "em_promocao": False, 
        "preco_promocional": 0.0,
        "imagem": imagem_url
    })

def cadastrar_promocao(produto_id, novo_preco):
    for p in st.session_state.produtos:
        if p["id"] == produto_id:
            if novo_preco >= p["preco"]:
                raise PromocaoInvalidaError()
            p["em_promocao"] = True
            p["preco_promocional"] = novo_preco

def excluir_produto(produto_id, nome_produto):
    for venda in st.session_state.vendas:
        for item in venda["itens"]:
            if item["id"] == produto_id:
                raise ProdutoVendidoError(nome_produto)
    st.session_state.produtos = [p for p in st.session_state.produtos if p["id"] != produto_id]