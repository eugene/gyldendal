import logging
import json
import numpy as np
import matplotlib.pyplot as plt
#import seaborn

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora

with open('FFM.json') as data_file:
    FFM = json.load(data_file)

with open('34hist.json') as data_file:
    data = json.load(data_file)


færdighed = [
                "Eleven kan placere elementer fra historien tidsmæssigt i forhold til hinanden",
                "Eleven kan sammenligne tidlige tiders familie, slægt og fællesskaber med eget liv",
                "Eleven kan beskrive ændringer i livsgrundlag og produktion",
                "Eleven kan beskrive ændringer i magtforhold og samfundsstrukturer over tid",
                "Eleven kan bruge kanonpunkter til at skabe historisk overblik og sammenhængsforståelse",
                "Eleven kan bruge historiske spor i lokalområdet til at fortælle om fortiden",
                "Eleven kan bruge digitale medier og andre udtryksformer som kilder til at beskrive fortiden",
                "Eleven kan læse enkle historiske kilder og udtrykke sig sprogligt enkelt om deres indhold",
                "Eleven kan opnå viden om historie gennem brug af historiske scenarier",
                "Eleven kan skelne mellem typer af historiske fortællinger",
                "Eleven kan forklare, hvorledes de og andre er historieskabte og skaber historie"
            ]

documents = færdighed

v = "eleven kan viden om af alle alt andre at blev bliver bort da dag de dem den der deres det dig dog du efter eller en end er et far fik fin for forbi fordi frafri få gik glad godt ham han hanshar havde have hele hen hende her hjemhun hvad hver hvis hvor igen ikke indjeg jer jo kan kom kommer kun kunnelang lidt lige lille løb man mange medmeget men mere mig min mod mon måned nej noget nok nu når og ogsåom op os over på sagde se selvsidste sig sin sine skal skulle små somstor store så tid til tog ud undervar ved vi vil ville være været år"
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
#dictionary = corpora.Dictionary.load('/tmp/tmm.dict')
corpus = corpora.MmCorpus('/tmp/tmm.mm') # comes from the first tutorial, "From strings to vectors"

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=12)



correct = []
for i in range(len(data)):
    datapoint = data[str(i)]
    text = datapoint['text']
    mål = datapoint['færdighed'] + ' ' + datapoint['viden']
    for i2, f in enumerate(færdighed):
        if f == datapoint['færdighed']:
            correct.append(i2)
    if datapoint['færdighed'] not in færdighed:
        print(datapoint['færdighed'])
        print(' ')
        correct.append(-1)

#embed()





predict_correct = []
for i in range(len(data)):
    if correct[i] != -1:
        datapoint = data[str(i)]
        doc = datapoint['text']
        mål = datapoint['færdighed']

        #Initialize array
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow] # convert the query to LSI space

        index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it

        sims = index[vec_lsi] # perform a similarity query against the corpus
        #print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #pprint(sims) # print sorted (document number, similarity score) 2-tuples
        for i in range(11): #number of suggestions to print
            print(str(i+1),': % ', str(sims[i][1]), ' ', documents[sims[i][0]],sep='')
            if documents[sims[i][0]] == mål:
                predict_correct.append(i+1)
                #print('Result = {}'.format(result))
                #print('Mål = {}'.format(mål))

import random
result = np.zeros(11)
for h in range(100):
    for i in range(len(data)):
        if correct[i] != -1:
            datapoint = data[str(i)]
            doc = datapoint['text']
            mål = datapoint['færdighed']
            guess = random.sample(range(11), 11)
            for element,i2 in enumerate(guess):
                if færdighed[element] == mål:
                    result[i2] = result[i2] + 1

result = result/(100*73)
for i in range(1,11):
    result[i] = result[i]+result[i-1]




f = np.array(predict_correct)

accuracy = []

for i in range(1,8):
    accuracy.append( sum(f <= i) / len(predict_correct) * 100 )

plt.figure()
plt.rc('font', size = 50)
plt.rc('font', family='serif')
#Plot from Fasttext
plotti = [42.5, 56.16, 68.49, 73.97, 83.56, 90.41, 95.89]
plt.plot(list(range(1,len(plotti)+1)),plotti,label='Fasttext',linewidth=5.0)
plt.scatter(list(range(1,len(plotti)+1)),plotti,linewidth=6.0)
#Plot of LSI accuracy
plt.plot(list(range(1,len(accuracy)+1)),accuracy,label='LSI',linewidth=5.0)
plt.scatter(list(range(1,len(accuracy)+1)),accuracy,linewidth=6.0)
plt.plot([1,2],[40.4, 47.6],label='"Human"',linewidth=5.0)
plt.scatter([1,2],[40.4, 47.6],linewidth=6.0)

result = result[:-4]
plt.plot(list(range(1,len(result)+1)),result*100,label='Random Guess',linewidth=5.0)
plt.grid()
plt.xlabel(("TOP X"))
plt.ylabel(("Accuracy [%]"))
#plt.title('Accuracy of Fasttext and LSI')
plt.legend(loc='upper left')
plt.ylim([0,100])
plt.show()