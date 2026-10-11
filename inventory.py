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
            SELECT p.id, p.nome, p.categoria, p.quantita, p.prezzo, p.data_inserimento
            FROM prodotti p
            ORDER BY p.id
            """
        return self.db.execute_query(query)
    
    def visualizza_movimenti_per_prodotto(self, prodotto_id):
        """Visualizza i movimenti per un prodotto specifico"""
        query = """
            SELECT p.nome, m.tipo, m.quantita, m.data_movimento, m.note
            FROM movimenti m
            JOIN prodotti p ON m.prodotto_id = p.id
            WHERE m.prodotto_id = ?
            ORDER BY m.data_movimento ASC
            """
        return self.db.execute_query(query, (prodotto_id,))
    
    def visualizza_tutti_movimenti(self):
        """Visualizza i movimenti di tutti i prodotti"""
        query = """
            SELECT m.prodotto_id, p.nome, m.tipo, m.quantita, m.data_movimento, m.note
            FROM movimenti m
            JOIN prodotti p ON m.prodotto_id = p.id
            ORDER BY m.data_movimento ASC
            """
        return self.db.execute_query(query)

    def get_prodotto_per_id(self, prodotto_id):
        """Ottiene un prodotto per il suo ID"""
        query = """
            SELECT p.id ,p.nome, p.categoria, p.quantita, p.prezzo, p.data_inserimento
            FROM prodotti p  
            WHERE p.id = ?
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
    
    def registra_movimento(self, prodotto_id, tipo, quantita, note):
        """Registra un movimento ENTRATA/USCITA"""
        prodotto = self.get_prodotto_per_id(prodotto_id)
        if not prodotto:
            print('Prodotto non trovato')
            return False
        elif tipo == 'USCITA' and quantita > prodotto[3]:
            print(f'Giacenza insufficiente: disponibili {prodotto[3]} pezzi')
            return False
        else: 
            query = """
                INSERT INTO movimenti (prodotto_id, tipo, quantita, note)
                VALUES (?,?,?,?)
                """
            success = self.db.execute_update(query, (prodotto_id, tipo, quantita, note))
            if success: 
                if tipo == 'ENTRATA':
                    nuova_quantita = prodotto[3] + quantita
                else:
                    nuova_quantita = prodotto[3] - quantita
                query_update = "UPDATE prodotti SET quantita = ? WHERE id = ?"
                self.db.execute_update(query_update, (nuova_quantita, prodotto_id))
                print('Movimento registrato con successo!')
                return True
            else:
                print('Errore nel registro del movimento')
                return False
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













