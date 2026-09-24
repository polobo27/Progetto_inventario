"""
main.py
Menu principale e interfaccia CLI dell'applicazione
"""

from inventory import Inventario
import os
import sys

class MenuPrincipale:
    """Gestisce il menu principale e la navigazione dell'applicazione"""
    def __init__(self):
        """inizializza il menu e l'inventario"""
        self.inventario = Inventario()
        self.running = True
    def startup(self):
        """Esegue il setup iniziale del programma"""
        print('Benvenuto nel Sistema di Gestione Inventario!')
        self.inventario.db.create_tables()
    def shutdown(self):
        """Arresta il programma"""
        self.inventario.close ()
        print('Arrivederci!')

    def clear_screen(self):
        """Pulisce lo schermo del terminale"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def stampa_header(self, titolo):
        """Stampa un header formattato con il titolo"""
        print('\n' + '=' * 60)
        print(titolo.center(60))
        print('=' * 60) 

    def stampa_separatore(self):
        """Stampa una linea di separazione"""
        print('-' * 60)
    def input_valido(self, prompt, tipo=str, valori_validi=None):
        """Chiede input all'utente con validazione"""
        while True:
            valore = input(prompt)
            if not valore:
                print('Input non può essere vuoto')
                continue    
            if valori_validi and valore not in valori_validi:
                print(f"Valore non valido. Accettati:{' , '.join(valori_validi)}")
                continue
            try:
                if tipo == int:
                    return int(valore)
                elif tipo == float:
                    return float(valore)
                else:
                    return str(valore)
            except ValueError:
                print (f'Inserisci un valore valido di tipo {tipo.__name__}')
            except KeyboardInterrupt:
                print('\n Operazione annullata')
                return None
    def menu_principale(self):
        """Mostra il menu principale e gestisce la navigazione"""
        while self.running: 
            self.stampa_header('MENU PRINCIPALE')
            print('\n1. Gestione Prodotti')
            print('2. Registra Movimento')
            print('3. Visualizza Inventario')
            print('4. Ricerca Prodotto')
            print('5. Report e Statistiche')
            print('6. Esci')
            scelta = self.input_valido('Scelta: ', str, ['1', '2', '3', '4', '5', '6'])
            if scelta == '1':
                self.menu_gestione_prodotti()
            elif scelta == '2':
                self.menu_registra_movimento()
            elif scelta == '3':
                self.menu_visualizza_inventario()
            elif scelta == '4':
                self.menu_ricerca_prodotto()
            elif scelta == '5':
                self.menu_report_e_statistiche()
            elif scelta == '6':
                self.menu_esci()
    def menu_gestione_prodotti(self):
        """Mostra il menu per gestire i prodotti"""
        while True:
            self.stampa_header('GESTIONE PRODOTTI')
            print('\n1. Aggiungi Prodotto')
            print('2. Visualizza Prodotti')
            print('3. Modifica Prodotto')
            print('4. Elimina Prodotto')
            print('5. Torna Indietro')
            scelta = self.input_valido('Scelta: ', str, ['1', '2', '3', '4', '5'])
            if scelta == '1':
                self.aggiungi_prodotto()
            elif scelta == '2':
                self.visualizza_tutti_prodotti()
            elif scelta == '3':
                self.modifica_prodotto()
            elif scelta == '4':
                self.elimina_prodotto()
            elif scelta == '5':
                break
    def aggiungi_prodotto(self):
        """Aggiunge un nuovo prodotto"""
        self.stampa_header('AGGIUNGI NUOVO PRODOTTO')
        nome = self.input_valido('Nome Prodotto:', str)
        categoria = self.input_valido('Categoria:', str)
        quantita = self.input_valido('Quantità:', int)
        prezzo = self.input_valido('Prezzo: ', float)
        self.inventario.aggiungi_prodotto(nome, categoria, quantita, prezzo)
        input('\nPremere INVIO per continuare...')
    def visualizza_tutti_prodotti(self):
        """Visualizza tutti i prodototi in una tabella"""
        self.stampa_header('ELENCO PRODOTTI')
        prodotti = self.inventario.visualizza_tutti_prodotti()
        if not prodotti:
            print('Nessun prodotto trovato')
        else:
            print('\n{:<5} {:<30} {:<15} {:<10} {:<10} {:<20}'.format( 'ID', 'Nome', 'Categoria', 'Quantità', 'Prezzo(€)', 'Data_Inserimento' )) 
            self.stampa_separatore()
            for id, nome, categoria, quantita, prezzo, data in prodotti:
                print('\n{:<5} {:<30} {:<15} {:<10} {:<10.2f} {:<20}'.format(id, nome[:29], categoria[:14], quantita, prezzo, data[:19]))  
            input('\nPremere INVIO per continuare...')  
    def modifica_prodotto(self):
        """Modifica un prodotto esistente"""
        self.stampa_header('MODIFICA PRODOTTO')
        prodotti = self.inventario.visualizza_tutti_prodotti()
        prodotto_id = self.input_valido('ID prodotto da modificare: ', int)
        prodotto = self.inventario.get_prodotto_per_id(prodotto_id)
        if not prodotto:
            print('Prodotto non trovato')
            return
        else:
            print(f'\nProdotto selezionato: {prodotto[1]}')
            print('(Lascia vuoto per non modificare)')
            nuovo_nome = input('Nuovo nome: ').strip() or None
            nuova_categoria = input('Nuova categoria: ').strip() or None
            prezzo_input = input('Nuovo prezzo: ').strip()
            nuovo_prezzo = float(prezzo_input) if prezzo_input else None
            self.inventario.modifica_prodotto(prodotto_id, nuovo_nome, nuova_categoria, nuovo_prezzo)
    def elimina_prodotto(self):
        """Elimina un prodotto dal database"""
        self.stampa_header('ELIMINA PRODOTTO')
        prodotti = self.inventario.visualizza_tutti_prodotti()
        prodotto_id = self.input_valido('ID prodotto da eliminare: ', int)
        prodotto = self.inventario.get_prodotto_per_id(prodotto_id)
        if not prodotto: 
            print('Prodotto non trovato')
            return 
        else: 
            print(f'\nProdotto selezionato: {prodotto[1]}')
            print('(Lascia vuoto per non eliminare)')
            conferma =  input('Sei sicuro di eliminare? (s/n): ').strip().lower()
            if conferma == 's':
                self.inventario.elimina_prodotto(prodotto_id)
                input('\nPremere INVIO per continuare...')
            else: 
                print('Eliminazione annullata')
                input('\nPremere INVIO per continuare...')
    def menu_registra_movimento(self):
        """Registra i movimenti (entrata/uscita) dei prodotti""" 
        self.stampa_header('REGISTRA MOVIMENTO')
        prodotti = self.inventario.visualizza_tutti_prodotti()
        prodotto_id = self.input_valido('ID prodotto: ', int)
        prodotto = self.inventario.get_prodotto_per_id(prodotto_id)
        if not prodotto: 
            print('Prodotto non trovato')
            return 
        else: 
            print(f'\nProdotto selezionato: {prodotto[1]}')
            print('(Lascia vuoto per non registrare movimenti)')
            tipo_movimento = self.input_valido('Tipo movimento (ENTRATA/USCITA): ', str, ['ENTRATA', 'USCITA'])
            quantita = self.input_valido('Quanti pezzi da movimentare: ', int)
            note = input('Note (opzionale): ').strip() or None
            self.inventario.registra_movimento(prodotto_id, tipo_movimento, quantita, note)
            input('\nPremere INVIO per continuare...')
    def menu_visualizza_inventario(self):
        """Visualizza i prodotti nell'inventario"""
        self.stampa_header('INVENTARIO')
        prodotti = self.inventario.visualizza_tutti_prodotti()
        self._visualizza_tabella_prodotti(prodotti)
        input('\nPremere INVIO per continuare...')
    def menu_ricerca_prodotto(self):
        """Cerca il prodotto"""
        self.stampa_header('RICERCA PRODOTTO')
        while True:
            prodotto_id = self.input_valido('ID prodotto da cercare: ', int)
            if prodotto_id == 0:
                break
            prodotto = self.inventario.get_prodotto_per_id(prodotto_id)
            if not prodotto: 
                print('prodotto non trovato')
                input('\nPremere INVIO per continuare...')
                continue
            else: 
                print('\n{:<5} {:<30} {:<15} {:<10} {:<10} {:<20}'.format( 'ID', 'Nome', 'Categoria', 'Quantità', 'Prezzo(€)', 'Data_Inserimento' ))
                self.stampa_separatore()
                print('\n{:<5} {:<30} {:<15} {:<10} {:<10.2f} {:<20}'.format(prodotto[0], prodotto[1][:29], prodotto[2][:14], prodotto[3], prodotto[4], prodotto[5][:19]))
                input('\nPremere INVIO per continuare...')
                break
    def menu_report_e_statistiche(self):
        """Mostra report e statistiche dell'inventario"""
        self.stampa_header('REPORT E STATISTICHE')
        prodotti = self.inventario.visualizza_tutti_prodotti()
        if not prodotti: 
            print('prodotto non trovato')
        else: 
            totale_prodotti = len(prodotti)
            valore_totale = sum(p[3] * p[4] for p in prodotti)
            quantita_totale = sum(p[3] for p in prodotti)
            print(f'\n Totale prodotti: {totale_prodotti}')
            print(f'Quantità totale: {quantita_totale} pezzi')
            print(f'Valore totale inventario: € {valore_totale:.2f}')
            input('\nPremere INVIO per continuare...')
    def menu_esci(self):
        """Arresta il programma e torna al sistema operativo"""
        self.running = False
        print('\n Arrivederci!')
    def _visualizza_tabella_prodotti(self, prodotti):
        """Versione interna: stampa solo la tabella senza header"""
        if not prodotti:
            print('Nessun prodotto trovato')
        else:
            print('\n{:<5} {:<30} {:<15} {:<10} {:<10} {:<20}'.format( 'ID', 'Nome', 'Categoria', 'Quantità', 'Prezzo(€)', 'Data_Inserimento' )) 
            self.stampa_separatore()
            for id, nome, categoria, quantita, prezzo, data in prodotti:
                print('{:<5} {:<30} {:<15} {:<10} {:<10.2f} {:<20}'.format(id, nome[:29], categoria[:14], quantita, prezzo, data[:19])) 
def main():
    """Funzione principale"""
    menu = MenuPrincipale()
    menu.startup()
    menu.menu_principale()

if __name__ == '__main__':
    main()       
        
