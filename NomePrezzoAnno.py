#estrae nome hotel e prezzo di tutte le pagine per un anno
##funziona in modalita headless con firefox eventualmente per server
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import warnings
from selenium.webdriver.firefox.options import Options
import mysql.connector
from mysql.connector import Error
from selenium.webdriver.common.proxy import Proxy, ProxyType

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "ip_addr:port"
prox.socks_proxy = "ip_addr:port"
prox.ssl_proxy = "ip_addr:port"


options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path = '/Users/matteogiannettoni/Desktop/scraper/geckodriver', options=options, )






mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "rootroot",
    database = "booking"
   )
mycursor = mydb.cursor()
mycursor.execute("SELECT url FROM urlhotel")
myresult = mycursor.fetchall()
mycursor.close()
mydb.close()
beta = 1
try:
 for i in myresult:
    print(beta)
    driver.get(i[0])
    #trova hotel e prezzi
    def trovaHtPr():
        ht = driver.find_element_by_xpath('//*[@id="hotellist_inner"]')
        numHt = ht.find_elements_by_class_name('sr_item')
        print(len(numHt))
        for i in range(0, len(numHt)):
            o = numHt[i].find_element_by_class_name('sr-hotel__name').text
            s = (o,)
            if(numHt[i].find_elements_by_class_name("fe_banner__title")):
                t ="€ 0"
                p = (t,)

            else:
                try:
                    if(numHt[i].find_element_by_class_name('tpi_price_label.tpi_price_label__orange')):
                        t= numHt[i].find_element_by_class_name('tpi_price_label.tpi_price_label__orange').text
                        p = (t,)
                except WDE:
                    t = numHt[i].find_element_by_class_name('bui-price-display__value').text
                    p = (t,)

                try:
                    mydb = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            passwd = "rootroot",
                            database = "booking"
                           )
                    mySql_insert_query = """INSERT INTO nomeprezzohotel (NomeHotel,PrezzoHotel)
                           VALUES
                           (%s,%s) """

                    cursor = mydb.cursor()
                    result = cursor.execute(mySql_insert_query, (s[0],p[0]))
                    mydb.commit()
                    cursor.close()

                except mysql.connector.Error as error:
                    print("Failed to insert record into urlht table {}".format(error))

                finally:
                    if (mydb.is_connected()):
                        cursor.close()
                        mydb.close()
                        #print("MySQL connection is closed")
            #inserire(s, p)
            #inserire(p)
            #print(s +" : "+ p)
        #hts = ht.find_elements_by_class_name('sr-hotel__name')
        #print(hts[0].text)


    # a = driver.current_url


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
        try:
            km = driver.find_element_by_xpath('//*[@id="filter_distance"]/div[2]/a[3]/label/div')
            time.sleep(2)
            km.click()
            time.sleep(1)
        except WDE:
             print("no 5km")
    time.sleep(2)
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
                try:
                    coo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
                    coo.click()
                except WDE:
                    print("Not able to find coockie while")
                try:
                    coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
                    coo1.click()
                except WDE:
                    print("Not able to find coockie while")
                driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a').click()
                time.sleep(4)
            except WDE:
                print("stop")

    except WDE:
       trovaHtPr()
            #for i in range(0,len(passo1)):
            #    if(passo1[i].get_attribute('class')==h[0].get_attribute('class')):
            #        print('no'+passo1[i].text)
            #    else:
            #        print('s'+passo1[i].text)
    beta = beta + 1
except WDE:
    print("probabile errore di rete per il giorno ")
