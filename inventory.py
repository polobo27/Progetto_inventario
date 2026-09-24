"""
inventory.py
Classe principale per la gestione della logica di business
"""
from database import Database

class Inventario:
    """classe per gestire tutte le operazioni di inventario"""
    def __init__(self, db_name='inventario.db'):
        """inizializza l'inventario connettendosi al database"""
        self.db = Database(db_name)
        self.db.connect()
    
    def close(self):
        """Chiude la connessionne al database"""
        self.db.disconnect()

    def aggiungi_prodotto(self, nome, categoria, quantita, prezzo):
        """Aggiunge un nuovo prodotto con nome, categoria, quantita e prezzo"""
        query = """
            INSERT INTO prodotti (nome, categoria, quantita, prezzo)
            VALUES (?,?,?,?)
            """
        success = self.db.execute_update(query, (nome, categoria, quantita, prezzo))
        if success:
            print('Il prodotto è stato aggiunto con successo!')
        else: 
            print('Il prodotto non è stato aggiunto')
        return success

    def visualizza_tutti_prodotti(self):
        """Visualizza tutti i prodotti del database"""
        query = """
            SELECT id, nome, categoria, quantita, prezzo, data_inserimento
            FROM prodotti
            ORDER BY categoria, nome
            """
        return self.db.execute_query(query)

    def get_prodotto_per_id(self, prodotto_id):
        """Ottiene un prodotto per il suo ID"""
        query = """
            SELECT id, nome, categoria, quantita, prezzo, data_inserimento
            FROM prodotti   
            WHERE id = ?
            """
        return self.db.execute_query_one(query, (prodotto_id,))

    def modifica_prodotto(self, prodotto_id, nome=None, categoria=None, prezzo=None):
        """Modifica i dati di un prodotto (nome, categoria, prezzo)"""
        updates = []
        params = []
        if nome:
            updates.append("nome = ?")
            params.append(nome)
        if categoria:
            updates.append("categoria = ?")
            params.append(categoria)
        if prezzo is not None:
            updates.append("prezzo = ?")
            params.append(prezzo)
        if not updates:
            print('Nessun campo da modificare')
            return False
        params.append(prodotto_id) 
        query = f"UPDATE prodotti SET {', '.join(updates)} WHERE id = ?"
        success = self.db.execute_update(query, tuple(params))
        if success:
            print('Prodotto modificato con successo!')
        else:
            print('Errore nella modifica del prodotto')
        return success
    def elimina_prodotto(self, prodotto_id):
        """Elimina un prodotto dal database"""
        query_check = """
                SELECT COUNT(*) FROM movimenti WHERE prodotto_id = ?
                """
        result = self.db.execute_query_one(query_check, (prodotto_id,))
        if result and result[0] > 0:
            print(f'Non puoi eliminare il prodotto: ha {result[0]} movimenti registrati')
            return False
        query = 'DELETE FROM prodotti WHERE id = ?'
        success = self.db.execute_update(query, (prodotto_id,))
        if success:
            print('Prodotto eliminato correttamente!')
        else:
            print("Errore nell eliminazione del prodotto")
        return success













