import streamlit as st
from dados import inicializar_dados
from ui import (render_sidebar, render_login, render_cliente, 
                render_admin, render_entregador)

st.set_page_config(page_title="Sistema de E-Commerce", page_icon="🛍️", layout="wide")

inicializar_dados()

if st.session_state.usuario_atual:
    render_sidebar()

if st.session_state.usuario_atual is None:
    render_login()
elif st.session_state.usuario_atual["perfil"] == "Cliente":
    render_cliente()
elif st.session_state.usuario_atual["perfil"] == "Admin":
    render_admin()
elif st.session_state.usuario_atual["perfil"] == "Entregador":
    render_entregador()