#estrae nome hotel e prezzo di tutte le pagine per un giorno
##funziona in modalita headless con firefox eventualmente per server
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import warnings
from selenium.webdriver.firefox.options import Options


options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path='/Users/matteogiannettoni/Desktop/scraper/geckodriver', options=options, )


#pisa
driver.get('https://www.booking.com/searchresults.it.html?aid=397594&label=gog235jc-1FCAEoggI46AdIM1gDaHGIAQGYARS4AQfIAQzYAQHoAQH4AQyIAgGoAgO4AsCrnu0FwAIB&sid=1a7eec527f46b9d43c5486f437bdc452&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.it.html%3Faid%3D397594%3Blabel%3Dgog235jc-1FCAEoggI46AdIM1gDaHGIAQGYARS4AQfIAQzYAQHoAQH4AQyIAgGoAgO4AsCrnu0FwAIB%3Bsid%3D1a7eec527f46b9d43c5486f437bdc452%3Bsb_price_type%3Dtotal%26%3B&ss=Pisa%2C+Toscana%2C+Italia&is_ski_area=0&checkin_monthday=9&checkin_month=12&checkin_year=2019&checkout_monthday=10&checkout_month=12&checkout_year=2019&group_adults=1&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=pisa&ac_position=0&ac_langcode=it&ac_click_type=b&dest_id=-124918&dest_type=city&iata=PSA&place_id_lat=43.716358&place_id_lon=10.402089&search_pageview_id=9be35f3b10af012e&search_selected=true')


#trova hotel e prezzi
def trovaHtPr():
    ht = driver.find_element_by_xpath('//*[@id="hotellist_inner"]')
    numHt = driver.find_elements_by_class_name('sr_item')
    print(len(numHt))
    for i in range(0, len(numHt)):
        s = numHt[i].find_element_by_class_name('sr-hotel__name').text
        if(numHt[i].find_elements_by_class_name("fe_banner__title")):
            p ="€ 0"
        else:
            try:
                if(numHt[i].find_element_by_class_name('tpi_price_label.tpi_price_label__orange')):
                    p = numHt[i].find_element_by_class_name('tpi_price_label.tpi_price_label__orange').text
            except WDE:
                p = numHt[i].find_element_by_class_name('bui-price-display__value').text
        print(s +" : "+ p)
    #hts = ht.find_elements_by_class_name('sr-hotel__name')
    #print(hts[0].text)


# a = driver.current_url
def pagSuccessiva():
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
    time.sleep(1)

seleziona5km()
time.sleep(2)
#for i in range(0,7):
try:
    while(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')):
        try:
            #a = driver.current_url
            trovaHtPr()
            #if(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a').get_attribute('title')!="pagina successiva"):
            #    print("basta")
            #    break
            driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a').click()
            time.sleep(6)
        except WDE:
            print("stop")
except WDE:
    trovaHtPr()
        #for i in range(0,len(passo1)):
        #    if(passo1[i].get_attribute('class')==h[0].get_attribute('class')):
        #        print('no'+passo1[i].text)
        #    else:
        #        print('s'+passo1[i].text)
