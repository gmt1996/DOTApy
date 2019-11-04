#estrae info hotel

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE

driver = webdriver.Chrome('/Users/matteogiannettoni/Desktop/scraper/chromedriver')

a = driver.get('https://www.booking.com/searchresults.it.html?aid=397594&label=gog235jc-1FCAEoggI46AdIM1gDaHGIAQGYARS4AQfIAQzYAQHoAQH4AQyIAgGoAgO4AsCrnu0FwAIB&sid=1a7eec527f46b9d43c5486f437bdc452&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.it.html%3Faid%3D397594%3Blabel%3Dgog235jc-1FCAEoggI46AdIM1gDaHGIAQGYARS4AQfIAQzYAQHoAQH4AQyIAgGoAgO4AsCrnu0FwAIB%3Bsid%3D1a7eec527f46b9d43c5486f437bdc452%3Bsb_price_type%3Dtotal%26%3B&ss=Pisa%2C+Toscana%2C+Italia&is_ski_area=0&checkin_monthday=9&checkin_month=12&checkin_year=2019&checkout_monthday=10&checkout_month=12&checkout_year=2019&group_adults=1&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=pisa&ac_position=0&ac_langcode=it&ac_click_type=b&dest_id=-124918&dest_type=city&iata=PSA&place_id_lat=43.716358&place_id_lon=10.402089&search_pageview_id=9be35f3b10af012e&search_selected=true')
a
main_page = driver.current_window_handle
def entraHotel():
    #main_page = driver.current_window_handle
    numHt = driver.find_elements_by_class_name('sr_item')
    #se indentato apre tutte le pagine degli hotel
    for i in range(0,len(numHt)):
        s = numHt[i].find_element_by_class_name('sr-hotel__name')
        s.click()
        print(numHt[i].find_element_by_class_name('sr-hotel__name').text)
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
    try:
        indirizzo = driver.find_element_by_class_name('hp_address_subtitle')
        print(indirizzo.text)
    except WDE:
        print("non ci sono")

    #reperisce tutte le cose che piacciono di più ai vistatori
    try:
        pazziper = driver.find_elements_by_class_name('important_facility')
        for i in range(0,len(pazziper)//2):
            print(pazziper[i].text)
    except WDE:
        print("err pazzi per")

    #estrae tutte le recensioni caricate sulla pagina
    try:
        recensioni = driver.find_elements_by_class_name('c-review__body')
        for i in range(0,len(recensioni)):
            print(recensioni[i].text)
    except WDE:
        print("err recensioni")

    #estare i buoni motivi per scegliere la struttura
    try:
        motivi3 = driver.find_elements_by_class_name('oneusp')
        for i in range(0,len(motivi3)):
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
            for j in range(0,1):
                elementi = checklistSection[i].find_element_by_tag_name('ul').text
                print(elementi)
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
