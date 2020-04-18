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
#windows
options.add_argument('--lang=it')
driver = webdriver.Chrome( options = options)
#linux inserire path chromedriver
#driver = webdriver.Chrome(executable_path='/mnt/c/Windows/chromedriver.exe', options = options)
parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str, required= True, help="seleziona la città per la quale estrarre i dati es: pisa")
parser.add_argument('--verbose', '-v', action='count', default=0, help="si utilizza per determinare il livello delle stampe in output aggiungendo uno o due v come parametro. -v primo livello che stampa errori e milestones, -vv stampa i precedenti più altri messaggi di debug, di default stampa solo errori")
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
if not hostDB or not userDB or not dbDB:
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

def estrazioneInfoHotel():
    for i in driver.window_handles:
        driver.switch_to.window(i)
        time.sleep(2)
        #prende nome hotel
    try:
        nomeHt = driver.find_element_by_class_name('hp__hotel-name')
    except WDE:
        debug("errore estrazione nome hotel", 0)

    #estrae indirizzo
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
    except WDE:
        debug("errore estrazione url", 0)
    #estrae latitudine e longitudine dal file javaScript
    javaScriptLat = "return(booking.env.b_map_center_latitude)"
    lat = driver.execute_script(javaScriptLat)
    javaScriptLon = "return(booking.env.b_map_center_longitude)"
    lon = driver.execute_script(javaScriptLon)
    try:

        mySql_insert_query = """INSERT INTO accomodation (NomeHotel, indirizzo, url, latitudine, longitudine)
               VALUES
               (%s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        global NomeHote
        result = cursor.execute(mySql_insert_query, (NomeHote[0], indiri[0], hturl[0], lat, lon))
        connection.commit()
        debug("Record inserted successfully into accomodation table",1)
        cursor.close()

    except mysql.connector.Error as error:
        debug("Failed to insert record into accomodation table {}".format(error),1)

    #estrae tutte le cose che piacciono di più ai vistatori e le inserisce nel DB
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
                debug("Record inserted successfully into accomodationpazziper table",1)
                cursor.close()

            except mysql.connector.Error as error:
                debug("Failed to insert record into accomodationpazziper table {}".format(error),1)
            pazzi = pazzi + pazziper[i].text + ', '
    except WDE:
        debug("errore estrazione sezione pazzi per", 0)

    #estrae tutte le categorie e per ognuna le sue info
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

            debug("Fine estrazione informazioni hotel",1)
    except WDE:
        debug("errore estrazione informazioni",0)

    driver.close()
    driver.switch_to.window(main_page)

def pagSuccessiva(a):
    ##accetta i cookie se presenti
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
passo0 = driver.find_element_by_class_name('c-autocomplete__input')
passo0.send_keys(args.c)
cerca = driver.find_element_by_class_name('xp__button')
cerca.click()
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
except WDE:
    entraHotel()
    pagSuccessiva(a)
    debug("finito estrazione info hotel e recensioni", 0)
if(connection.is_connected()):
    cursor.close()
    connection.close()
