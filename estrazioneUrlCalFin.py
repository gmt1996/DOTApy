#estrae tutti gli url per tutte le date dell'anno da dicembre 2019 a novembre 2020 compresi
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

parser = argparse.ArgumentParser()
parser.add_argument("city", type=str, help="seleziona la città per la quale estrarre i dati")
parser.add_argument("data inizio", type=str, help="seleziona il mese di inizio")
parser.add_argument("numero di mesi", type=int, help="seleziona per quanti mesi effettuare l'estrazione")

args = parser.parse_args()
config = configparser.ConfigParser()
config.read('config.ini')

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#windows
driver = webdriver.Chrome( options = options)
#linux inserire path chromedriver
#driver = webdriver.Chrome(executable_path='/mnt/c/Windows/chromedriver.exe', options = options)

driver.get('https://www.booking.com/index.it.html?aid=376372;label=it-5Srxg0e1twJI_ryrey2UnQS267778030990%3Apl%3Ata%3Ap1%3Ap22.537.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1008645%3Ali%3Adec%3Adm;sid=d609fa4cf73aa79faad84de2c1edf6e7;keep_landing=1;redirected=1;source=country&gclid=Cj0KCQjwrrXtBRCKARIsAMbU6bGPNWfeLivjgzvrBEe5kwcWMZSwg2cl7-5iz3j_1hebY6CifnAXBQkaAnecEALw_wcB&')

def data(inpu,inpu1):
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
    global mesi
    global meseRiferimento
    global splitt
    global calendario
    global annorife
    global ann
    for i in range(calendario[0],calendario[1]+calendario[0]):
            passo3 = driver.find_element_by_class_name('xp__dates-inner')
            driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
            passo3.click()
            mon = calendar.month_name[splitt]
            month = funmonth(mon)
            print(month)

            while( driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div').text != month+' '+str(ann)):
                avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')
                avanti.click()
            #passo3.click()
            driver.implicitly_wait(5)
            disab = driver.find_elements_by_class_name('bui-calendar__date.bui-calendar__date--disabled')


            avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]')


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
                format = funData(date)
                b = (format,)
                c = inpu
                try:
                    connection = mysql.connector.connect(host = config['mysqlDB']['host'],
                           user = config['mysqlDB']['user'],
                           passwd = config['mysqlDB']['pass'],
                           db = config['mysqlDB']['db'])
                    time.sleep(3)

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

                time.sleep(3)

                #torna alla pagina prima
                driver.back()
                time.sleep(1)
                #driver.refresh()
                driver.implicitly_wait(5)
                passo3 = driver.find_element_by_class_name('xp__dates-inner')
                passo3.click()
                while( driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div').text != month+' '+str(ann)):
                    avanti = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]').click()

                driver.implicitly_wait(5)
            if(int(driver.find_elements_by_class_name('bui-calendar__date')[i].text) == calendario[1]):
                print('fine mese')
                passo3.click()
                print(splitt)
                if (splitt == 12):
                    splitt = 1
                    ann = ann + 1
                else:
                    splitt = splitt + 1
                mon = calendar.month_name[splitt]
                calendario = calendar.monthrange(ann,splitt)
                return
            passo3.click()

def funmonth(mese):
    if(mese =='January'):
        nume = 'gennaio'
    elif(mese == 'February'):
        nume = 'febbraio'
    elif(mese == 'March'):
        nume = 'marzo'
    elif(mese == 'April'):
        nume = 'aprile'
    elif(mese == 'May'):
        nume = 'maggio'
    elif(mese == 'June'):
        nume = 'giugno'
    elif(mese == 'July'):
        nume = 'luglio'
    elif(mese == 'August'):
        nume = 'agosto'
    elif(mese == 'September'):
        nume = 'settembre'
    elif(mese == 'October'):
        nume = 'ottobre'
    elif(mese == 'November'):
        nume = 'novembre'
    elif(mese == 'December'):
        nume = 'dicembre'
    return (nume)
def funAnno(anno):
    b = anno.split()
    return (int(b[1]))
def funMesi(month):
    b = month.split()
    mese = b [0]
    nume  = ''
    if(mese =='gennaio'):
        nume = 1
    elif(mese == 'febbraio'):
        nume = 2
    elif(mese == 'marzo'):
        nume = 3
    elif(mese == 'aprile'):
        nume = 4
    elif(mese == 'maggio'):
        nume = 5
    elif(mese == 'giugno'):
        nume = 6
    elif(mese == 'luglio'):
        nume = 7
    elif(mese == 'agosto'):
        nume = 8
    elif(mese == 'settembre'):
        nume = 9
    elif(mese == 'ottobre'):
        nume = 10
    elif(mese == 'novembre'):
        nume = 11
    elif(mese == 'dicembre'):
        nume = 12
    return (nume)
calendario = calendar.monthrange(funAnno(sys.argv[2]),funMesi(sys.argv[2]))
print(calendario)
annorife = 2020
meseRiferimento = sys.argv[2]
splitt = int(funMesi(meseRiferimento))
splittato = meseRiferimento.split()
ann = int(splittato[1])
def funData(a):
    b = a.split()
    mese = b[2]
    nume=''
    if(mese =='gennaio'):
        nume = '01'
    elif(mese == 'febbraio'):
        nume = '02'
    elif(mese == 'marzo'):
        nume = '03'
    elif(mese == 'aprile'):
        nume = '04'
    elif(mese == 'maggio'):
        nume = '05'
    elif(mese == 'giugno'):
        nume = '06'
    elif(mese == 'luglio'):
        nume = '07'
    elif(mese == 'agosto'):
        nume = '08'
    elif(mese == 'settembre'):
        nume = '09'
    elif(mese == 'ottobre'):
        nume = '10'
    elif(mese == 'novembre'):
        nume = '11'
    elif(mese == 'dicembre'):
        nume = '12'
    giorno = b[1]
    if(giorno=='1'):
        giorno = '01'
    elif(giorno=='2'):
        giorno ='02'
    elif(giorno=='3'):
        giorno ='03'
    elif(giorno=='4'):
        giorno ='04'
    elif(giorno=='5'):
        giorno ='05'
    elif(giorno=='6'):
        giorno ='06'
    elif(giorno=='7'):
        giorno ='07'
    elif(giorno=='8'):
        giorno ='08'
    elif(giorno=='9'):
        giorno ='09'
    c = ['','','']
    c[0] = b[3]
    c[1]= nume
    c[2]= giorno
    d = '-'.join(c)
    return (d)
loop = int(sys.argv[3])
for iter in range(0,loop):
    data(sys.argv[1],sys.argv[2])
