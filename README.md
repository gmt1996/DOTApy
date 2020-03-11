# Scraper ota
Applicazione per l'estrazione automatica dei dati.
## Requisiti
Usare **python3**

Installare le librerie con **pip** https://pip.pypa.io/en/stable/quickstart/

- `selenium` https://selenium-python.readthedocs.io/
- `mysql connector` https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
- `re` https://docs.python.org/3/library/re.html
- `configparser` https://docs.python.org/3/library/configparser.html
- `argparse` https://docs.python.org/3/library/argparse.html

Scaricare il driver per la vostra versione di Google Chrome da questo link https://chromedriver.chromium.org/downloads

## Struttura progetto
- `DBstruttura.sql`: file in formato sql che contiene la struttura del database utilizzato.
- `config.ini`: file di configurazione per l'accesso al database.
- `estrazioneUrl.py`: file python che esegue l'estrazione delle url per la citta selezionata e per il periodo di tempo specificato.
- `estrazioneInfoHotel.py`: file python che esegue l'estrazione delle informazioni principali di tutti gli hotel per una specificata città.
- `estrazioneInfoHotelRec.py`: programma identico al precedente al quale aggiunge l'estrazione di tutte le recensioni di ogni singolo hotel, a discapito del tempo impiegato che sarà considerevolmente più lungo.
- `NomePrezzoAnno.py`: file python che esegue l'estrazione dei prezzi di tutti gli hotel utilizzando le url estratte dal file *estrazioneUrl.py*
## Procedimento
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Eseguire il file `estrazioneUrl.py` inserendo in input: **-c** seguito dalla città desiderata, **-d** seguito da mese e anno, tra apici, dal quale si desidera iniziare l'estrazione e **-m** seguito dal numero di mesi per cui effettuare l'estrazione. es: python estrazioneUrl.py -c pisa -d "maggio 2020" -m 6![estrazioneUrl](https://user-images.githubusercontent.com/51764993/76440538-47eef480-63be-11ea-9766-8862608a9321.png)
- Eseguire il programma 'estrazioneInfoHotel.py' che permette di reperire tutte le info necessarie sugli hotel.![estrazioneInfoHotel](https://user-images.githubusercontent.com/51764993/76440765-a4eaaa80-63be-11ea-8a33-f97a74a7fbfd.png)
- Eseguire il programma 'NomePrezzoAnno.py' per estrarre i prezzi di tutti gli hotel di tutti i giorni per un anno.![NomePrezzoAnno](https://user-images.githubusercontent.com/51764993/76440840-bb910180-63be-11ea-9854-2e441c38939e.png)
