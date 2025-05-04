from backend.services.database import DataBase
import streamlit as st
from frontend.index import form_page, dashboard_page

def main():
    # Cria o banco de dados para depois ser adicionado os valores a ele
    db = DataBase()
    db.create_table()
    
    if "form_enviado" not in st.session_state:
        st.session_state["form_enviado"] = False

    menu_options = ["Formulário"]
    if st.session_state["form_enviado"]:
        menu_options.append("Dashboard")

    escolha = st.sidebar.selectbox("Navegue pelo app", menu_options)

    if escolha == "Formulário":
        form_page()
    elif escolha == "Dashboard":
        dashboard_page(st.session_state["dados"])

if __name__ == "__main__":
    main()