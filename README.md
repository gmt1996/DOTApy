# Scraper ota
Applicazione per l'estrazione automatica dei dati.
## Requisiti
Usare **python3**

Installare le seguenti librerie con **pip** https://pip.pypa.io/en/stable/quickstart/

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
- `utility.py`: file python contenente alcuni funzioni utilizzate nel file *estrazioneUrl.py*.
- `run.sh`: file esegubile che se lanciato esegue in ordine i file: *estrazioneUrl.py*,*estrazioneInfoHotel.py*, *NomePrezzoAnno.py*.
## Procedimento
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Modificare il file `config.ini` secondo le proprie credenziali.
- Eseguire il file `estrazioneUrl.py` inserendo in input: **-c** seguito dalla città desiderata, **-d** seguito tra apici da mese e anno dai quali si desidera iniziare l'estrazione e **-m** seguito dal numero di mesi per cui effettuare l'estrazione.

es: **python estrazioneUrl.py -c pisa -d "maggio 2020" -m 6**![estrazioneUrl](https://user-images.githubusercontent.com/51764993/76440538-47eef480-63be-11ea-9766-8862608a9321.png)
- Eseguire il file `estrazioneInfoHotel.py` o `estrazioneInfoHotelRec.py`(permette l'estrazione delle recensioni) inserendo in input **-c** seguito dalla città desiderata.
**es: python estrazioneInfoHotel -c pisa**
![estrazioneInfoHotel](https://user-images.githubusercontent.com/51764993/76440765-a4eaaa80-63be-11ea-8a33-f97a74a7fbfd.png)
- Eseguire il file `NomePrezzoAnno.py` che permette l'estrazione dei prezzi di tutti gli hotel per il periodo selezionato con il programma `estrazioneUrl.py`.
**es: python NomePrezzoAnno.py**
![NomePrezzoAnno](https://user-images.githubusercontent.com/51764993/76440840-bb910180-63be-11ea-9854-2e441c38939e.png)
