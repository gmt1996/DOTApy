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
parser.add_argument("city", type=str, help="seleziona la città per la quale estrarre i dati es: pisa")

args = parser.parse_args()
config = configparser.ConfigParser()
config.read('config.ini')

a = driver.get('https://www.booking.com/')
a
NomeHote = 'a'
main_page = driver.current_window_handle
connection = mysql.connector.connect(host = config['mysqlDB']['host'],
       user = config['mysqlDB']['user'],
       passwd = config['mysqlDB']['pass'],
       db = config['mysqlDB']['db'])
time.sleep(3)
def recen():
    time.sleep(2)
    allRec = driver.find_element_by_xpath('//*[@id="left"]/div[10]/div[14]/button')
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
        print(len(numRec))
        #driver.find_element_by_class_name('bicon-aclose').click()

        for i in range(0,len(numRec)):
            name = numRec[i].find_element_by_class_name('bui-avatar-block__title').text
            title = numRec[i].find_element_by_class_name('c-review-block__title').text
            nation = numRec[i].find_element_by_class_name('bui-avatar-block__subtitle').text
            recens = numRec[i].find_element_by_class_name('c-review')
            pos = recens.find_elements_by_class_name('c-review__row')
            score = numRec[i].find_element_by_class_name('bui-review-score__badge').text

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
                    print(pos[0].text)
                    print(pos[1].text)
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
                    print(pos[0].text)
            except WDE:
                print('no rec')
            time.sleep(2)
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT max(IDHotel) from accomodation")
                risultato = cursor.fetchone()
                cursor.close()
                mySql_insert_query = """INSERT INTO accomodationrecensioni (idhotel, nome, titolo, recensionePos, recensioneNeg, score, nazione)
                                    VALUES
                              (%s, %s, %s, %s, %s, %s, %s) """
                cursor = connection.cursor()
                result = cursor.execute(mySql_insert_query, (risultato[0],name,title,rp,rn,score,nation))
                connection.commit()
                print("Record inserted successfully into accomodationrecensioni table")
                cursor.close()

            except mysql.connector.Error as error:
                 print("Failed to insert record into accomodationrecensioni table {}".format(error))
        #driver.find_element_by_tag_name('body').send_keys(Keys.END)
        #time.sleep(2)
        try:
            next = driver.find_element_by_xpath('//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a')
            next.click()
            time.sleep(2)
        except:
            break
    print('fine recensioni')
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
        print("err ")
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

    #estare i buoni motivi per scegliere la struttura
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
                print("Record inserted successfully into accomodationmotivi table")
                cursor.close()


            except mysql.connector.Error as error:
                print("Failed to insert record into accomodationmotivi table {}".format(error))
            mot = mot + motivi3[i].text + '; '
    except WDE:
        print("err motivi")

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

            print("MySQL connection is closed")
    except WDE:
        print("err recensioni")
    try:
        recen()
    except WDE:
        print('errore recensioni')
    driver.close()
    driver.switch_to.window(main_page)

def pagSuccessiva(a):
    ##accettare tasto cookie
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
passo0.send_keys(sys.argv[1])
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
            print("stop")
except WDE:
    entraHotel()
    pagSuccessiva(a)
    print("finito estrarre info hotel")
if(connection.is_connected()):
    cursor.close()
    connection.close()
