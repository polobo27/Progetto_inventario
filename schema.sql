-- Schema del Database per Sistema di Gestione Inventario 
-- Questo file definisce la struttura delle tabelle e delle relazioni tra di esse 

CREATE TABLE IF NOT EXISTS prodotti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50) NOT NULL,
    quantita INTEGER NOT NULL DEFAULT 0 CHECK (quantita >= 0),
    prezzo DECIMAL(10, 2) NOT NULL CHECK (prezzo > 0),
    data_inserimento DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabella per tracciare entrate e uscite

CREATE TABLE IF NOT EXISTS movimenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prodotto_id INTEGER NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    quantita INTEGER NOT NULL CHECK (quantita > 0),
    data_movimento DATETIME DEFAULT CURRENT_TIMESTAMP,
    note VARCHAR(200),
    FOREIGN KEY (prodotto_id) REFERENCES prodotti(id) ON DELETE RESTRICT 
);
