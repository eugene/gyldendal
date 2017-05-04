import fasttext
import json
import pandas
import numpy as np
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
	
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
	v = "eleven har viden om af alle alt andre at blev bliver bort da dag de dem den der deres det dig dog du efter eller en end er et far fik fin for forbi fordi frafri få gik glad godt ham han hanshar havde have hele hen hende her hjemhun hvad hver hvis hvor igen ikke indjeg jer jo kan kom kommer kun kunnelang lidt lige lille løb man mange medmeget men mere mig min mod mon måned nej noget nok nu når og ogsåom op os over på sagde se selvsidste sig sin sine skal skulle små somstor store så tid til tog ud undervar ved vi vil ville være været år"
	stoplist = set(v.split())
	return ' '.join([word for word in string.lower().split() if word not in stoplist]).replace(',', '')

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
