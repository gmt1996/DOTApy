# Scraper DOTApy
<!---Applicazione per l'estrazione automatica dei dati.-->
Software sviluppato in Python per l'estrazione automatica dei dati.
L'applicazione si concentra su due diversi obiettivi: il primo riguarda l'estrazione di informazioni e di recensioni degli hotel per una determinata città, il secondo (che può essere o meno correlato con il primo) riguarda l'estrazione dei prezzi degli hotel per un periodo di tempo prestabilito.
## Requisiti
Usare **python3**

Installare le seguenti librerie utilizzando **pip** https://pip.pypa.io/en/stable/quickstart/

- `selenium` https://selenium-python.readthedocs.io/
- `mysql connector` https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
- `re` https://docs.python.org/3/library/re.html
- `configparser` https://docs.python.org/3/library/configparser.html
- `argparse` https://docs.python.org/3/library/argparse.html

Scaricare il driver per la vostra versione di Google Chrome da questo link https://chromedriver.chromium.org/downloads.

## Struttura progetto
- `DBstruttura.sql`: file in formato sql che contiene la struttura del database utilizzato.
- `config.ini`: file di configurazione per l'accesso al database.
- `URIextractor.py`: file python che esegue l'estrazione delle url per la città selezionata e per il periodo di tempo specificato.
- `InfoReviews.py`: file python che esegue l'estrazione delle informazioni principali di tutti gli hotel per una specificata città.
- `Prices.py`: file python che esegue l'estrazione dei prezzi di tutti gli hotel utilizzando le url estratte dal file *URIextractor.py*.
- `utility.py`: file python contenente funzioni utilizzate nel file *URIextractor.py*.
- `run.sh`: file con estensione sh che esegue in ordine i file: *URIextractor.py*, *InfoReviews.py*, *Prices.py*.

## Procedimento di estrazione delle informazioni e delle recensioni per gli hotel di una determinata città
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Modificare il file `config.ini` secondo le proprie credenziali.
- Eseguire il file `InfoReviews.py`.
  * Argomenti utilizzabili:
    * **-c** seguito dalla città desiderata. **Obbligatorio**.
    * **-v** per il primo livello di debug, **-vv** per il secondo con conseguente aumento di messaggi in output. Se omesso mostrerà in output solo messaggi di errore. **Facoltativo**.
    * **-ph** seguito da un numero intero per stabilire quante pagine di hotel estrarre. Se omesso sarà esguita l'estrazione su tutte. **Facoltativo**.
    * **-nr** seguito da un numero intero per stabilire quante pagine di recensioni per ogni hotel estrarre. Se non specificato verranno estratte informazioni da tutte le pagini disponibili. **Facoltativo**.
- Esempio: **python InfoReviews.py -c pisa -ph 2 -nr 1 -vv**
![estrazioneInfohotelRec](https://user-images.githubusercontent.com/51764993/80222437-1d43bd00-8647-11ea-86ac-a9fbe40b9f50.png)
---
## Procedimento di estrazione dei prezzi per gli hotel di una determinata città
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Modificare il file `config.ini` secondo le proprie credenziali.
- Eseguire il file `URIextractor.py`
  * Argomenti utilizzabili:
    * **-c** seguito dalla città desiderata. **Obbligatorio**.
    * **-d** seguito ,tra doppi apici, da mese e anno dai quali si desidera iniziare l'estrazione. **Obbligatorio**.
    * **-m** seguito dal numero di mesi per cui effettuare l'estrazione. **Obbligatorio**.
<!---inserendo in input: **-c** seguito dalla città desiderata, **-d** seguito ,tra doppi apici, da mese e anno dai quali si desidera iniziare l'estrazione e **-m** seguito dal numero di mesi per cui effettuare l'estrazione.-->
- Esempio: **python URIextractor.py -c pisa -d "maggio 2020" -m 6**
![estrazioneUrl](https://user-images.githubusercontent.com/51764993/76440538-47eef480-63be-11ea-9766-8862608a9321.png)
- Eseguire il file `Prices.py` che permette l'estrazione dei prezzi di tutti gli hotel per il periodo selezionato con il programma `URIextractor.py`.
Esempio: **python Prices.py**
![estrazionePrezzo](https://user-images.githubusercontent.com/51764993/76615809-0deb3300-6523-11ea-838d-a250a9ec145b.png)
