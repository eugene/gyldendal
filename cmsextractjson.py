import json
import glob
import io

path = glob.glob('data/historie/34/*.json')
mapping = {}
count = 0
for p in path:
	try:
		with open(p) as json_data:
		    data = json.load(json_data)

		l1 = data['objectives']['objectives'][0]['idPairs']

		v = data['objectives']['formalObjectives'][0]['idPair']

		lin = []
		textin = []

		lid = []
		FM = []
		VM = []

		for x in data['objectives']['objectives']:
			lin.append(x['idPairs'])
			textin.append(x['text'])


		for x in data['objectives']['formalObjectives']:
			lid.append(x['idPair'])
			FM.append(x['faerdighedsMaal'])
			VM.append(x['vidensMaal'])


		for i, text in enumerate(textin):
			print(text)
			for j, FO in enumerate(lid):
				try:
					if FO == lin[i][0]:
						print(FM[j])
						print(VM[j])
						print(' ')
						mapping[count] = {'text': text, 'viden':VM[j], 'færdighed': FM[j]}
						count += 1
				except:
					pass
	except:
		pass

#Save File
with io.open('34hist.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(mapping,
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(str(str_))




