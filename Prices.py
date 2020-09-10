
"""Copyright 2020 Matteo Giannettoni

This file is part of Nome-Programma.

Nome-Programma is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nome-Programma is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nome-Programma.  If not, see <http://www.gnu.org/licenses/>."""


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count', default=0 , help="Argomento utilizzato per determinare la quantità delle stampe in output, inserendo una o due v come parametro. Es: -v per primo livello che porterà in stampa errori e messaggi importanti , -vv per il secondo livello che porterà in stampa errori e messaggi importanti più altri messaggi di debug, di default saranno riportati in output i soli messaggi di errore")
args = parser.parse_args()

config = configparser.ConfigParser()
configurazione = config.read('config.ini')
if not configurazione:
    exit('file config.ini non trovato')
else:
    hostDB = config['mysqlDB']['host']
    userDB = config['mysqlDB']['user']
    passwdDB = config['mysqlDB']['pass']
    dbDB = config['mysqlDB']['db']
if not hostDB or not userDB or not passwdDB or not dbDB:
    exit('parametri file config.ini non definiti')

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "ip_addr:port"
prox.socks_proxy = "ip_addr:port"
prox.ssl_proxy = "ip_addr:port"

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options = options)

#definizione di verbose
verbose = 0
if args.verbose:
	verbose = args.verbose
#funzione per la stampa dei messaggi
def debug(stringa, livello):
	if livello <= verbose:
		print(stringa)

giorno = (datetime.date.today(), )

mydb = mysql.connector.connect(
           host = hostDB,
           user = userDB,
           passwd = passwdDB,
           db = dbDB
   )
mycursor = mydb.cursor()
mycursor.execute("SELECT url, data, citta FROM urlhotel")
myresult = mycursor.fetchall()
mycursor.close()
beta = 1
try:
 for i in myresult:
    try:
        mainCoo = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        mainCoo.click()
    except  WDE:
        debug("NO main Cookies",2)
    debug(beta,2)
    driver.get(i[0])
    d = (i[1],)
    kk = (i[2],)
    try:
        #estrazione nome hotel e prezzo
        def trovaHtPr():
            attesa = WebDriverWait(driver, 5)
            attesa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hotellist_inner"]')))
            ht = driver.find_element_by_xpath('//*[@id="hotellist_inner"]')
            numHt = ht.find_elements_by_class_name('sr_item')
            debug(len(numHt),2)
            #aggiunte delle attese con time.sleep per permettere al programma e al motore di ricerca di eseguire i calcoli in maniera corretta
            #time.sleep(6)
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
                        debug("Failed to insert record into urlht table {}".format(error),1)
                    finally:
                        if (mydb.is_connected()):
                            cursor.close()

        def seleziona5km():
            try:
                mainCoo = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
                mainCoo.click()
            except  WDE:
                debug("NO main Cookies",2)
            try:
                coo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
                coo.click()
            except WDE:
                debug("No coockie",2)
            try:
                coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
                coo1.click()
            except WDE:
                debug("No coockie",2)
            try:
                attesa = WebDriverWait(driver, 5)
                attesa.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filter_distance"]/div[2]/a[3]/label/div')))
                km = driver.find_element_by_xpath('//*[@id="filter_distance"]/div[2]/a[3]/label/div')
                #time.sleep(2)
                km.click()
                time.sleep(1)
            except WDE:
                 debug("no 5km",2)
        time.sleep(2)
        seleziona5km()
        time.sleep(2)
        try:
            while(driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')):
                try:
                    trovaHtPr()
                    try:
                        mainCoo = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
                        mainCoo.click()
                    except  WDE:
                        debug("NO main Cookies",2)
                    try:
                        coo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
                        coo.click()
                    except WDE:
                        debug("No coockie",2)
                    try:
                        coo1 = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
                        coo1.click()
                    except WDE:
                        debug("No coockie",2)
                    driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a').click()
                    time.sleep(4)
                except WDE:
                    debug("probabile errore di rete, riprovare",0)
        except WDE:
           trovaHtPr()
        beta = beta + 1
    except WDE:
        debug('data scaduta',0)
except WDE:
    debug("probabile errore di rete",0)
mydb.close()
