# Scraper ota
Applicazione estrazione automatica dei dati
## Requisiti
Usare python3

Installare le librerie

- selenium
- mysql connector
- re

Scaricare un driver per i browser Chrome e Mozilla

## Strumento per database
MYSQLWorkbench
## Procedimento
- Importare la struttura del database utilizzando il file 'tabelleota.sql' presente nella cartella 'tabelle'.
- *Inserire alla riga 16 del file 'estrazioneUrl.py' il vostro path del driver Chrome. 
- Eseguire 'estrazioneUrl.py' inserendo in input la città desiderata. es: python estrazioneUrl.py Pisa. 
- *Inserire alla riga 10 del file 'estrazioneInfoHotel.py' il vostro path del driver Chrome. 
- Eseguire il programma 'estrazioneInfoHotel.py' che permette di reperire tutte le info necessarie sugli hotel.
- *Inserire alla riga 23 del file 'NomePrezzoAnno.py' il vostro path del driver Mozzilla. 
- Eseguire il programma 'NomePrezzoAnno.py' per estrarre i prezzi di tutti gli hotel di tutti i giorni per un anno.
