# dados.py
import streamlit as st

def inicializar_dados():
    if "categorias" not in st.session_state:
        st.session_state.categorias = ["Eletrônicos", "Periféricos", "MousePad"]

    if "usuarios" not in st.session_state:
        st.session_state.usuarios = [
            {"email": "admin@email.com", "senha": "123", "perfil": "Admin", "nome": "Administrador"},
            {"email": "joao@email.com", "senha": "123", "perfil": "Cliente", "nome": "João Cliente"},
            {"email": "carlos@email.com", "senha": "123", "perfil": "Entregador", "nome": "Carlos Entregador"},
        ]

    if "produtos" not in st.session_state:
        st.session_state.produtos = [
            {
                "id": 1, 
                "nome": "Notebook Gamer", 
                "preco": 5000.00, 
                "categoria": "Eletrônicos", 
                "estoque": 3, 
                "em_promocao": False, 
                "preco_promocional": 0.0,
                "imagem": "https://asset.msi.com/resize/image/global/product/product_165087784033b7d73ab07e01bdae6c7fabdf1c9c42.png62405b38c58fe0f07fcef2367d8a9ba1/1024.png"
            },
            {
                "id": 2, 
                "nome": "Teclado Mecânico", 
                "preco": 250.00, 
                "categoria": "Periféricos", 
                "estoque": 10, 
                "em_promocao": False, 
                "preco_promocional": 0.0,
                "imagem": "https://fallen.cdn.magazord.com.br/img/2025/06/produto/3419/teclado-pantera-pro-tkl-3.png?null"
            },
            {
                "id": 3, 
                "nome": "Mousepad", 
                "preco": 130.00, 
                "categoria": "Periféricos", 
                "estoque": 3, 
                "em_promocao": False, 
                "preco_promocional": 0.0,
                "imagem": "https://fallen.cdn.magazord.com.br/img/2025/09/produto/4895/artwork-spirit-dragon-45x45.png?null"
            },
        ]

    if "vendas" not in st.session_state:
        st.session_state.vendas = []

    if "usuario_atual" not in st.session_state:
        st.session_state.usuario_atual = None

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []