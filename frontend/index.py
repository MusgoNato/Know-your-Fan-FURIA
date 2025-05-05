import streamlit as st
import os
import praw
import pandas as pd
import time
from dotenv import load_dotenv
from backend.utils.verifyFields import verify
from backend.utils.savePhoto import save_user_photo
from backend.utils.verifyDocs import extract_textFromImg, extract_cpfFromText
from backend.services.AIrecomendation import get_recomendationsAI

def form_page():

    st.markdown("""
        <style>
        .stTextInput > div > input {
            background-color: #f0f0f5;
            border-radius: 8px;
            padding: 8px;
        }
        .stButton button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.image("https://vectorseek.com/wp-content/uploads/2023/04/Furia-Esports-Logo-Vector.jpg", width=150)
    st.title("Know Your Fan FURIA 🔥")
    st.markdown("### 👤 Formulário do Fã")

    with st.form(key="form_user_data"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome completo")
            email = st.text_input("Email")
            idade = st.text_input("Idade")
            cpf = st.text_input("CPF", placeholder="Ex: 000.000.000-00")
            interesses = st.text_input("Interesses", placeholder="Ex: valorant, cs go, lol, etc")

        with col2:
            endereco = st.text_input("Endereço")
            atividades = st.text_input("Quais são as suas atividades no dia a dia?")
            eventos = st.text_input("Quais são os eventos você mais acompanha?")
            user_reddit = st.text_input("Perfil no Reddit", placeholder="JaoJoao")
            compras = st.text_input("Quais as suas últimas compras feitas no último mês?")

        user_photo = st.file_uploader("📸 Foto da identidade (CPF ou RG)", type=["png", "jpeg"], accept_multiple_files=False)

        enviar = st.form_submit_button("Enviar")

    if enviar:
        errors = verify(nome, email, endereco, idade, cpf, interesses, eventos, atividades, compras, user_photo)

        if not errors:
            dados = {}
            photo_path = save_user_photo(user_photo, cpf)
            photo_inText = extract_textFromImg(photo_path)

            if not photo_inText:
                st.error("Foto inválida, tire outra foto")
                return

            cpf_extracted = extract_cpfFromText(photo_inText)

            if cpf not in cpf_extracted:
                st.error("Foto não bate com o CPF, tire outra foto")
            else:
                with st.spinner("Enviando dados..."):
                    time.sleep(2)
                    st.session_state["form_enviado"] = True
                    dados = {"nome": nome, "email": email, "endereco": endereco, "idade": idade, "cpf": cpf, "interesses": interesses, "atividades": atividades, "eventos": eventos, "user_reddit": user_reddit, "compras": compras, "photo_path": photo_path}
                    st.session_state["dados"] = dados

                time.sleep(2)
                st.success("Dados enviados com sucesso!")
        else:
            for i in errors:
                st.error(i)

def dashboard_page(dados):
    """Pagina para mostrar os dados pegos do usuario no reddit"""
    
    # Variaveis de ambiente
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="Know Your Fan v1.0 by /u/MisgoNato"
    )

    # Filtro de pesquisa
    user_nickname = dados["user_reddit"]
    query_terms = ["FURIA", "FURIA CS:GO", "furia csgo", "Fúria", "Furia cs2", "FURIA valorant", "furia dota2", "furia pugb", "furia"]

    # Requisição a API do Reddit
    user = reddit.redditor(user_nickname)

    relevant_posts = []
    relevant_comments = []

    # Busca de posts
    for post in user.submissions.new(limit=100):
        if any(term.lower() in post.title.lower() or term.lower() in post.selftext.lower() for term in query_terms):
            relevant_posts.append({
                "tipo": "Post",
                "conteudo": post.title,
                "subreddit": post.subreddit.display_name,
                "pontuacao": post.score,
                "data": pd.to_datetime(post.created_utc, unit="s")
            })

    # Busca de comentarios
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

    st.title("📊 Dashboard do Fã - Reddit")

    if df.empty:
        st.info("Nenhuma atividade relacionada à FURIA foi encontrada.")
        return

    # Graficos
    col1, col2 = st.columns(2)
    col1.metric("Atividades relacionadas", len(df))
    col2.metric("Pontuação Total", df['pontuacao'].sum())

    st.dataframe(df)

    st.markdown("### Distribuição por Subreddit")
    st.bar_chart(df['subreddit'].value_counts())

    st.markdown("### Posts vs Comentários")
    st.bar_chart(df['tipo'].value_counts())

    st.markdown("### Atividades ao Longo do Tempo")
    timeline = df.groupby(df['data'].dt.to_period("M")).size()
    st.line_chart(timeline)

    # Score do usuario
    user_activity_score = df['pontuacao'].sum()

    st.markdown("### ⭐ Score do Usuário FURIA")
    if user_activity_score > 20:
        st.success("Usuário altamente ativo sobre FURIA!")
    else:
        st.warning("Usuário com pouca atividade sobre FURIA.")

    # Recomendações IA
    st.markdown("### 🔮 Recomendações Personalizadas")
    recomendacoes_ia = get_recomendationsAI(
        dados["nome"], dados["interesses"], dados["atividades"], dados["eventos"], dados["compras"]
    )

    if recomendacoes_ia:
        for rec in recomendacoes_ia:
            rec = rec.strip()
            if rec:
                st.success(f"✅ {rec}")
    else:
        st.info("Não há recomendações no momento.")