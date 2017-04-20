import fasttext
import json
import numpy as np
	
path = "/Users/eugene/Git/fastText/models/wiki.da.bin"

if not 'model' in vars():
	model = fasttext.load_model(path)

labeled = open('36hist.json', 'r').read()
labeled = json.loads(labeled)

def clean(string):
	v = "eleven har viden om af alle alt andre at blev bliver bort da dag de dem den der deres det dig dog du efter eller en end er et far fik fin for forbi fordi frafri få gik glad godt ham han hanshar havde have hele hen hende her hjemhun hvad hver hvis hvor igen ikke indjeg jer jo kan kom kommer kun kunnelang lidt lige lille løb man mange medmeget men mere mig min mod mon måned nej noget nok nu når og ogsåom op os over på sagde se selvsidste sig sin sine skal skulle små somstor store så tid til tog ud undervar ved vi vil ville være været år"
	stoplist = set(v.split())
	return ' '.join([word for word in string.lower().split() if word not in stoplist]).replace(',', '')


texts = []
i = 0
for key in labeled:
	i+=1
	text          = labeled[key]["text"]
	ffm_skill     = labeled[key]["færdighed"]
	ffm_knowledge = labeled[key]["viden"]
	texts.append(text)
	# ffm           = clean(f"{ffm_skill} {ffm_knowledge}")
	# dstruct[text] = ffm
	# dstruct.setdefault(text,[]).append(ffm)
	# print(text, "\n", ffm_skill, "\n", ffm_knowledge)

vecs = []
for text in texts:
	vecs = list(map(lambda word: model[word], clean(text).split()))
	vecs.append(np.sum(vecs, axis=0))
