#estrae info hotel

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import mysql.connector
from mysql.connector import Error
import re
driver = webdriver.Chrome('/Users/matteogiannettoni/Desktop/scraper/chromedriver')

a = driver.get('https://www.booking.com/searchresults.it.html?aid=376372&label=it-3aOU9G8CnPp3k4iv4SLQrwS267778030993%3Apl%3Ata%3Ap1%3Ap22.538.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-298012084940%3Alp1008645%3Ali%3Adec%3Adm&sid=d609fa4cf73aa79faad84de2c1edf6e7&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.it.html%3Faid%3D376372%3Blabel%3Dit-3aOU9G8CnPp3k4iv4SLQrwS267778030993%253Apl%253Ata%253Ap1%253Ap22.538.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-298012084940%253Alp1008645%253Ali%253Adec%253Adm%3Bsid%3Dd609fa4cf73aa79faad84de2c1edf6e7%3Bsb_price_type%3Dtotal%26%3B&ss=Pisa&is_ski_area=0&ssne=Pisa&ssne_untouched=Pisa&dest_id=-124918&dest_type=city&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1')
a
NomeHote = 'a'
main_page = driver.current_window_handle
connection = mysql.connector.connect(host='localhost',
                                    database='ota',
                                    user='root',
                                    password='rootroot')
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

        #print(numHt[i].find_element_by_class_name('sr-hotel__name').text)
        estrazioneInfoHotel()
        time.sleep(1)
    time.sleep(3)
    #non funziona
    #indirizzo = driver.find_element_by_xpath('//*[@id="showMap2"]/span')
    #print(indirizzo)



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
    #main_page = driver.current_window_handle
    for i in driver.window_handles:
        driver.switch_to.window(i)
        time.sleep(2)
        #prende nome hotel
    try:
        nomeHt = driver.find_element_by_class_name('hp__hotel-name')
        #nomeHt = driver.find_element_by_xpath('//*[@id="hp_hotel_name"]')
        #nomeHt = driver.find_element_by_class_name('fn')
        #print(nomeHt.text)
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

    #reperisce tutte le cose che piacciono di più ai vistatori
    try:
        pazziper = driver.find_elements_by_class_name('important_facility')
        pazzi = ' '
        for i in range(0,len(pazziper)//2):
            pazzi = pazzi + pazziper[i].text + ', '
            #print(pazziper[i].text)
    except WDE:
        print("err pazzi per")

    #estrae tutte le recensioni caricate sulla pagina
    try:
        recensioni = driver.find_elements_by_class_name('c-review__body')
        recen = ''
        for i in range(0,len(recensioni)):
            recen = recen + recensioni[i].text + '; '
            #print(recensioni[i].text)
    except WDE:
        print("err recensioni")

    #estare i buoni motivi per scegliere la struttura
    try:
        motivi3 = driver.find_elements_by_class_name('oneusp')
        mot = ''
        for i in range(0,len(motivi3)):
            mot = mot + motivi3[i].text + '; '
    except WDE:
        print("err recensioni")
    try:
        l=re.findall(r'(h.*)\?', driver.current_url)
        x= l[0]
        hturl = (x,)
    except WDE:
        print("err recensioni")
    try:

        mySql_insert_query = """INSERT INTO accomodation (NomeHotel, indirizzo, pazziPer, recensioni, motivi, url)
               VALUES
               (%s, %s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        global NomeHote
        result = cursor.execute(mySql_insert_query, (NomeHote[0], indiri[0], pazzi, recen, mot, hturl[0]))
        connection.commit()
        print("Record inserted successfully into accomodation table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into accomodation table {}".format(error))
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
                    mySql_insert_query = """INSERT INTO servizi (value)
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
                    cursor.execute("SELECT idservizi from servizi WHERE value = %s" , e)
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
