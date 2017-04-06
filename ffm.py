import pandas
import json

path = 'data/all_ffms.json'
df = pandas.read_json(path)

dansk = df.get('forloeb')[14]

klass12 = dansk[0]
klass34 = dansk[1]
klass56 = dansk[2]
#klass79 = dansk[3]
#klass10 = dansk[4]

klass12komp = klass12.get('kompetenceomraade')
klass12komplist = []
klass12faardighed = []
klass12viden = []

for maal in klass12komp:
    faerdighedsMaal = maal.get('maalPar')[0].get('maalFaser')[0].get('faerdighedsMaal').get('navn')
    videnMaal = maal.get('maalPar')[0].get('maalFaser')[0].get('vidensMaal').get('navn')

    for maalpar in maal.get('maalPar'):
        for maalFaser in maalpar.get('maalFaser'):
            faerdighedsMaal = maalFaser.get('faerdighedsMaal').get('navn')
            videnMaal = maalFaser.get('vidensMaal').get('navn')
            klass12faardighed.append(faerdighedsMaal)
            klass12viden.append(videnMaal)



    kompmaal = maal.get('kompetenceMaal')
    klass12komplist.append(kompmaal)




print (klass12komplist)