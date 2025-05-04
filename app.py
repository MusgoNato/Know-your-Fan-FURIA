import streamlit as st
from frontend.index import form_page, dashboard_page

def main():
    st.set_page_config(
        page_title="Know Your Fan",
        page_icon="https://images.seeklogo.com/logo-png/52/1/furia-logo-png_seeklogo-526137.png",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    if "form_enviado" not in st.session_state:
        st.session_state["form_enviado"] = False

    menu_options = ["Formulário", "Dashboard"]

    escolha = st.sidebar.selectbox("Navegue pelo app", menu_options)

    if escolha == "Formulário":
        form_page()
    elif escolha == "Dashboard":
        if "dados" not in st.session_state:
            st.error("Envie o formulário")
        else:
            dashboard_page(st.session_state["dados"])

if __name__ == "__main__":
    main()