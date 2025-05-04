# Know-your-Fan-FURIA

# Estrutura do Projeto
```
Know-your-Fan-FURIA/
├── assets/
│   ├── user/
├── backend/
│   ├── services/
│   │   └── AIrecomendation.py
│   └── utils/
│       ├── savePhoto.py
│       ├── verifyDocs.py
│       └── verifyFields.py
├── frontend/
│   └── index.py
├── .env.example
├── .gitignore
├── app.py
├── logo.png
├── README.md
└── requirements.txt 
```

# Instalação
1. Vá ao terminal e clone o repositório
    ```
    https://github.com/MusgoNato/Know-your-Fan-FURIA.git
    ``` 
    Acesse a pasta do projeto
    ```
    cd Know-your-Fan-FURIA
    ```
2. Crie um ambiente virtual
    
    - No terminal digite os códigos abaixo:
        
        ```
        python -m venv venv
        ```
        ```
        venv\Scripts\activate
        ```
3. Instale as dependencias
    ```
    pip install -r requirements.txt
    ```

# Configurações
Renomeie o arquivo `.env.example para` para `.env` e configure as seguintes variáveis de ambiente:
```
CLIENT_ID=SEU_CLIENT_ID_DO_REDDIT    # Fica localizado abaixo do icone do aplicativo criado

CLIENT_SECRET=SEU_CLIENT_SECRET_DO_REDDIT # Fica localizado no campo secret
```

Cada uma dessas variaveis você pode acessar criando um aplicativo de desenvolvedor do tipo script nesta página do reddit: [API REDDIT](https://www.reddit.com/prefs/apps)

# Pré-Requisitos
- Python 3.9+
- Conta no Reddit (para acessar a API)
- Tesseract OCR instalado e no PATH (usado na extração de CPF via imagem). Durante a instalação, marque a opção “Add to PATH”. [TESSERACT](https://tesseract-ocr.github.io/tessdoc/Downloads.html)

# Execução do projeto
No terminal execute a linha de código a seguir:
```
streamlit run app.py
```

# Bibliotecas utilizadas
- openai==1.77.0
- pandas==2.2.3
- Pillow==11.2.1
- praw==7.8.1
- pytesseract==0.3.13
- python-dotenv==1.1.0
- streamlit==1.42.0


# 👨‍💻 Desenvolvedor

Este projeto foi desenvolvido por:

Hugo Josue
- 📧 hugojosue03@gmail.com
- 🔗 [LinkedIn](www.linkedin.com/in/hugo-josue-25246525b) | [GitHub](https://github.com/MusgoNato)