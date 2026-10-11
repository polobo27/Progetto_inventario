""" 
database.py
Gestione della connessione SQLite e operazioni base
"""
import sqlite3
class Database:
    """Classe per gestire la connessione al database SQLite"""
    def __init__(self, db_name='inventario.db'):
        """Inizializza la connessione al database"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Stabilisce la connessione al database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.execute('PRAGMA foreign_keys = ON')
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"x Errore connessione database: {e}") 
            raise

    def disconnect(self):
        """Chiude la connessione al database SQLite""" 
        if self.conn:
            self.conn.close()
            print('Connessione al database chiusa')

    def create_tables(self):
        """Crea le tabelle del file schema.sql"""  
        try:
            with open('schema.sql', 'r') as f:
                self.conn.executescript(f.read())
                self.conn.commit()
                print('Tabelle create con successo')
        except FileNotFoundError:
            print('File schema.sql non trovato')    
        except sqlite3.Error as e:
            print(f'Errore creazione tabelle: {e}')

    def execute_query(self, query, params=None):
        """esegue una query SELECT e ritorna i risultati"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Errore esecuzione query: {e}')
            return None

    def execute_query_one(self, query, params=None):
        """Esegue una query e ritorna un solo risultato"""  
        try:    
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f'Errore query: {e}')
            return None
    def execute_update(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f'Errore esecuzione update: {e}')
            self.conn.rollback()
            return False
                            





            

        

        