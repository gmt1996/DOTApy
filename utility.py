def traduciMesi(mese):
    a =  {'January':'gennaio','February':'febbraio','March':'marzo','April':'aprile','May':'maggio','June':'giugno','July':'luglio','August':'agosto','September':'settembre','October':'ottobre','November':'novembre','December':'dicembre'}
    return (a[mese])
def normalizzaAnno(anno):
    b = anno.split()
    return (int(b[1]))
def normalizzaMesi(month):
    b = month.split()
    mese = b [0]
    a =  {'gennaio':1,'febbraio':2,'marzo':3,'aprile':4,'maggio':5,'giugno':6,'luglio':7,'agosto':8,'settembre':9,'ottobre':10,'novembre':11,'dicembre':12}
    return (a[mese])
def normalizzaData(a):
    b = a.split()
    mese = b[2]
    giorno = b[1]
    numeroMese =  {'gennaio':'01','febbraio':'02','marzo':'03','aprile':'04','maggio':'05','giugno':'06','luglio':'07','agosto':'08','settembre':'09','ottobre':'10','novembre':'11','dicembre':'12'}
    numeroGiorno =  {'1':'01','2':'02','3':'03','4':'04','5':'05','6':'06','7':'07','8':'08','9':'09'}
    c = ['','','']
    c[0] = b[3]
    c[1]= numeroMese[mese]
    c[2]= numeroGiorno[giorno]
    d = '-'.join(c)
    return (d)
