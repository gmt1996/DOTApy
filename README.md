# Scraper ota
Applicazione estrazione automatica dei dati
## Requisiti
Usare python3

Installare le librerie con pip https://pip.pypa.io/en/stable/quickstart/

- selenium https://selenium-python.readthedocs.io/
- mysql connector https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
- re https://docs.python.org/3/library/re.html
- configparser https://docs.python.org/3/library/configparser.html
- argparse https://docs.python.org/3/library/argparse.html

Scaricare il driver per la vostra versione di Google Chrome da questo link https://chromedriver.chromium.org/downloads

## Strumento per database
MYSQLWorkbench
## Procedimento
- *Inserire nel vostro disco locale all'interno della cartella windows il file del vostro driver Chrome.
- Importare la struttura del database utilizzando il file 'Dump20200102.zip' nella cartella 'DBstruttura', creando così il DB (verificare che non sia presente un omonimo DB).
- Eseguire 'estrazioneUrl.py' inserendo in input la città desiderata. es: python estrazioneUrl.py Pisa. Oppure eseguendo estrazioneUrlconTK.py inserire la città desiderata nell'interfaccia che apparirà.
- Eseguire il programma 'estrazioneInfoHotel.py' che permette di reperire tutte le info necessarie sugli hotel.
- Eseguire il programma 'NomePrezzoAnno.py' per estrarre i prezzi di tutti gli hotel di tutti i giorni per un anno.
