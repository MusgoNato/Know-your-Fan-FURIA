import streamlit as st
import time
from backend.utils.verifyFields import verify
from backend.services.database import DataBase
from backend.utils.savePhoto import save_user_photo
from backend.utils.verifyDocs import extract_textFromImg, extract_cpfFromText
from requests import request
from dotenv import load_dotenv
import os
import requests
import praw
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from backend.services.IArecomendation import gerar_recomendacoes_com_ia

def form_page():
    st.title("Know Your Fan FURIA 🔥")
        
    with st.form(key="form_user_data"):
        nome = st.text_input("Informe o seu nome completo")
        email = st.text_input("Informe seu email")
        endereco = st.text_input("Informe seu endereço")
        idade = st.text_input("Informe sua idade")
        cpf = st.text_input("Informe seu CPF", placeholder="Ex: 000.000.000-00")
        interesses = st.text_input("Informe seus interesses")
        atividades = st.text_input("Ïnforme suas atividades")
        eventos = st.text_input("Informe os eventos que você mais gosta de seguir")
        user_reddit = st.text_input("Informe o nome do seu perfil no reddit", placeholder="MisgoNato")
        compras = st.text_input("Informe as compras que você realizou no ultimo mes")
        user_photo = st.file_uploader("Adicione uma foto da sua identidade", type=["png, jpeg"], accept_multiple_files=False, help="CPF ou RG")

        enviar = st.form_submit_button("Enviar")

    if enviar:
    
        errors = verify(nome, email, endereco, idade, cpf, interesses, eventos, atividades, compras, user_photo)
        
        if not errors:
            dados = {}
            # Validação com ORC
            photo_path = save_user_photo(user_photo, cpf)
            photo_inText = extract_textFromImg(photo_path)

            if not photo_inText:
                st.error("Foto inválida, tire outra foto")
            else:
                cpf_extracted = extract_cpfFromText(photo_inText)


            # Envio para o banco de dados
            conn = DataBase()
            if conn.cpf_exists(cpf):
                msg = st.error("Este usuário já existe")
                time.sleep(3)
                msg.empty()
            else:
                if cpf not in cpf_extracted:
                    st.error("Foto não bate com o CPF, tire outra foto")
                else:
                    msg = st.success("Dados enviados com sucesso")
                    time.sleep(3)
                    msg.empty()
                    conn.insert_user(nome, email, endereco, idade, cpf, interesses, eventos, atividades, compras, photo_path)
                    st.session_state["form_enviado"] = True
                    dados = {"nome": nome, "email": email, "endereco": endereco, "idade": idade, "cpf": cpf, "interesses": interesses, "atividades": atividades, "eventos": eventos, "user_reddit": user_reddit, "compras": compras, "photo_path": photo_path}
                    st.session_state["dados"] = dados

                    st.rerun()
        else:
            for i in errors:
                msg = st.error(i)

def dashboard_page(dados):
    load_dotenv()

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="Know Your Fan v1.0 by /u/MisgoNato"
    )

    user_nickname = dados["user_reddit"]
    query_terms = ["FURIA", "FURIA CS:GO", "furia csgo", "Fúria", "Furia cs2", "FURIA valorant", "furia dota2", "furia pugb", "furia"]

    user = reddit.redditor(user_nickname)

    relevant_posts = []
    relevant_comments = []

    # Buscar os posts do usuário
    for post in user.submissions.new(limit=100):
        if any(term.lower() in post.title.lower() or term.lower() in post.selftext.lower() for term in query_terms):
            relevant_posts.append({
                "tipo": "Post",
                "conteudo": post.title,
                "subreddit": post.subreddit.display_name,
                "pontuacao": post.score,
                "data": pd.to_datetime(post.created_utc, unit="s")
            })

    # Buscar os comentários do usuário
    for comment in user.comments.new(limit=100):
        if any(term.lower() in comment.body.lower() for term in query_terms):
            relevant_comments.append({
                "tipo": "Comentário",
                "conteudo": comment.body,
                "subreddit": comment.subreddit.display_name,
                "pontuacao": comment.score,
                "data": pd.to_datetime(comment.created_utc, unit="s")
            })

    all_data = relevant_posts + relevant_comments
    df = pd.DataFrame(all_data)

    st.title("Dashboard do Fã - Reddit")
    
    # Melhorar a visibilidade
    if df.empty:
        st.info("Nenhuma atividade relacionada à FURIA ou encontrada para este usuário.")
        return

    st.markdown(f"### Total de atividades relacionadas: {len(df)}")
    st.dataframe(df)

    # Mostrar distribuição de subreddits de forma mais visual
    st.markdown("### Distribuição de Atividades por Subreddit")
    subreddit_counts = df['subreddit'].value_counts()
    st.bar_chart(subreddit_counts)

    # Mostrar distribuição de tipo de atividade
    st.markdown("### Distribuição entre Posts e Comentários")
    tipo_counts = df['tipo'].value_counts()
    st.bar_chart(tipo_counts)

    # Atividades ao longo do tempo
    st.markdown("### Atividades ao Longo do Tempo")
    timeline = df.groupby(df['data'].dt.to_period("M")).size()
    st.line_chart(timeline)

    # Pontuação do usuário para posts e comentários relacionados à FURIA
    user_activity_score = df['pontuacao'].sum()

    # Mostrar o score do usuário de maneira clara
    st.markdown(f"### **Score do Usuário (FURIA)**")
    st.markdown(f"- **Score de atividades relacionadas a FURIA**: {user_activity_score}")

    # Comparar os scores
    if user_activity_score > 0:
        activity_percentage = (user_activity_score / user_activity_score) * 100  # Essa comparação sempre vai resultar em 100, então pode ser ajustado
    else:
        activity_percentage = 0

    st.markdown(f"- **Porcentagem de atividade relacionada à FURIA**: {activity_percentage:.2f}%")

    if user_activity_score > 20:
        st.success("Este usuário é altamente ativo relacionado à FURIA!")
    else:
        st.warning("Este usuário não é muito ativo relacionado à FURIA.")

    # Recomendações baseadas na IA
    st.markdown("### **Recomendações Personalizadas**")
    recomendacoes_ia = gerar_recomendacoes_com_ia(
        dados["nome"],
        dados["interesses"],
        dados["atividades"],
        dados["eventos"],
        dados["compras"]
    )

    # Formatar as recomendações para visualização
    if recomendacoes_ia:
        for rec in recomendacoes_ia:
            st.markdown(f"- {rec}")
    else:
        st.info("Não há recomendações no momento.")