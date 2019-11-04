#estrae info hotel

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import mysql.connector
from mysql.connector import Error

driver = webdriver.Chrome('/Users/matteogiannettoni/Desktop/scraper/chromedriver')

a = driver.get('https://www.booking.com/searchresults.it.html?aid=376372&label=it-5Srxg0e1twJI_ryrey2UnQS267778030990%3Apl%3Ata%3Ap1%3Ap22.537.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1008645%3Ali%3Adec%3Adm&sid=b04ba1a9b8c54b39542699416c8b40b5&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_year_month_monthday=2019-12-01&checkout_year_month_monthday=2019-12-02&class_interval=1&dest_id=-124918&dest_type=city&from_sf=1&group_adults=1&group_children=0&iata=PSA&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&src=index&srpvid=76536e1242fa01da&ss=Pisa%2C%20Toscana%2C%20Italia&ss_raw=pisa&ssb=empty&top_ufis=1&rdf=')
a
NomeHote = 'a'
main_page = driver.current_window_handle
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
        print(nomeHt.text)
    except WDE:
        print("no nome")

    #prende tutti indirizzo
    indirizz = driver.find_element_by_class_name('hp_address_subtitle').text
    indiri = (indirizz, )
    try:
        indirizzo = driver.find_element_by_class_name('hp_address_subtitle')
        print(indirizzo.text)
    except WDE:
        print("non ci sono")

    #reperisce tutte le cose che piacciono di più ai vistatori
    try:
        pazziper = driver.find_elements_by_class_name('important_facility')
        pazzi = ' '
        for i in range(0,len(pazziper)//2):
            pazzi = pazzi + pazziper[i].text + ', '
            print(pazziper[i].text)
    except WDE:
        print("err pazzi per")

    #estrae tutte le recensioni caricate sulla pagina
    try:
        recensioni = driver.find_elements_by_class_name('c-review__body')
        recen = ''
        for i in range(0,len(recensioni)):
            recen = recen + recensioni[i].text + '; '
            print(recensioni[i].text)
    except WDE:
        print("err recensioni")

    #estare i buoni motivi per scegliere la struttura
    try:
        motivi3 = driver.find_elements_by_class_name('oneusp')
        mot = ''
        for i in range(0,len(motivi3)):
            mot = mot + motivi3[i].text + '; '
            print(motivi3[i].text)
    except WDE:
        print("err recensioni")

    #estrae tutte le categorie e per ognuna le sue info
    try:
        #checklist = driver.find_element_by_class_name('facilitiesChecklist')
        checklistSection = driver.find_elements_by_class_name('facilitiesChecklistSection')
        print(len(checklistSection))
        for i in range(0,len(checklistSection)):
            h5 = checklistSection[i].find_element_by_tag_name('h5')
            #tit = checklistSection[i].find_element_by_class_name('faciliesGroupIcon').text
            print(h5.text)
            ele = ''
            for j in range(0,1):
                elementi = checklistSection[i].find_element_by_tag_name('ul').text
                ele = ele + elementi +'; '
                print(elementi)
    except WDE:
        print("err recensioni")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='prova',
                                            user='root',
                                            password='rootroot')
        time.sleep(3)
        #a = (driver.current_url)

        mySql_insert_query = """INSERT INTO accomodation (NomeHotel, indirizzo, pazziPer, recensioni, motivi, servizi)
               VALUES
               (%s, %s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        global NomeHote
        result = cursor.execute(mySql_insert_query, (NomeHote[0], indiri[0], pazzi, recen, mot, ele))
        connection.commit()
        print("Record inserted successfully into urlht table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into urlht table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

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
    #print(pag)
    time.sleep(3)
    pag.click()
    main_page = driver.current_window_handle

seleziona5km()
#for i in range(0,2):
try:
    while(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')):
        try:
            #a = driver.current_url

            #trovaHtPr()
            entraHotel()
            pagSuccessiva(a)
            time.sleep(6)
        except WDE:
            print("stop")
except WDE:
    entraHotel()
    pagSuccessiva(a)
    print("finito estrarre info hotel")



#estrazioneInfoHotel()
