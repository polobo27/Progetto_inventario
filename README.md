## Sistema di Gestione Inventario
    Avendo lavorato per 3 anni in un magazzino, quando ho iniziato a studiare Python mi è venuto naturale provare a costruire qualcosa che conoscevo bene dal lato pratico: un gestionale da riga di comando per tenere traccia di prodotti, quantità e movimenti di magazzino.

    Il progetto copre un flusso completo. Aggiunta e modifica dei prodotti, carico/scarico dal magazzino, ricerca e qualche statistica di base. L'ho usato soprattutto per mettere in pratica Python e SQLite partendo da un caso reale, piuttosto che da un tutorial.

## Funzionalità 
-   Aggiunta di nuovi prodotti (nome, categoria, quantità, prezzo)
-   Modifica di prodotti esistenti 
-   Eliminazione di prodotti (bloccata se il prodotto ha movimenti registrati)
-   Visualizzazione dell'intero inventario in formato tabellare
-   Ricerca di un prodotto per ID
-   Report con statistiche generali (numero prodotti, quantità totale, valore totale)
-   Registrazione di movimenti di entrata/uscita (carico/scarico prodotti)

## Requisiti
-   Python 3.8 o superiore
-   SQLite (incluso in Python)

## Struttura del progetto 
|-- main.py         # Interfaccia a riga di comando e menu
|-- inventory.py    # Logica dell'inventario (operazioni su prodotti)
|-- database.py     # Gestione della connessione SQLite
|-- schema.sql      # Definizione delle tabelle del database
|-- README.md

## Installazione e avvio 
Clona il repository ed entra nella cartella del progetto:
git clone https://github.com/polobo27/Progetto_inventario.git
cd Progetto_inventario
Avvia l'applicazione: 
python main.py
Su alcuni sistemi (Linux/MacOS) potrebbe essere necessario usare python3 al posto di python:
python3 main.py
Al primo avvio, il programma crea automaticamente il database inventario.db e le tabelle definite in schema.sql

## Database
Il database SQLite è composto da due tabelle: 
-   Prodotti: anagrafica dei prodotti (id, nome, categoria, quantità, prezzo, data di inserimento)
-   Movimenti: storico delle entrate/uscite, collegato a prodotti tramite chiave esterna
Lo schema completo è definito in schema.sql

## Autore
Mirco Antoniello 