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

Scaricare il driver per la vostra versione di Google Chrome da questo link https://chromedriver.chromium.org/downloads.

## Struttura progetto
- `DBstruttura.sql`: file in formato sql che contiene la struttura del database utilizzato.
- `config.ini`: file di configurazione per l'accesso al database.
- `estrazioneUrl.py`: file python che esegue l'estrazione delle url per la città selezionata e per il periodo di tempo specificato.
- `estrazioneInfoHotel.py`: file python che esegue l'estrazione delle informazioni principali di tutti gli hotel per una specificata città.
- `estrazioneInfoHotelRec.py`: programma identico al precedente al quale aggiunge l'estrazione di tutte le recensioni di ogni singolo hotel, a discapito del tempo impiegato che sarà considerevolmente più lungo.
- `estrazionePrezzo.py`: file python che esegue l'estrazione dei prezzi di tutti gli hotel utilizzando le url estratte dal file *estrazioneUrl.py*.
- `utility.py`: file python contenente funzioni utilizzate nel file *estrazioneUrl.py*.
- `run.sh`: file con estensione sh che esegue in ordine i file: *estrazioneUrl.py*, *estrazioneInfoHotel.py*, *estrazionePrezzo.py*.

## Procedimento per l'estrazione informazioni e recensioni degli hotel
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Modificare il file `config.ini` secondo le proprie credenziali.
- Eseguire il file `estrazioneInfoHotel.py` o `estrazioneInfoHotelRec.py`(che permette l'estrazione delle recensioni).
  * Argomenti utilizzabili:
    * **-c** seguito dalla città desiderata.
    * **-v** per il prinmo livello di debug, **-vv** per il secondo
    * **-ph** seguito da un numero intero per stabilire quante pagine di hotel estrarre, se omesso si esguirà l'estrazione su tutte.
    * **-nr** seguito da un numero intero per stabilire quante pagine di recensioni per ogni hotel estrarre, se non specificato verranno estratte tutte.

 inserendo in input **-c** seguito dalla città desiderata, per ricevere messagi importanti in output inserire **-v** e nel caso in cui se si volesse ricevere tutte le informazioni di debug in output inserire **-vv**.
**Esempio: python estrazioneInfoHotel -c pisa -ph 2 -nr 1 -vv**
![estrazioneInfoHotel](https://user-images.githubusercontent.com/51764993/76440765-a4eaaa80-63be-11ea-8a33-f97a74a7fbfd.png)
## Procedimento per l'estrazione dei prezzi, in una fascia temporale definita, degli hotel
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Modificare il file `config.ini` secondo le proprie credenziali.
- Eseguire il file `estrazioneUrl.py` inserendo in input: **-c** seguito dalla città desiderata, **-d** seguito ,tra doppi apici, da mese e anno dai quali si desidera iniziare l'estrazione e **-m** seguito dal numero di mesi per cui effettuare l'estrazione.
**Esempio: python estrazioneUrl.py -c pisa -d "maggio 2020" -m 6**
![estrazioneUrl](https://user-images.githubusercontent.com/51764993/76440538-47eef480-63be-11ea-9766-8862608a9321.png)
- Eseguire il file `estrazionePrezzo.py` che permette l'estrazione dei prezzi di tutti gli hotel per il periodo selezionato con il programma `estrazioneUrl.py`.
**Esempio: python estrazionePrezzo.py**
![estrazionePrezzo](https://user-images.githubusercontent.com/51764993/76615809-0deb3300-6523-11ea-838d-a250a9ec145b.png)
