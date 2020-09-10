
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


import configparser
import mysql.connector
from mysql.connector import Error
import calendar
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import argparse
from utility import *

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count', default=0 , help="Argomento utilizzato per determinare la quantità delle stampe in output, inserendo una o due v come parametro. Es: -v per primo livello che porterà in stampa errori e messaggi importanti , -vv per il secondo livello che porterà in stampa errori, messaggi importanti più altri messaggi di debug, di default saranno riportati in output i soli messaggi di errore")
parser.add_argument("-c", type=str, required= True, help="seleziona la città per la quale estrarre i dati es: pisa")
parser.add_argument("-d", type=str, required= True, help='seleziona il mese di inizio con il formato mese anno es: "maggio 2020"')
parser.add_argument("-m", type=int, required= True, help="seleziona per quanti mesi effettuare l'estrazione es: 6")

args = parser.parse_args()
config = configparser.ConfigParser()
configurazione = config.read('config.ini')
#controllo su esistenza del file config.ini e se i suoi parametri non sono vuoti
if not configurazione:
    exit('file config.ini non trovato')
else:
    hostDB = config['mysqlDB']['host']
    userDB = config['mysqlDB']['user']
    passwdDB = config['mysqlDB']['pass']
    dbDB = config['mysqlDB']['db']
if not hostDB or not userDB or not passwdDB or not dbDB:
    exit('parametri file config.ini non definiti')
#definizione di verbose
verbose = 0
if args.verbose:
	verbose = args.verbose
#funzione per la stampa dei messaggi
def debug(stringa, livello):
	if livello <= verbose:
		print(stringa)
try:
    connection = mysql.connector.connect(host = hostDB,
           user = userDB,
           passwd = passwdDB,
           db = dbDB)
    debug('stabilita connessione al DB',0)
except:
    exit('impossibile stabilire connessione al DB')
options = webdriver.ChromeOptions()
#options.add_argument('headless')
#windows
driver = webdriver.Chrome( options = options)

#driver = webdriver.Chrome(executable_path='/Users/rizla/Documents/chromedriver_win32/chromedriver.exe', options = options)

#apre la pagina web all'indirizzo specificato
driver.get('https://www.booking.com/')

def data(inpu,inpu1):
    #Accetta i coockie se presenti
    try:
        mainCoo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
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

    avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')

    mese = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div')
    global mesi
    global meseRiferimento
    global splitt
    global calendario
    global ann
    #ciclo su tutti i giorni disponibili per il mese considerato
    for i in range(calendario[0],calendario[1]+calendario[0]):
            try:
                mainCoo = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div/div/div[2]/button')
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
            passo3 = driver.find_element_by_class_name('xp__dates-inner')
            driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
            passo3.click()
            mon = calendar.month_name[splitt]
            month = traduciMesi(mon)
            #avanza nel calendario fino ad arrivare al mese obbiettivo
            while( driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div').text != month+' '+str(ann)):
                avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
                avanti.click()
            driver.implicitly_wait(5)
            disab = driver.find_elements_by_class_name('bui-calendar__date.bui-calendar__date--disabled')


            avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')


            vuoti = driver.find_elements_by_class_name('bui-calendar__date.bui-calendar__date--empty')

            numGiorni = driver.find_elements_by_class_name('bui-calendar__date')
            if(numGiorni[i].get_attribute('class') != vuoti[0].get_attribute('class')):
                passo0 = driver.find_element_by_class_name('c-autocomplete__input')
                passo0.send_keys(inpu)


                #diminuisce di uno gli adulti
                passo1 = driver.find_element_by_xpath('//*[@id="xp__guests__toggle"]/span[2]')
                passo2 = driver.find_element_by_xpath('//*[@id="xp__guests__inputs-container"]/div/div/div[1]/div/div[2]/button[1]/span')
                passo1.click()
                passo2.click()

                #apre quadrante date
                passo3 = driver.find_element_by_class_name('xp__dates-inner')
                passo3.click()

                #click sulle date non vuote
                driver.find_elements_by_class_name('bui-calendar__date')[i].click()
                driver.find_elements_by_class_name('bui-calendar__date')[i+1].click()

                #click sul tasto cerca
                cerca = driver.find_element_by_class_name('xp__button')
                cerca.click()
                urlCorrenteHotel = (driver.current_url,)
                date = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div/div[1]/div[1]/div/div/div/div[2]').text
                #date = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div/div[1]/div[1]/div/div/div[1]/div/div[2]').text
                format = normalizzaData(date)
                dataPernottamento = (format,)
                cittaEstrazione = inpu
                try:
                    time.sleep(1)

                    mySql_insert_query = """INSERT INTO urlHotel (url, data, citta)
                           VALUES
                           (%s, %s, %s) """

                    cursor = connection.cursor()
                    result = cursor.execute(mySql_insert_query, (urlCorrenteHotel[0], dataPernottamento[0], cittaEstrazione))
                    connection.commit()
                    debug("Record inserted successfully into urlht table",1)
                    cursor.close()

                except mysql.connector.Error as error:
                    debug("Failed to insert record into urlht table {}".format(error),1)
                time.sleep(3)

                #torna alla pagina precedente
                driver.back()
                time.sleep(1)
                driver.implicitly_wait(5)
                passo3 = driver.find_element_by_class_name('xp__dates-inner')
                passo3.click()
                #avanza fino ad arrivare al mese obbiettivo
                while( driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div').text != month+' '+str(ann)):
                    avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]').click()

                driver.implicitly_wait(5)
            if(int(driver.find_elements_by_class_name('bui-calendar__date')[i].text) == calendario[1]):
                debug('fine mese',2)
                passo3.click()
                debug(splitt,2)
                if (splitt == 12):
                    splitt = 1
                    ann = ann + 1
                else:
                    splitt = splitt + 1
                mon = calendar.month_name[splitt]
                calendario = calendar.monthrange(ann,splitt)
                return
            passo3.click()


calendario = calendar.monthrange(normalizzaAnno(args.d),normalizzaMesi(args.d))
debug(calendario,2)
meseRiferimento = args.d
splitt = int(normalizzaMesi(meseRiferimento))
splittato = meseRiferimento.split()
ann = int(splittato[1])

loop = int(args.m)
for iter in range(0,loop):
    data(args.c,args.d)
