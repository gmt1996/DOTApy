#estrae tutti gli url per tutte le date dell'anno da dicembre 2019 a novembre 2020 compresi

import mysql.connector
from mysql.connector import Error

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


driver = webdriver.Chrome('/Users/matteogiannettoni/Desktop/scraper/chromedriver')

driver.get('https://www.booking.com/index.it.html?aid=376372;label=it-5Srxg0e1twJI_ryrey2UnQS267778030990%3Apl%3Ata%3Ap1%3Ap22.537.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1008645%3Ali%3Adec%3Adm;sid=d609fa4cf73aa79faad84de2c1edf6e7;keep_landing=1;redirected=1;source=country&gclid=Cj0KCQjwrrXtBRCKARIsAMbU6bGPNWfeLivjgzvrBEe5kwcWMZSwg2cl7-5iz3j_1hebY6CifnAXBQkaAnecEALw_wcB&')

z = 1
mesi = ["dicembre 2019", "gennaio 2020", "febbraio 2020", "marzo 2020", "aprile 2020", "maggio 2020", "giugno 2020", "luglio 2020", "agosto 2020", "settembre 2020", "ottobre 2020", "novembre 2020"]
cont = 0
def data(inpu):
    #driver.refresh()
    #leva i coockie
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

    avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')

    mese = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div')


    for i in range(0,38):
            passo3 = driver.find_element_by_class_name('xp__dates-inner')
            driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
            passo3.click()
            global cont
            global mesi
            while( driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div').text != mesi[cont]):
                avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
                avanti.click()
            #passo3.click()
            driver.implicitly_wait(5)
            disab = driver.find_elements_by_class_name('bui-calendar__date.bui-calendar__date--disabled')


            avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
            #passo3 = driver.find_element_by_class_name('xp__dates-inner')
            #passo3.click()
            global z
            if(z==38):
                cont = cont + 1
                z = 0
                passo3.click()
                return
            if(cont == 5 and z == 35):
                cont = cont + 1
                z = 0
                passo3.click()
                return
            if(cont == 6 and z == 30):
                cont = cont + 1
                z = 0
                passo3.click()
                return



            #passo3.click()


            z = z + 1
            vuoti = driver.find_elements_by_class_name('bui-calendar__date.bui-calendar__date--empty')

            numGiorni = driver.find_elements_by_class_name('bui-calendar__date')
            if(numGiorni[i].get_attribute('class') != vuoti[0].get_attribute('class')):
                print("si" )
                #print(i)
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
                a = (driver.current_url,)
                date = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div/div[1]/div[1]/div/div/div[1]/div/div[2]').text
                b = (date,)
                c = inpu
                try:
                    connection = mysql.connector.connect(host='localhost',
                                                        database='ota',
                                                        user='root',
                                                        password='rootroot')
                    time.sleep(3)
                    #a = (driver.current_url)

                    mySql_insert_query = """INSERT INTO urlHotel (url, data, citta)
                           VALUES
                           (%s, %s, %s) """

                    cursor = connection.cursor()
                    result = cursor.execute(mySql_insert_query, (a[0], b[0], c))
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
                time.sleep(3)

                #torna alla pagina prima
                #driver.history.go(-1)
                driver.back()
                time.sleep(1)
                #driver.refresh()
                driver.implicitly_wait(5)
                passo3 = driver.find_element_by_class_name('xp__dates-inner')
                #ck = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div[2]')
                #avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
                passo3.click()
                while( driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div').text != mesi[cont]):
                    #avanti.click()
                    avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]').click()
                #avanti.click()
                #avanti.click()

                driver.implicitly_wait(5)
            passo3.click()




for i in range(0,11):
    data(sys.argv[1])
