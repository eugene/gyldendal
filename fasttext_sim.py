# General script notes:
#  * Running in ipython without reloading model every time: run -i fasttext_sim.py
#
# General Python notes
# 
#  * Convert an iterator (like the one returned by map) to 
#    an array: list(map(lambda n: n, [1,2,3])) or [*map(lambda n: n, [1,2,3])]

import fasttext
import json
import pandas
import numpy as np
import scipy
import string # for punctuation

from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine as cosine_distance
import matplotlib.pyplot as plt
	
if not 'model' in vars():
	path = "/Users/eugene/Git/fastText/models/wiki.da.bin"
	model = fasttext.load_model(path)

labeled = open('34hist.json', 'r').read()
labeled = json.loads(labeled)

def read_ffms():
	with open('FFM.json') as data_file:    
		faerdiheder = json.load(data_file)["Historie"]["3. - 4. klasse"]["færdighed"]
		return faerdiheder 

def clean(string):
	v = """eleven har viden om af alle alt andre at blev bliver bort da dag de 
	       dem den der deres det dig dog du efter eller en end er et far fik fin 
	       for forbi fordi frafri få gik glad godt ham han hanshar havde have hele hen 
	       hende her hjemhun hvad hver hvis hvor igen ikke indjeg jer jo kan kom kommer 
	       kun kunnelang lidt lige lille løb man mange medmeget men mere mig min mod mon 
	       måned nej noget nok nu når og ogsåom op os over på sagde se selvsidste sig sin 
	       sine skal skulle små somstor store så tid til tog ud undervar ved 
	       vi vil ville være været år"""
	       
	stoplist = set(v.split())
	return ' '.join([word for word in string.lower().split() if word not in stoplist]).replace(',', '')

def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')
    s = s.replace(' ', '')

    return s.lower().strip()

texts = {}
for key in labeled:
	text          = labeled[key]["text"]
	ffm_skill     = labeled[key]["færdighed"]
	ffm_knowledge = labeled[key]["viden"]
	text_vectors  = list(map(lambda word: model[word], clean(text).split()))
	texts[text]   = {
		"text"      : text,
		"skill"     : ffm_skill,
		"knowledge" : ffm_knowledge,
		"vector"    : np.sum(text_vectors, axis=0)
	}

ffms = {}
for ffm in read_ffms():
	text_vectors = list(map(lambda word: model[word], clean(ffm).split()))
	ffms[ffm] = {
		"text"   : ffm,
		"vector" : np.sum(text_vectors, axis=0)	
	}

for text, text_value in texts.items():
	text_value["distance"] = {}

	for ffm_text, ffm_value in ffms.items():
		distance = cosine_distance(text_value["vector"], ffm_value["vector"])
		text_value["distance"][str(distance)] = { 
			"ffm": ffm_text,
			"match": (normalize(text_value["skill"]) == normalize(ffm_text))
		}
		
# calculating accuracy
def accuracy_plot():
	accuracy = []
	for i in range(len(ffms)):
		a = 0
		for text_key, text_value in texts.items():
			m = [v["match"] for v in text_value["distance"].values()]
			a += np.sum(m[0:(i+1)])
		accuracy.append(a / len(texts))
	
	plt.plot(range(len(ffms)), accuracy)
	plt.grid()
	plt.xlabel(("In top n"))
	plt.ylabel(("Accuracy"))
	plt.show(block=False)
	input("Hit Enter To Close")
	plt.close()
