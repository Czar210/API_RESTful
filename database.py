# database.py

import sqlite3

def create_connection(db_file="mydatabase.db"):
    """Cria (se não existir) ou conecta a um banco de dados SQLite."""
    conn = sqlite3.connect(db_file, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conn

def create_table(conn):
    """Cria a tabela para armazenar dados de partidas, se ela ainda não existir."""
    sql_create_matches_table = """
    CREATE TABLE IF NOT EXISTS matches (
        matchId TEXT,
        Player_name TEXT,
        championName TEXT,
        kills INTEGER,
        deaths INTEGER,
        assists INTEGER,
        win BOOLEAN,
        gameCreation INTEGER,
        gameDuration INTEGER,
        bountyLevel INTEGER,
        damageDealtToObjectives INTEGER,
        doubleKills INTEGER,
        tripleKills INTEGER,
        goldEarned INTEGER,
        PRIMARY KEY (matchId, Player_name)
    );
    """
    conn.execute(sql_create_matches_table)
    conn.commit()

def insert_matches(conn, data_list):
    """Insere os dados de partidas no banco."""
    sql_insert = """
    INSERT OR REPLACE INTO matches (
        matchId, Player_name, championName, kills, deaths, assists, win,
        gameCreation, gameDuration, bountyLevel, damageDealtToObjectives,
        doubleKills, tripleKills, goldEarned
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    conn.executemany(sql_insert, data_list)
    conn.commit()

def query_player_matches(conn, player_name_with_tag):
    """Busca todas as partidas de um jogador no banco."""
    sql_select = """
    SELECT * FROM matches WHERE Player_name = ? ORDER BY gameCreation DESC
    """
    cursor = conn.execute(sql_select, (player_name_with_tag,))
    
    # Converter os resultados para uma lista de dicionários
    columns = [column[0] for column in cursor.description]
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row)))
    
    return result if result else []