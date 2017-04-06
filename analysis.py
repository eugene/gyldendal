import logging
import json


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora

with open('FFM.json') as data_file:
    FFM = json.load(data_file)

documents = FFM['Dansk']['5. - 6. klasse']['færdighed']
v = "eleven har viden om af alle alt andre at blev bliver bort da dag de dem den der deres det dig dog du efter eller en end er et far fik fin for forbi fordi frafri få gik glad godt ham han hanshar havde have hele hen hende her hjemhun hvad hver hvis hvor igen ikke indjeg jer jo kan kom kommer kun kunnelang lidt lige lille løb man mange medmeget men mere mig min mod mon måned nej noget nok nu når og ogsåom op os over på sagde se selvsidste sig sin sine skal skulle små somstor store så tid til tog ud undervar ved vi vil ville være været år"
stoplist = set(v.split())

texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

from pprint import pprint  # pretty-printer
pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/tmm.dict')  # store the dictionary, for future reference
print(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/tmm.mm', corpus) 


from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('/tmp/tmm.dict')
corpus = corpora.MmCorpus('/tmp/tmm.mm') # comes from the first tutorial, "From strings to vectors"

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=12)

doc = "Eleven kan anvende grafiske modeller"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it

index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

sims = index[vec_lsi] # perform a similarity query against the corpus
#print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
sims = sorted(enumerate(sims), key=lambda item: -item[1])
#pprint(sims) # print sorted (document number, similarity score) 2-tuples

while True:
	doc = input('Skriv læringsmål, skriv q for at afslutte: ')
	if doc == 'q':
		break
	vec_bow = dictionary.doc2bow(doc.lower().split())
	vec_lsi = lsi[vec_bow] # convert the query to LSI space

	index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it

	sims = index[vec_lsi] # perform a similarity query against the corpus
	#print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	#pprint(sims) # print sorted (document number, similarity score) 2-tuples
	for i in range(5): #number of suggestions to print
		print(str(i+1),': % ', str(sims[i][1]), ' ', documents[sims[i][0]],sep='')