#estrae info hotel

import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import mysql.connector
from mysql.connector import Error
import re
import sys
import argparse
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--lang=it')
#windows
driver = webdriver.Chrome( options = options)
#linux inserire path chromedriver
#driver = webdriver.Chrome(executable_path='/mnt/c/Windows/chromedriver.exe', options = options)
parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str,required= True, help="seleziona la città per la quale estrarre i dati es: pisa")
parser.add_argument('--verbose', '-v', action='count', default=0, , help="si utilizza per determinare il livello delle stampe in output aggiungendo uno o due v come parametro. -v primo livello che stampa errori e milestones, -vv stampa i precedenti più altri messaggi di debug, di default stampa solo errori")
args = parser.parse_args()

verbose = 0
if args.verbose:
	verbose = args.verbose
def debug(stringa, livello):
	if livello <= verbose:
		print(stringa)
config = configparser.ConfigParser()
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

#apre la pagina web all'indirizzo specificato
driver.get('https://www.booking.com/')
NomeHote = 'a'
main_page = driver.current_window_handle
connection = mysql.connector.connect(host = hostDB,
       user = userDB,
       passwd = passwdDB,
       db = dbDB)
#aggiunte delle attese con time.sleep per permettere al programma e al motore di ricerca di eseguire i calcoli in maniera corretta
time.sleep(3)
#funzione che estrae le tutte le recensioni presenti ordinate dalle più recenti
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
    while(next):
        time.sleep(1)
        listaRec = driver.find_element_by_class_name('review_list')
        numRec = listaRec.find_elements_by_class_name('review_list_new_item_block')
        debug(len(numRec),2)
        #if args.verbose:
        #    print(len(numRec))

        for i in range(0,len(numRec)):
            name = numRec[i].find_element_by_class_name('bui-avatar-block__title').text
            title = numRec[i].find_element_by_class_name('c-review-block__title').text
            nation = ''
            try:
                nation = numRec[i].find_element_by_class_name('bui-avatar-block__subtitle').text
            except WDE:
                print('no nation')
            recens = numRec[i].find_element_by_class_name('c-review')
            pos = recens.find_elements_by_class_name('c-review__row')
            score = numRec[i].find_element_by_class_name('bui-review-score__badge').text
            dataRec = numRec[i].find_element_by_class_name('c-review-block__date').text
            Lang = numRec[i].find_element_by_class_name('c-review__body')
            try:
                LinguaRec = Lang.get_attribute('lang')
            except WDE:
                print('Non è presente la lingua della recensione')
            normalizzatore = 'Recensione: '
            if normalizzatore in dataRec:
                temp = dataRec.split(normalizzatore)
                dataRec = ''.join(temp)
                dataRecensioneNormalizzata = normalizzaData(dataRec)
            debug(dataRecensioneNormalizzata,2)
            #if args.verbose:
            #    print(dataRecensioneNormalizzata)
            rp = ''
            rn = ''

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
                    #if args.verbose:
                    #    print(pos[0].text)
                    #    print(pos[1].text)
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
                    #if args.verbose:
                    #    print(pos[0].text)
            except WDE:
                debug("recensione non valida per l'estrazione", 2)
                #print('no rec')

            time.sleep(2)
            try:
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
                #print("Record inserted successfully into accomodationrecensioni table")
                cursor.close()

            except mysql.connector.Error as error:
                debug("Failed to insert record into accomodationrecensioni table {}".format(error),1)
                 #print("Failed to insert record into accomodationrecensioni table {}".format(error))

        try:
            next = driver.find_element_by_xpath('//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a')
            next.click()
            time.sleep(2)
        except:
            break
    debug('fine recensioni',1)
    #print('fine recensioni')
#funzione che apre la pagina di ogni singolo hotel dove verranno poi estratte le informazioni
def entraHotel():
    numHt = driver.find_elements_by_class_name('sr_item')
    for i in range(0,len(numHt)):
        s = numHt[i].find_element_by_class_name('sr-hotel__name')

        pi = numHt[i].find_element_by_class_name('sr-hotel__name').text
        global NomeHote
        NomeHote = (pi,)
        s.click()
        estrazioneInfoHotel()
        time.sleep(1)
    time.sleep(3)
#funzione che seleziona 5km come distanza dal centro
def seleziona5km():
    try:
        coo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
        coo.click()
    except WDE:
        debug("Not able to find element",2)
        #print("Not able to find element")
    try:
        coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        coo1.click()
    except WDE:
        debug("Not able to find element",2)
        #print("Not able to find element")
    #imposta la distanza a un km
    #km1 = driver.find_element_by_xpath('//*[@id="filter_distance"]/div[2]/a[1]/label/div')
    km = driver.find_element_by_xpath('//*[@id="filter_distance"]/div[2]/a[3]/label/div')
    time.sleep(2)
    km.click()
    time.sleep(2)
#funzione che estrae informazioni dagli hotel
def estrazioneInfoHotel():
    for i in driver.window_handles:
        driver.switch_to.window(i)
        time.sleep(2)
        #prende nome hotel
    try:
        nomeHt = driver.find_element_by_class_name('hp__hotel-name')
    except WDE:
        debug("errore estrazione nome hotel", 0)
        #print("no nome")

    #prende indirizzo
    indirizz = driver.find_element_by_class_name('hp_address_subtitle').text
    indiri = (indirizz, )
    try:
        indirizzo = driver.find_element_by_class_name('hp_address_subtitle')
    except WDE:
        debug("errore estrazione indirizzo", 0)
        #print("non ci sono indirizzi presnti")
    try:
        l=re.findall(r'(h.*)\?', driver.current_url)
        x= l[0]
        hturl = (x,)
    except WDE:
        debug("errore estrazione url", 0)
        #print("errore estrazione url")
    #estrae latitudine e longitudine dal file javaScript
    javaScript = "return(booking.env.b_map_center_latitude)"
    js = driver.execute_script(javaScript)
    javaScript1 = "return(booking.env.b_map_center_longitude)"
    js1 = driver.execute_script(javaScript1)
    try:

        mySql_insert_query = """INSERT INTO accomodation (NomeHotel, indirizzo, url, latitudine, longitudine)
               VALUES
               (%s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        global NomeHote
        result = cursor.execute(mySql_insert_query, (NomeHote[0], indiri[0], hturl[0], js, js1))
        connection.commit()
        debug("Record inserted successfully into accomodation table",1)
        #print("Record inserted successfully into accomodation table")
        cursor.close()

    except mysql.connector.Error as error:
        debug("Failed to insert record into accomodation table {}".format(error),1)
        #print("Failed to insert record into accomodation table {}".format(error))

    #estrae tutte le cose che piacciono di più ai vistatori
    try:
        pazziper = driver.find_elements_by_class_name('important_facility')
        pazzi = ' '
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
                #print("Record inserted successfully into accomodationpazziper table")
                cursor.close()

            except mysql.connector.Error as error:
                debug("Failed to insert record into accomodationpazziper table {}".format(error),1)
                #print("Failed to insert record into accomodationpazziper table {}".format(error))
            pazzi = pazzi + pazziper[i].text + ', '
    except WDE:
        debug("errore estrazione sezione pazzi per", 0)
        #print("err pazzi per")

    #estrae i buoni motivi per scegliere la struttura
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
                #print("Record inserted successfully into accomodationmotivi table")
                cursor.close()


            except mysql.connector.Error as error:
                debug("Failed to insert record into accomodationmotivi table {}".format(error),1)
                #print("Failed to insert record into accomodationmotivi table {}".format(error))
            mot = mot + motivi3[i].text + '; '
    except WDE:
        debug("errore estrazione sezione pazzi per", 0)

    #estrae tutte le categorie e per ognuna le sue info
    try:
        checklistSection = driver.find_elements_by_class_name('facilitiesChecklistSection')
        ele = ''

        for i in range(0,len(checklistSection)):
            h5 = checklistSection[i].find_element_by_tag_name('h5')
            debug(h5.text,2)
            #if args.verbose:
            #    print(h5.text)

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
                    #print("Record inserted successfully into servizi table")
                    cursor.close()
                except mysql.connector.Error as error:
                    debug("Failed to insert record into servizi table {}".format(error),1)
                    #print("Failed to insert record into servizi table {}".format(error))
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
                    #print("Record inserted successfully into accomodationservice table")
                    cursor.close()


                except mysql.connector.Error as error:
                    debug("Failed to insert record into accomodationservice table {}".format(error),1)
                    #print("Failed to insert record into accomodationservice table {}".format(error))
                ele = ele + elementi +'; '
                debug(elementi,2)
                #if args.verbose:
                #    print(elementi)
            debug("Fine estrazione informazioni, inizio estrazione recensioni",1)
            #print("Fine estrazione informazioni, inizio estrazione recensioni")
    except WDE:
        debug("err recensioni",0)
        #print("err recensioni")
    try:
        recen()
    except WDE:
        debug("errore recensioni",0)
        #print('errore recensioni')
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

def pagSuccessiva(a):
    ##accettare tasto cookie
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

    #selettore freccia avanti pag
    pag = driver.find_element_by_css_selector('#search_results_table > div.bui-pagination.results-paging > nav > ul > li.bui-pagination__item.bui-pagination__next-arrow > a')
    time.sleep(3)
    pag.click()
    main_page = driver.current_window_handle
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
passo0 = driver.find_element_by_class_name('c-autocomplete__input')
passo0.send_keys(args.c)
passo0.send_keys(Keys.ENTER)
time.sleep(3)
seleziona5km()
try:
    while(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')):
        try:
            entraHotel()
            pagSuccessiva(a)
            time.sleep(6)
        except WDE:
            debug("errore estrazione delle informazioni, info non estratte", 0)
            #print("stop")
except WDE:
    entraHotel()
    pagSuccessiva(a)
    debug("finito estrazione info hotel e recensioni", 0)
    #print("finito estrarre info hotel e recensioni")
if(connection.is_connected()):
    cursor.close()
    connection.close()
