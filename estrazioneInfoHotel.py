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
#options.add_argument('headless')
#windows
driver = webdriver.Chrome( options = options)
#linux inserire path chromedriver
#driver = webdriver.Chrome(executable_path='/mnt/c/Windows/chromedriver.exe', options = options)
parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str,required= True, help="seleziona la città per la quale estrarre i dati es: pisa")

args = parser.parse_args()
config = configparser.ConfigParser()
configurazione = config.read('config.ini')
hostDB = config['mysqlDB']['host']
userDB = config['mysqlDB']['user']
passwdDB = config['mysqlDB']['pass']
dbDB = config['mysqlDB']['db']
if not configurazione:
    exit('file config.ini non trovato')
if not hostDB or not userDB or not passwdDB or not dbDB:
    exit('parametri file config.ini non definiti')


driver.get('https://www.booking.com/')
NomeHote = 'a'
main_page = driver.current_window_handle
connection = mysql.connector.connect(host = hostDB,
       user = userDB,
       passwd = passwdDB,
       db = dbDB)
time.sleep(3)
def entraHotel():
    #main_page = driver.current_window_handle
    numHt = driver.find_elements_by_class_name('sr_item')
    #se indentato apre tutte le pagine degli hotel
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
        print("Not able to find element")
    try:
        coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        coo1.click()
    except WDE:
        print("Not able to find element")
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
        print("no nome")

    #prende tutti indirizzo
    indirizz = driver.find_element_by_class_name('hp_address_subtitle').text
    indiri = (indirizz, )
    try:
        indirizzo = driver.find_element_by_class_name('hp_address_subtitle')
        #print(indirizzo.text)
    except WDE:
        print("non ci sono")


    try:
        l=re.findall(r'(h.*)\?', driver.current_url)
        x= l[0]
        hturl = (x,)
    except WDE:
        print("err recensioni")
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
        print("Record inserted successfully into accomodation table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into accomodation table {}".format(error))

    #reperisce tutte le cose che piacciono di più ai vistatori
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
                print("Record inserted successfully into accomodationpazziper table")
                cursor.close()

            except mysql.connector.Error as error:
                print("Failed to insert record into accomodationpazziper table {}".format(error))
            pazzi = pazzi + pazziper[i].text + ', '
    except WDE:
        print("err pazzi per")

    #estrae tutte le categorie e per ognuna le sue info
    try:
        checklistSection = driver.find_elements_by_class_name('facilitiesChecklistSection')
        print(len(checklistSection))
        ele = ''

        for i in range(0,len(checklistSection)):
            h5 = checklistSection[i].find_element_by_tag_name('h5')
            print(h5.text)

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
                    print("Record inserted successfully into servizi table")
                    cursor.close()
                except mysql.connector.Error as error:
                    print("Failed to insert record into servizi table {}".format(error))
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
                    print("Record inserted successfully into accomodationservice table")
                    cursor.close()


                except mysql.connector.Error as error:
                    print("Failed to insert record into accomodationservice table {}".format(error))
                ele = ele + elementi +'; '
                print(elementi)

            print("fine info hotel")
    except WDE:
        print("err recensioni")

    driver.close()
    driver.switch_to.window(main_page)

def pagSuccessiva(a):
    ##accetta i cookie se presenti
    try:
        coo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
        coo.click()
    except WDE:
        print("Not able to find element")
    try:
        coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
        coo1.click()
    except WDE:
        print("Not able to find element")

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
            print("impossibile estrarre informazioni dagli hotel")
except WDE:
    entraHotel()
    pagSuccessiva(a)
    print("finito estrarre informazioni hotel")
if(connection.is_connected()):
    cursor.close()
    connection.close()
