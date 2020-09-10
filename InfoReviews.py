
"""Copyright 2020 Matteo Giannettoni

This file is part of Nome-Programma.

Nome-Programma is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nome-Programma is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nome-Programma.  If not, see <http://www.gnu.org/licenses/>."""


import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
from selenium.common.exceptions import NoSuchElementException as NSE
import mysql.connector
from mysql.connector import Error
import re
import argparse

options = webdriver.ChromeOptions()
options.add_argument('--lang=it-IT')
#options.add_experimental_option("prefs", {"intl.accept_languages": "it-IT"})
#options.add_argument('headless')
options.add_argument('--log-level=3')

driver = webdriver.Chrome( options = options)

#driver = webdriver.Chrome(executable_path='/Users/rizla/Documents/chromedriver_win32/chromedriver.exe', options = options)
parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str,required= True, help="Inserire la città per la quale estrarre i dati. Es: pisa")
parser.add_argument('--verbose', '-v', action='count', default=0 , help="Argomento utilizzato per determinare la quantità delle stampe in output, inserendo una o due v come parametro. Es: -v per primo livello che porterà in stampa errori e messaggi importanti , -vv per il secondo livello che porterà in stampa errori e messaggi importanti più altri messaggi di debug, di default saranno riportati in output i soli messaggi di errore")
parser.add_argument('-nr', type= int, default=1000, help='Inserire il numero di pagine per hotel di recensioni da estrarre, se non specificato estrarrà tutte le recensioni')
parser.add_argument('-ph', type=int, help='Inserire il numero di pagine di hotel da estrarre, se non specificato verranno estratte informazioni da tutte le pagini presenti')
args = parser.parse_args()

if args.ph:
	pagineHotelSelezionate = args.ph
#definizione di verbose
verbose = 0
if args.verbose:
	verbose = args.verbose
#funzione per la stampa dei messaggi
def debug(stringa, livello):
	if livello <= verbose:
		print(stringa)
config = configparser.ConfigParser()
#verifica dei parametri del file config.ini
configurazione = config.read('config.ini')
if not configurazione:
    exit('file config.ini non trovato')
else:
    hostDB = config['mysqlDB']['host']
    userDB = config['mysqlDB']['user']
    passwdDB = config['mysqlDB']['pass']
    dbDB = config['mysqlDB']['db']
if not hostDB or not userDB  or not dbDB:
    exit('parametri file config.ini non definiti')

#Il driver apre la pagina web all'indirizzo specificato
driver.get('https://www.booking.com/')

NomeHote = 'a'
main_page = driver.current_window_handle
#connessione al DB
connection = mysql.connector.connect(host = hostDB,
       user = userDB,
       passwd = passwdDB,
       db = dbDB)

#funzione per l'estrazione delle recensioni che si basa sull'argomento -nr per estrarne il numero selezionato
def recen():
    time.sleep(3)
    allRec = driver.find_element_by_xpath('//*[@id="show_reviews_tab"]')
    allRec.click()
    cust = driver.find_element_by_xpath('//*[@id="review_sort"]')
    cust.click()
    recenti = driver.find_element_by_xpath('//*[@id="review_sort"]/option[2]')
    recenti.click()
    time.sleep(2)
    next = driver.find_element_by_xpath('//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a')
    numeroRecensioni = args.nr
    while(numeroRecensioni>0):
        time.sleep(1)
        listaRec = driver.find_element_by_class_name('review_list')
        numRec = listaRec.find_elements_by_class_name('review_list_new_item_block')
        debug(len(numRec),2)
		#estrazione del nome, nazione e testo delle recensioni scritte dagli utenti
        for i in range(0,len(numRec)):
            name = numRec[i].find_element_by_class_name('bui-avatar-block__title').text
            title = numRec[i].find_element_by_class_name('c-review-block__title').text
            nation = ''
            try:
                nation = numRec[i].find_element_by_class_name('bui-avatar-block__subtitle').text
            except WDE:
                debug('nazione non presente',0)
            recens = numRec[i].find_element_by_class_name('c-review')
            pos = recens.find_elements_by_class_name('c-review__row')
            score = numRec[i].find_element_by_class_name('bui-review-score__badge').text
            dataRec = numRec[i].find_element_by_class_name('c-review-block__date').text
            Lang = numRec[i].find_element_by_class_name('c-review__body')
            try:
                LinguaRec = Lang.get_attribute('lang')
            except WDE:
                debug('Non è presente la lingua della recensione',0)
            normalizzatore = 'Recensione: '
            if normalizzatore in dataRec:
                temp = dataRec.split(normalizzatore)
                dataRec = ''.join(temp)
                dataRecensioneNormalizzata = normalizzaData(dataRec)
            debug("dataRecensioneNormalizzata",2)
            rp = ''
            rn = ''
			#estrazione e normalizzazione delle recensioni positive rp e negative rn
            try:
                if(len(pos)>1):
                    rp = pos[0].find_element_by_class_name('c-review__body').text
                    rn = pos[1].find_element_by_class_name('c-review__body').text
                    trad = 'Mostra traduzione'
                    comm = 'Il cliente non ha lasciato un commento'
                    piac = 'Cosa è piaciuto · '
                    piacn = 'Cosa non è piaciuto · '
                    if trad in rp:
                        c = trad.split('Mostra traduzione')
                        rp = ''.join(c)
                    if comm in rp:
                        c = comm.split('Il cliente non ha lasciato un commento')
                        rn = ''.join(c)
                    if piac in rp:
                        c = piac.split('Cosa è piaciuto · ')
                        rp = ''.join(c)
                    if piacn in rn:
                        c = piacn.split('Cosa non è piaciuto · ')
                        rn = ''.join(c)
                    debug(pos[1].text,2)
                else:
                    rp = pos[0].find_element_by_class_name('c-review__body').text
                    comm = 'Il cliente non ha lasciato un commento'
                    piac = 'Cosa è piaciuto · '
                    if comm in rp:
                        c = comm.split('Il cliente non ha lasciato un commento')
                        rp = ''.join(c)
                    if piac in rp:
                        c = piac.split('Cosa è piaciuto ·')
                        rp = ''.join(c)
                    debug(pos[0].text,2)
            except WDE:
                debug("recensione non valida per l'estrazione", 2)

            time.sleep(2)
            try:
                prin('ciao')
                cursor = connection.cursor()
                cursor.execute("SELECT max(IDHotel) from accomodation")
                risultato = cursor.fetchone()
                cursor.close()
                mySql_insert_query = """INSERT INTO accomodationrecensioni (idhotel, nome, titolo, recensionePos, recensioneNeg, score, nazione, dataRecensione, LinguaRecensione)
                                    VALUES
                              (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
                cursor = connection.cursor()
                result = cursor.execute(mySql_insert_query, (risultato[0],name,title,rp,rn,score,nation, dataRecensioneNormalizzata, LinguaRec))
                connection.commit()
                debug("Record inserted successfully into accomodationrecensioni table",1)
                cursor.close()

            except mysql.connector.Error as error:
                debug("Failed to insert record into accomodationrecensioni table {}".format(error),1)
        numeroRecensioni = numeroRecensioni - 1
        try:
            next = driver.find_element_by_xpath('//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a')
            next.click()
            time.sleep(2)
        except:
            break
    debug('fine recensioni',1)

#funzione per aprire le pagine dei singoli hotel da dove verranno poi estratte le informazioni
def entraHotel():
    numHt = driver.find_elements_by_class_name('sr_item')
    for i in range(0,len(numHt)):
        s = numHt[i].find_element_by_class_name('sr-hotel__name')
        pi = numHt[i].find_element_by_class_name('sr-hotel__name').text
        print('ht')
        global NomeHote
        NomeHote = (pi,)
        s.click()
        estrazioneInfoHotel()
        time.sleep(1)
    time.sleep(3)

#funzione che seleziona 5km come distanza dal centro
def seleziona5km():
    accettaCookie()
    #imposta la distanza a un km
    #km1 = driver.find_element_by_xpath('//*[@id="filter_distance"]/div[2]/a[1]/label/div')
    km = driver.find_element_by_xpath('//*[@id="filter_distance"]/div[2]/a[3]/label/div')
    print('km')
    time.sleep(2)
    try:
        mainCoo = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        mainCoo.click()
    except  WDE:
        debug("NO main Cookies",2)
    km.click()
    time.sleep(2)

#funzione per l'estrazione delle informazioni dagli hotel
def estrazioneInfoHotel():
    for i in driver.window_handles:
        driver.switch_to.window(i)
        time.sleep(2)
        #estrazione nome hotel
    try:
        nomeHt = driver.find_element_by_class_name('hp__hotel-name')
    except WDE:
        debug("errore estrazione nome hotel", 0)
    #estrazionetipologia
    try:
        #tipologia = driver.find_element_by_class_name('hp__hotel-type-badge').text
        tipologia  =driver.find_element_by_xpath('//*[@id="hp_hotel_name"]/span').text
        typ = (tipologia,)
    except WDE:
        typ = ['']
        debug("errore estrazione tipologia", 2)
    #estrazione stelle
    try:
        stelle = driver.find_element_by_xpath('//*[@id="wrap-hotelpage-top"]/div[1]/span/span[1]/span/span/span').get_attribute('aria-label')
        #stelle = driver.find_element_by_class_name('hp__hotel_ratings').text
        #stelle = driver.find_element_by_xpath('//*[@id="wrap-hotelpage-top"]/div[1]/span/span[1]/i/span').text
        ns = re.findall(r'\d', stelle)
        NumeroStelle = ns[0]
    except :
        NumeroStelle = ['']
        debug("nessuna stella", 2)
    #estrazione indirizzo
    indirizz = driver.find_element_by_class_name('hp_address_subtitle').text
    indiri = (indirizz, )
    try:
        indirizzo = driver.find_element_by_class_name('hp_address_subtitle')
    except WDE:
        debug("errore estrazione indirizzo", 0)
    try:
        l=re.findall(r'(h.*)\?', driver.current_url)
        x= l[0]
        hturl = (x,)
    except :
        hturl=[driver.current_url]
        debug("errore estrazione url", 0)
    print('in')
    #estrazione della latitudine e della longitudine dal file javaScript
    javaScript = "return(booking.env.b_map_center_latitude)"
    js = driver.execute_script(javaScript)
    javaScript1 = "return(booking.env.b_map_center_longitude)"
    js1 = driver.execute_script(javaScript1)
    global NomeHote
    cursor = connection.cursor()
    cursor.execute("select NomeHotel, indirizzo from accomodation")
    hotelEstratti = cursor.fetchall()
    if ((NomeHote[0], indiri[0]) not in hotelEstratti):
        try:
            mySql_insert_query = """INSERT INTO accomodation (NomeHotel, indirizzo, url, latitudine, longitudine,tipologia,stelle)
	               VALUES
	               (%s, %s, %s, %s, %s, %s, %s) """
            cursor = connection.cursor()
            result = cursor.execute(mySql_insert_query, (NomeHote[0], indiri[0], hturl[0], js, js1, typ[0], NumeroStelle[0]))
            connection.commit()
            debug("Record inserted successfully into accomodation table",1)
            cursor.close()
        except mysql.connector.Error as error:
            debug("Failed to insert record into accomodation table {}".format(error),1)
        #estrazione di tutti i servizi preferiti dai vistatori
        try:
            pazziper = driver.find_elements_by_class_name('important_facility')
            pazzi = ''
            for i in range(0,len(pazziper)//2):
                gsd = pazziper[i].text
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT max(IDHotel) from accomodation")
                risultato = cursor.fetchone()
                cursor.close()
                mySql_insert_query = """INSERT INTO accomodationpazziper (idhotel, pazziper)
	                       VALUES
	                       (%s, %s) """
                cursor = connection.cursor()
                result = cursor.execute(mySql_insert_query, (risultato[0],gsd))
                connection.commit()
                debug("Record inserted successfully into accomodationpazziper table",2)
                cursor.close()

            except mysql.connector.Error as error:
                debug("Failed to insert record into accomodationpazziper table {}".format(error),1)
                pazzi = pazzi + pazziper[i].text + ', '
        except WDE:
            debug("errore estrazione sezione pazzi per", 0)

        #estrazione dei buoni motivi per scegliere la struttura
        try:
            motivi3 = driver.find_elements_by_class_name('oneusp')
            mot = ''
            for i in range(0,len(motivi3)):
                fd = motivi3[i].text
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT max(IDHotel) from accomodation")
                    risultato = cursor.fetchone()
                    cursor.close()

                    mySql_insert_query = """INSERT INTO accomodationmotivi (idhotel, motivo)
                            VALUES
	                       (%s, %s) """
                    cursor = connection.cursor()
                    result = cursor.execute(mySql_insert_query, (risultato[0],fd))
                    connection.commit()
                    debug("Record inserted successfully into accomodationmotivi table",1)
                    cursor.close()

                except mysql.connector.Error as error:
                    debug("Failed to insert record into accomodationmotivi table {}".format(error),1)
                mot = mot + motivi3[i].text + '; '
        except WDE:
            debug("errore estrazione sezione pazzi per", 0)

        #estrazione di tutte le categorie e per ognuna di esse le sue info
        try:
            checklistSection = driver.find_elements_by_class_name('facilitiesChecklistSection')
            ele = ''

            for i in range(0,len(checklistSection)):
                h5 = checklistSection[i].find_element_by_tag_name('h5')
                debug(h5.text,2)

                for j in range(0,len(checklistSection[i].find_elements_by_tag_name('li'))):
                    elementi = checklistSection[i].find_elements_by_tag_name('li')[j].text
                    e = (elementi, )
                    try:
                        mySql_insert_query = """INSERT INTO servizi (servizio)
	                           VALUES
	                           (%s) """

                        cursor = connection.cursor()
                        result = cursor.execute(mySql_insert_query, e)
                        connection.commit()
                        debug("Record inserted successfully into servizi table",1)
                        cursor.close()
                    except mysql.connector.Error as error:
                        debug("Failed to insert record into servizi table {}".format(error),1)
                    try:
                        cursor = connection.cursor()
                        cursor.execute("SELECT max(IDHotel) from accomodation")
                        risultato = cursor.fetchone()
                        cursor.close()
                        cursor = connection.cursor()
                        cursor.execute("SELECT id from servizi WHERE servizio = %s" , e)
                        risultato1 = cursor.fetchone()
                        cursor.close()
                        mySql_insert_query = """INSERT INTO accomodationservice (IDHotel, IDServizi)
	                           VALUES
	                           (%s, %s) """
                        cursor = connection.cursor()
                        result = cursor.execute(mySql_insert_query, (risultato[0], risultato1[0]))
                        connection.commit()
                        debug("Record inserted successfully into accomodationservice table",1)
                        cursor.close()


                    except mysql.connector.Error as error:
                        debug("Failed to insert record into accomodationservice table {}".format(error),1)
                    ele = ele + elementi +'; '
                    debug(elementi,2)
                debug("Fine estrazione informazioni, inizio estrazione recensioni",1)
        except WDE:
            debug("err recensioni",0)
        try:
            if args.nr > 0:
                recen()
        except WDE:
            debug("errore recensioni",0)
    else:
        debug("Info hotel già estratte, inizio estrazione prossimo hotel", 1)
    driver.close()
    driver.switch_to.window(main_page)

#funzione che normalizza la data che ne permette l'inserimento nel DB
def normalizzaData(x):
    dataSeparata = x.split()
    giorno = dataSeparata[0]
    mese = dataSeparata[1]
    anno = dataSeparata[2]
    numeroMese =  {'gennaio':'01','febbraio':'02','marzo':'03','aprile':'04','maggio':'05','giugno':'06','luglio':'07','agosto':'08','settembre':'09','ottobre':'10','novembre':'11','dicembre':'12'}
    if len(giorno)==1:
        giorno = '0'+giorno
    ArrayAppoggio = ['','','']
    ArrayAppoggio[0] = anno
    ArrayAppoggio[1]= numeroMese[mese]
    ArrayAppoggio[2]= giorno
    data = '-'.join(ArrayAppoggio)
    return (data)

#funzione che se presenti accetta i coockie
def accettaCookie ():
    try:
        mainCoo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        mainCoo.click()
    except  WDE:
        debug("NO main Cookies",2)
    try:
        coo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
        coo.click()
    except WDE:
        debug("Not able to find element",2)
    try:
        coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        coo1.click()
    except WDE:
        debug("Not able to find element",2)
def pagSuccessiva():
    accettaCookie()
    #selettore freccia avanti pag
    pag = driver.find_element_by_css_selector('#search_results_table > div.bui-pagination.results-paging > nav > ul > li.bui-pagination__item.bui-pagination__next-arrow > a')
    time.sleep(3)
    pag.click()
    main_page = driver.current_window_handle

def main():
    try:
        mainCoo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        mainCoo.click()
    except  WDE:
        debug("NO main Cookies",2)
    passo0 = driver.find_element_by_class_name('c-autocomplete__input')
    passo0.send_keys(args.c)
    passo0.send_keys(Keys.ENTER)
    time.sleep(3)
    try:
        mainCoo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        mainCoo.click()
    except  WDE:
        debug("NO main Cookies",2)
    seleziona5km()
    try:
        while(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')):
            try:
                entraHotel()
                pagSuccessiva()
                global pagineHotelSelezionate
                if args.ph:
                    pagineHotelSelezionate = pagineHotelSelezionate - 1
                    if pagineHotelSelezionate == 0:
                        exit("fine estrazione per "+ str(args.ph) + " pagine di hotel")
                time.sleep(6)
            except WDE:
                debug("errore estrazione delle informazioni, info non estratte", 0)
    except NSE:
        entraHotel()
        exit("fine estrazione info hotel e recensioni")
    except WDE:
        debug("fine estrazione info hotel e recensioni", 0)
    if(connection.is_connected()):
        cursor.close()
        connection.close()
main()
