from fastapi import HTTPException
import mysql.connector
from mysql.connector import Error
from .config import DB_CONFIG

def create_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Utiliza as configurações definidas em DB_CONFIG.
    Em caso de erro, lança uma exceção HTTP 500 para o FastAPI.

    Returns:
        connection (mysql.connector.connection.MySQLConnection): Conexão ativa com o banco.

    Raises:
        HTTPException: Se ocorrer erro ao conectar ao banco.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        # Erro de conexão tratado e propagado para o FastAPI
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao MySQL: {str(e)}")
