import streamlit as st
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de E-Commerce", page_icon="🛍️", layout="wide")

# =================================================================
# HERANÇA E EXCEÇÕES
# =================================================================
class EcommerceException(Exception): 
    """Exceção base para o sistema"""
    pass

class EmailDuplicadoError(EcommerceException):
    def __init__(self, email):
        super().__init__(f"O e-mail '{email}' já está cadastrado no sistema.")

class ProdutoSemCategoriaError(EcommerceException):
    def __init__(self, nome_produto):
        super().__init__(f"Não é possível cadastrar '{nome_produto}' sem uma categoria definida.")

class ProdutoVendidoError(EcommerceException):
    def __init__(self, nome_produto):
        super().__init__(f"Proibido excluir! O produto '{nome_produto}' já possui vendas registradas.")

class PromocaoInvalidaError(EcommerceException):
    def __init__(self):
        super().__init__("O preço promocional deve ser menor que o preço original do produto.")

# =================================================================
# SESSION STATE
# =================================================================
if "categorias" not in st.session_state:
    st.session_state.categorias = ["Eletrônicos", "Periféricos", "MousePad"]

if "usuarios" not in st.session_state:
    st.session_state.usuarios = [
        {"email": "admin@email.com", "senha": "123", "perfil": "Admin", "nome": "Administrador"},
        {"email": "joao@email.com", "senha": "123", "perfil": "Cliente", "nome": "João Cliente"},
        {"email": "carlos@email.com", "senha": "123", "perfil": "Entregador", "nome": "Carlos Entregador"},
    ]

# PRODUTOS ATUALIZADOS COM CAMPO DE IMAGEM
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


# =================================================================
# FUNÇÕES DO SISTEMA (RAISE)
# =================================================================
def cadastrar_cliente(nome, email, senha):
    for u in st.session_state.usuarios:
        if u["email"] == email:
            raise EmailDuplicadoError(email)
    st.session_state.usuarios.append({"email": email, "senha": senha, "perfil": "Cliente", "nome": nome})

# FUNÇÃO ATUALIZADA PARA RECEBER IMAGEM
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
        "imagem": imagem_url  # Salvando a imagem no dicionário
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


# =================================================================
# INTERFACE DO USUÁRIO (STREAMLIT)
# =================================================================

# Barra Superior / Logout
if st.session_state.usuario_atual:
    st.sidebar.write(f"Logado como: **{st.session_state.usuario_atual['nome']}** ({st.session_state.usuario_atual['perfil']})")
    if st.sidebar.button("Sair do Sistema", type="secondary"):
        st.session_state.usuario_atual = None
        st.session_state.carrinho = []
        st.rerun()

# -----------------------------------------------------------------
# VISITANTE / LOGIN 
# -----------------------------------------------------------------
if st.session_state.usuario_atual is None:
    st.title("🏪 Sistema de E-Commerce")
    
    aba_login, aba_cadastro = st.tabs(["🔐 Entrar", "📝 Abrir Conta"])
    
    with aba_login:
        st.subheader("Login")
        login_email = st.text_input("E-mail", key="login_email")
        login_senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar", type="primary"):
            usuario_encontrado = next((u for u in st.session_state.usuarios if u["email"] == login_email and u["senha"] == login_senha), None)
            if usuario_encontrado:
                st.session_state.usuario_atual = usuario_encontrado
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
                
    with aba_cadastro:
        st.subheader("Novo Cliente")
        cad_nome = st.text_input("Nome Completo")
        cad_email = st.text_input("E-mail para login")
        cad_senha = st.text_input("Senha", type="password")
        if st.button("Criar Conta"):
            try: 
                cadastrar_cliente(cad_nome, cad_email, cad_senha)
                st.success("Conta criada! Vá para a aba Entrar.")
            except EmailDuplicadoError as e:
                st.error(f"Erro: {e}")

# -----------------------------------------------------------------
# INTERFACE DO CLIENTE
# -----------------------------------------------------------------
elif st.session_state.usuario_atual["perfil"] == "Cliente":
    st.title("🛍️ Área do Cliente")
    tab_listar, tab_carrinho, tab_historico = st.tabs(["🔍 Produtos", "🛒 Carrinho", "📋 Minhas Compras / Entregas"])
    
    with tab_listar:
        for prod in st.session_state.produtos:
            # Layout reajustado para acomodar a coluna da imagem
            col_img, col1, col2, col3 = st.columns([1.2, 2, 1, 1])
            
            # Exibição da Imagem
            url_imagem = prod.get("imagem") if prod.get("imagem") else "https://placehold.co/300x300?text=Sem+Foto"
            col_img.image(url_imagem, use_container_width=True)
            
            col1.write(f"### {prod['nome']}")
            col1.caption(f"Categoria: {prod['categoria']}")
            
            preco_exibicao = prod["preco"]
            if prod.get("em_promocao"):
                col1.error("🔥 PROMOÇÃO!")
                preco_exibicao = prod["preco_promocional"]
                col2.write(f"~~R$ {prod['preco']:.2f}~~ \n\n **R$ {preco_exibicao:.2f}**")
            else:
                col2.write(f"\n\n**R$ {prod['preco']:.2f}**")
                
            if col3.button("Adicionar", key=f"add_{prod['id']}"):
                item_carrinho = prod.copy()
                item_carrinho["preco_final"] = preco_exibicao
                st.session_state.carrinho.append(item_carrinho)
                st.toast(f"{prod['nome']} adicionado ao carrinho!")
            st.divider()
                    
    with tab_carrinho:
        total_carrinho = sum(item["preco_final"] for item in st.session_state.carrinho)
        for idx, item in enumerate(st.session_state.carrinho):
            st.write(f"- {item['nome']} (R$ {item['preco_final']:.2f})")
        
        st.write(f"### Total: R$ {total_carrinho:.2f}")
        if st.session_state.carrinho and st.button("Comprar Carrinho", type="primary"):
            nova_venda = {
                "id_venda": len(st.session_state.vendas) + 101,
                "data": datetime.date.today(),
                "cliente": st.session_state.usuario_atual["email"],
                "itens": st.session_state.carrinho,
                "total": total_carrinho,
                "status": "Aguardando Entregador",
                "entregador_email": None
            }
            st.session_state.vendas.append(nova_venda)
            st.session_state.carrinho = []
            st.success("Compra efetuada!")
            st.rerun()
                
    with tab_historico:
        minhas_compras = [v for v in st.session_state.vendas if v["cliente"] == st.session_state.usuario_atual["email"]]
        for compra in reversed(minhas_compras):
            st.markdown(f"**Pedido #{compra['id_venda']}** | Total: R$ {compra['total']:.2f}")
            if compra['status'] == 'Entregue':
                st.success(f"Status da Entrega: {compra['status']} ✅")
            elif compra['status'] == 'Em Rota':
                st.warning(f"Status da Entrega: {compra['status']} 🚚")
            else:
                st.info(f"Status da Entrega: {compra['status']} ⏳")
            st.divider()

# -----------------------------------------------------------------
# INTERFACE DO ADMIN
# -----------------------------------------------------------------
elif st.session_state.usuario_atual["perfil"] == "Admin":
    st.title("⚙️ Painel Admin")
    tab_prod, tab_promo, tab_entrega = st.tabs(["📦 Cadastrar Produto", "🔥 Cadastrar Promoção", "🚚 Definir Entregador"])

    with tab_prod:
        p_nome = st.text_input("Nome do Produto")
        p_preco = st.number_input("Preço Original", min_value=0.0, step=10.0)
        p_cat = st.selectbox("Categoria", ["Selecione..."] + st.session_state.categorias)
        p_img = st.text_input("URL da Imagem (Ex: link da internet)", placeholder="https://exemplo.com/imagem.jpg")
        
        if st.button("Cadastrar Produto"):
            try:
                cadastrar_produto(p_nome, p_preco, p_cat, p_img)
                st.success(f"Produto '{p_nome}' cadastrado com sucesso!")
                st.rerun()
            except ProdutoSemCategoriaError as e:
                st.error(e)

    with tab_promo:
        st.write("Selecione um produto para colocar em promoção:")
        opcoes_prod = {p["id"]: p["nome"] for p in st.session_state.produtos}
        prod_selecionado = st.selectbox("Produto", options=opcoes_prod.keys(), format_func=lambda x: opcoes_prod[x])
        novo_preco = st.number_input("Preço Promocional", min_value=0.0)
        if st.button("Salvar Promoção"):
            try:
                cadastrar_promocao(prod_selecionado, novo_preco)
                st.success("Promoção ativada com sucesso!")
            except PromocaoInvalidaError as e:
                st.error(e)

    with tab_entrega:
        vendas_pendentes = [v for v in st.session_state.vendas if v["status"] == "Aguardando Entregador"]
        entregadores = [u for u in st.session_state.usuarios if u["perfil"] == "Entregador"]
        
        if not vendas_pendentes:
            st.success("Nenhuma venda aguardando entregador.")
        else:
            venda_sel = st.selectbox("Selecione a Venda", [v["id_venda"] for v in vendas_pendentes])
            entregador_sel = st.selectbox("Selecione o Entregador", [e["email"] for e in entregadores], format_func=lambda x: [e["nome"] for e in entregadores if e["email"] == x][0])
            
            if st.button("Atribuir Entregador"):
                for v in st.session_state.vendas:
                    if v["id_venda"] == venda_sel:
                        v["entregador_email"] = entregador_sel
                        v["status"] = "Em Rota"
                        st.success("Entregador designado!")
                        st.rerun()

# -----------------------------------------------------------------
# INTERFACE DO ENTREGADOR
# -----------------------------------------------------------------
elif st.session_state.usuario_atual["perfil"] == "Entregador":
    st.title("🚚 Painel do Entregador")
    st.subheader("Minhas Entregas")
    
    minhas_entregas = [v for v in st.session_state.vendas if v["entregador_email"] == st.session_state.usuario_atual["email"] and v["status"] == "Em Rota"]
    
    if not minhas_entregas:
        st.info("Nenhuma entrega pendente para você no momento.")
    else:
        for entrega in minhas_entregas:
            st.markdown(f"### Pedido #{entrega['id_venda']}")
            st.write(f"**Cliente:** {entrega['cliente']}")
            if st.button("Marcar como Entregue", key=f"entregar_{entrega['id_venda']}", type="primary"):
                for v in st.session_state.vendas:
                    if v["id_venda"] == entrega["id_venda"]:
                        v["status"] = "Entregue"
                st.success("Entrega confirmada!")
                st.rerun()
