#estrae nome hotel e prezzo di tutte le pagine per un anno

import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import warnings
from selenium.webdriver.firefox.options import Options
import mysql.connector
from mysql.connector import Error
from selenium.webdriver.common.proxy import Proxy, ProxyType
import datetime
import re

config = configparser.ConfigParser()
config.read('config.ini')

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "ip_addr:port"
prox.socks_proxy = "ip_addr:port"
prox.ssl_proxy = "ip_addr:port"

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options = options)
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(executable_path = '/Users/matteogiannettoni/Desktop/scraper/geckodriver', options=options, )

giorno = (datetime.date.today(), )




mydb = mysql.connector.connect(
    host = config['mysqlDB']['host'],
           user = config['mysqlDB']['user'],
           passwd = config['mysqlDB']['pass'],
           db = config['mysqlDB']['db']
   )
mycursor = mydb.cursor()
mycursor.execute("SELECT url, data, citta FROM urlhotel")
myresult = mycursor.fetchall()
mycursor.close()
#mydb.close()
beta = 1
try:
 for i in myresult:
    print(beta)
    driver.get(i[0])
    d = (i[1],)
    kk = (i[2],)
    try:
        #trova hotel e prezzi
        def trovaHtPr():
            ht = driver.find_element_by_xpath('//*[@id="hotellist_inner"]')
            numHt = ht.find_elements_by_class_name('sr_item')
            print(len(numHt))
            time.sleep(3)
            for i in range(0, len(numHt)):
                o = numHt[i].find_element_by_class_name('sr-hotel__name').text
                s = (o,)

                if(numHt[i].find_elements_by_class_name("fe_banner__title")):
                    t =0
                    p = (t,)

                else:
                    try:
                        if(numHt[i].find_element_by_class_name('tpi_price_label.tpi_price_label__orange')):
                            t= numHt[i].find_element_by_class_name('tpi_price_label.tpi_price_label__orange').text
                            num = re.findall(r'(\d+)', t)
                            p = (num[0],)
                    except WDE:
                        t = numHt[i].find_element_by_class_name('bui-price-display__value').text
                        num = re.findall(r'(\d+)', t)
                        p = (num[0],)
                    try:
                        global giorno
                        mySql_insert_query = """INSERT INTO accomodationprice (NomeHotel,PrezzoHotel, dataSoggiorno, dataRicerca, CittaHotel)
                               VALUES
                               (%s,%s,%s,%s,%s) """

                        cursor = mydb.cursor()
                        result = cursor.execute(mySql_insert_query, (s[0],p[0],d[0],giorno[0],kk[0]))
                        mydb.commit()
                        cursor.close()

                    except mysql.connector.Error as error:
                        print("Failed to insert record into urlht table {}".format(error))

                    finally:
                        if (mydb.is_connected()):
                            cursor.close()

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
        try:
            while(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')):
                try:
                    trovaHtPr()
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
        beta = beta + 1
    except WDE:
        print('data scaduta')
except WDE:
    print("probabile errore di rete")
mydb.close()
