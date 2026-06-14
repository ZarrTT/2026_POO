import streamlit as st
import datetime

class DAO:
    """Classe genérica (mãe) para persistência de dados em memória."""
    def __init__(self, session_key, dados_iniciais=None):
        self.session_key = session_key
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = dados_iniciais if dados_iniciais else []

    def listar_todos(self):
        return st.session_state[self.session_key]

    def salvar(self, objeto):
        st.session_state[self.session_key].append(objeto)


class ProdutoDAO(DAO):
    """Classe filha que herda de DAO para persistir Produtos."""
    def __init__(self):
        produtos_padrao = [
            {"id": 1, "nome": "Notebook Gamer", "preco": 450.00, "categoria": "Eletrônicos", "estoque": 5, "imagem": None},
            {"id": 2, "nome": "Teclado Mecânico", "preco": 350.00, "categoria": "Periféricos", "estoque": 10, "imagem": None},
            {"id": 3, "nome": "Mouse Sem Fio", "preco": 150.00, "categoria": "Periféricos", "estoque": 2, "imagem": None},
        ]
        super().__init__("produtos", produtos_padrao)

    def buscar_por_id(self, id_prod):
        for prod in self.listar_todos():
            if prod["id"] == id_prod:
                return prod
        return None


class VendaDAO(DAO):
    """Classe filha que herda de DAO para persistir Vendas/Pedidos."""
    def __init__(self):
        vendas_padrao = [
            {"id_venda": 101, "data": datetime.date(2026, 6, 10), "itens": "1x Notebook Gamer", "total": 405.00, "entregador": "Carlos MotoBoy", "status": "Em rota"}
        ]
        super().__init__("vendas_admin", vendas_padrao)


class EntregadorDAO(DAO):
    """Classe filha que herda de DAO para persistir Entregadores."""
    def __init__(self):
        entregadores_padrao = ["Carlos MotoBoy", "Ana Entregas"]
        super().__init__("entregadores", entregadores_padrao)


# Instanciação dos DAOs para uso global na aplicação
produto_dao = ProdutoDAO()
venda_dao = VendaDAO()
entregador_dao = EntregadorDAO()

# =====================================================================
# CONFIGURAÇÕES ADICIONAIS DO SISTEMA
# =====================================================================

st.set_page_config(page_title="E-Commerce DAO", page_icon="🛒", layout="wide")

if "promocoes" not in st.session_state:
    st.session_state.promocoes = {
        "Eletrônicos": {"desconto_pct": 10.0, "inicio": datetime.date(2026, 6, 1), "fim": datetime.date(2026, 6, 30)},
        "Periféricos": {"desconto_pct": 0.0, "inicio": datetime.date(2026, 6, 1), "fim": datetime.date(2026, 6, 30)}
    }

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

def obter_preco_atual(produto):
    cat = produto["categoria"]
    hoje = datetime.date.today()
    if cat in st.session_state.promocoes:
        promo = st.session_state.promocoes[cat]
        if promo["inicio"] <= hoje <= promo["fim"] and promo["desconto_pct"] > 0:
            desconto = produto["preco"] * (promo["desconto_pct"] / 100)
            return produto["preco"] - desconto, True, promo["desconto_pct"]
    return produto["preco"], False, 0.0

# NAVEGAÇÃO PRINCIPAL
st.sidebar.title("E-Commerce v3.0 (DAO)")
perfil = st.sidebar.radio("Selecione seu perfil:", ["Cliente", "Administrador (Admin)", "Entregador"])

# ==================== VISÃO DO CLIENTE ====================
if perfil == "Cliente":
    st.header("🛍️ Área do Cliente")
    aba_loja, aba_carrinho, aba_entregas = st.tabs(["Produtos", "Meu Carrinho", "Acompanhar Entrega"])
    
    with aba_loja:
        st.subheader("Vitrine Virtual")
        for prod in produto_dao.listar_todos():
            preco_final, em_promo, pct = obter_preco_atual(prod)
            col_img, col_detalhes, col_preco, col_acao = st.columns(4)
            
            with col_img:
                if prod["imagem"] is not None:
                    st.image(prod["imagem"], width=120)
                else:
                    st.write("🖼️ (Sem Imagem)")
            
            with col_detalhes:
                st.write(f"**{prod['nome']}**")
                st.caption(f"Categoria: {prod['categoria']} | Estoque: {prod['estoque']}")
            
            with col_preco:
                if em_promo:
                    st.markdown(f"~~R$ {prod['preco']:.2f}~~")
                    st.markdown(f"**🔥 R$ {preco_final:.2f}** ({int(pct)}% OFF)")
                else:
                    st.write(f"R$ {prod['preco']:.2f}")
                    
            with col_acao:
                if prod['estoque'] > 0:
                    if st.button("Adicionar", key=f"add_{prod['id']}"):
                        item_carrinho = prod.copy()
                        item_carrinho["preco_pago"] = preco_final
                        st.session_state.carrinho.append(item_carrinho)
                        st.success("Adicionado!")
                        st.rerun()
                else:
                    st.button("Esgotado", key=f"add_{prod['id']}", disabled=True)
            st.divider()

    with aba_carrinho:
        st.subheader("Carrinho")
        if not st.session_state.carrinho:
            st.info("Vazio")
        else:
            total = 0.0
            for idx, item in enumerate(st.session_state.carrinho):
                st.write(f"{item['nome']} - R$ {item['preco_pago']:.2f}")
                total += item['preco_pago']
            
            st.write(f"### Total: R$ {total:.2f}")
            if st.button("Finalizar Pedido", type="primary"):
                for item in st.session_state.carrinho:
                    orig = produto_dao.buscar_por_id(item['id'])
                    if orig:
                        orig['estoque'] -= 1
                
                novo_p = {
                    "id_venda": len(venda_dao.listar_todos()) + 101,
                    "data": datetime.date.today(),
                    "itens": ", ".join([i['nome'] for i in st.session_state.carrinho]),
                    "total": total,
                    "entregador": "Não Alocado",
                    "status": "Processando"
                }
                venda_dao.salvar(novo_p)
                st.session_state.carrinho = []
                st.success("Pedido realizado com sucesso!")
                st.rerun()

    with aba_entregas:
        st.subheader("Status das suas Entregas")
        st.dataframe(venda_dao.listar_todos(), use_container_width=True)

# ==================== VISÃO DO ADMIN ====================
elif perfil == "Administrador (Admin)":
    st.header("⚙️ Painel Administrativo")
    aba_img, aba_promo, aba_alocacao = st.tabs(["1. Upload de Imagens", "2. Controlar Promoções", "3. Alocar Entregadores"])
    
    with aba_img:
        st.subheader("Gerenciar Imagens dos Produtos")
        prod_selecionado = st.selectbox("Selecione o Produto:", [p["nome"] for p in produto_dao.listar_todos()])
        arquivo_img = st.file_uploader("Escolha uma imagem (PNG/JPG):", type=["png", "jpg", "jpeg"])
        if st.button("Salvar Imagem"):
            if arquivo_img is not None:
                p_obj = next(p for p in produto_dao.listar_todos() if p["nome"] == prod_selecionado)
                p_obj["imagem"] = arquivo_img.read()
                st.success(f"Imagem adicionada a {prod_selecionado}!")
                st.rerun()

    with aba_promo:
        st.subheader("Definir Promoção por Categoria")
        cat_sel = st.selectbox("Categoria:", list(st.session_state.promocoes.keys()))
        desc = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, value=10.0)
        dt_ini = st.date_input("Início da Promoção", datetime.date.today())
        dt_fim = st.date_input("Fim da Promoção", datetime.date.today() + datetime.timedelta(days=7))
        if st.button("Aplicar Promoção"):
            st.session_state.promocoes[cat_sel] = {"desconto_pct": desc, "inicio": dt_ini, "fim": dt_fim}
            st.success(f"Promoção aplicada à categoria {cat_sel}!")

    with aba_alocacao:
        st.subheader("Alocação de Pedidos para Entregadores")
        pedidos_pendentes = [v for v in venda_dao.listar_todos() if v["entregador"] == "Não Alocado"]
        if not pedidos_pendentes:
            st.info("Nenhum pedido aguardando alocação.")
        else:
            venda_id = st.selectbox("Selecione o ID do Pedido:", [v["id_venda"] for v in pedidos_pendentes])
            ent_sel = st.selectbox("Selecione o Entregador:", entregador_dao.listar_todos())
            if st.button("Alocar Entregador"):
                v_obj = next(v for v in venda_dao.listar_todos() if v["id_venda"] == venda_id)
                v_obj["entregador"] = ent_sel
                v_obj["status"] = "Pronto para Coleta"
                st.success(f"Pedido #{venda_id} alocado para {ent_sel}!")
                st.rerun()

# ==================== VISÃO DO ENTREGADOR ====================
elif perfil == "Entregador":
    st.header("🛵 Portal de Cadastro de Entregadores")
    
    novo_entregador = st.text_input("Nome do Novo Entregador:")
    if st.button("Cadastrar-se no Sistema"):
        if novo_entregador and novo_entregador not in entregador_dao.listar_todos():
            entregador_dao.salvar(novo_entregador)
            st.success("Cadastro realizado com sucesso!")
            st.rerun()
        else:
            st.error("Nome inválido ou já existente.")
            
    st.divider()
    st.subheader("Atualizar Status de Entrega")
    meus_pedidos = [v for v in venda_dao.listar_todos() if v["entregador"] != "Não Alocado"]
    if meus_pedidos:
        p_id = st.selectbox("Atualizar Pedido ID:", [m["id_venda"] for m in meus_pedidos])
        novo_status = st.selectbox("Novo Status:", ["Pronto para Coleta", "Em rota", "Entregue"])
