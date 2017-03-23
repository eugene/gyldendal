import pandas 
import json
import io

path = 'data/all_ffms.json'
data = pandas.read_json(path)

dataD = dict()

for i, fag in enumerate(list(data['navn'])):
	testdict = {}

	#For hvert klassetrin
	for klasse in data.get('forloeb')[i]:
		kompetence = []
		faardighed = []
		viden = []
		D = klasse['kompetenceomraade']
		for maal in D:
			for maalpar in maal.get('maalPar'):
				for maalFaser in maalpar.get('maalFaser'):
					faardighed.append(maalFaser.get('faerdighedsMaal').get('navn'))
					viden.append(maalFaser.get('vidensMaal').get('navn'))

			kompmaal = maal.get('kompetenceMaal')
			kompetence.append(kompmaal)
		testdict[klasse['navn']] =  {'kompetence':kompetence, 'færdighed':faardighed, 'viden':viden}
	dataD[fag] = testdict

testi = json.dumps(dataD)


#Save File
with io.open('FFM.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(dataD,
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(str(str_))

#Load File
with open('FFM.json') as data_file:
    FFM = json.load(data_file)

# For at få FFM for Matematik, 1-3 klasse, færdighed:  FFM['Matematik']['1. - 3. klasse ']['færdighed']
# Tjek indeholdt data med FFM.keys() // FFM['Dansk'].keys() osv