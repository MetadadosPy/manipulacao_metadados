from fastapi import HTTPException
import mysql.connector
from mysql.connector import Error
from .config import DB_CONFIG

def create_db_connection():
    """Cria e retorna uma conexão com o banco de dados"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao MySQL: {str(e)}")
