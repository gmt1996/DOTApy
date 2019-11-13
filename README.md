# Scraper ota
Applicazione estrazione automatica dei dati
## Requisiti
1)python3
2)selenium
3)mysql connector
4)re
5)driver Chrome, driver Mozzilla
## Strumento per database
MYSQLWorkbench
## Procedimento
1)inserire tabelle in database utilizzando il file 'tabelleota.sql' nella cartella 'tabelle' \n
2)inserire alla riga 16 il vostro path del driver Chrome. successivamente fate girare file 'estrazioneUrl.py' inserendo in input la città desiderata
es: python3 estrazioneUrl.py Pisa. attendere la fine dell'esecuzione.
3)recuperati gli url, inserire alla riga 10 il vostro path del driver Chrome. Eseguire il programma 'estrazioneInfoHotel.py' che permette di reperire tutte le info necessarie sugli hotel
4)inserire alla riga 23 il vostro path del driver Mozzilla. Infine eseguire il programma 'NomePrezzoAnno.py' per estrarre i prezzi di tutti gli hotel di tutti i giorni per un anno.
