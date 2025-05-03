from backend.services.database import DataBase
import streamlit as st
from frontend.formPage import index
import sqlite3

if __name__ == "__main__":
    # Cria o banco de dados para depois ser adicionado os valores a ele
    db = DataBase()
    db.create_table()


    # Renderização do form
    index()

    

