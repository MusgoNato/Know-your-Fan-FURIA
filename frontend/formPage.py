import streamlit as st
import time
from backend.utils.verifyFields import verify
from backend.services.database import DataBase

def index():
    st.title("Know Your Fan FURIA 🔥")
    
    error = False
    
    with st.form(key="form_user_data"):
        nome = st.text_input("Qual o seu nome completo?")
        email = st.text_input("Qual seu email?")
        endereco = st.text_input("Informe seu endereço")
        idade = st.text_input("Informe sua idade")
        cpf = st.text_input("Informe seu CPF")
        interesses = st.text_input("Informe seus interesses")
        atividades = st.text_input("Ïnforme suas atividades")
        eventos = st.text_input("Informe os eventos que você mais gosta de seguir")
        compras = st.text_input("Informe as compras que você realizou no ultimo mes")
        user_photo = st.file_uploader("Adicione uma foto de perfil para validarmos sua identidade", type=["png, pneg"], accept_multiple_files=False)

        enviar = st.form_submit_button("Enviar")

    if enviar:
        errors = verify(nome, email, endereco, idade, cpf, interesses, eventos, atividades, compras, user_photo)
        if not errors:
            msg = st.success("Dados enviados com sucesso")
            time.sleep(3)
            msg.empty()

            # Envio para o banco de dados
            conn = DataBase()
            conn.insert_user(nome, email, endereco, idade, cpf, interesses, eventos, atividades, compras, user_photo)

        else:
            for i in errors:
                msg = st.error(i)




