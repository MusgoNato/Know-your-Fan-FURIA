from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_recomendationsAI(nome, interesses, atividades, eventos, compras):
    prompt = f"""
    Gere recomendações personalizadas para um fã da organização de e-sports FURIA com base nas informações abaixo.

    Nome: {nome}
    Interesses: {interesses}
    Atividades: {atividades}
    Eventos favoritos: {eventos}
    Compras recentes: {compras}

    As recomendações devem ser específicas e curtas, úteis e relacionadas ao universo FURIA. Liste 1 a 3 ideias em tópicos, com linguagem objetiva sem usar emojis ou marcações.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um especialista em criar recomendações personalizadas para fãs de e-sports da FURIA, com base nas preferências e interesses individuais"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.8
    )

    return response.choices[0].message.content.strip().split("\n")