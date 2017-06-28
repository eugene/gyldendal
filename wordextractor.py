import fasttext
import numpy as np 
from IPython import embed
import json
from scipy import spatial
import matplotlib.pyplot as plt

with open('34hist.json') as data_file:
    data = json.load(data_file)

if not 'model' in vars():
    model = fasttext.load_model('fastText/wiki.da.bin')

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
kompetence =[
                "Eleven kan relatere ændringer i hverdag og livsvilkår over tid til eget liv",
                "Eleven kan anvende kilder til at opnå viden om fortiden",
                "Eleven kan fortælle om, hvordan mennesker er påvirket af og bruger historie"
            ],

viden = [
                "Eleven har viden om relativ kronologi",
                "Eleven har viden om fællesskaber før og nu",
                "Eleven har viden om livsgrundlag og produktion før og nu",
                "Eleven har viden om magtforhold og samfundsstrukturer før og nu",
                "Eleven har viden om kanonpunkter",
                "Eleven har viden om identifikation af historiske spor i lokalområdet",
                "Eleven har viden om enkle kildekritiske metoder",
                "Eleven har viden om enkle fagord og begreber og historiske kilders formål og struktur",
                "Eleven har viden om historiske scenarier",
                "Eleven har viden om særtræk ved historiske fortællinger",
                "Eleven har viden om personer og hændelser, der tillægges betydning i historien"
            ]



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

færdighedvec = []
#Find vektorer til alle færdigheder
for f in færdighed:
        færdighedvec.append(model[f])


predict_correct = []
predict_correct2 = []
#Test al data for top 1 præcision
TOP = 8

tester = []
for i in range(len(data)):
    if correct[i] != -1:
        datapoint = data[str(i)]
        text = datapoint['text']
        mål = datapoint['færdighed']
        #print(text)
        #print(mål)
        #print(' ')
        #Initialize array
        best = 1000
        dist_result = [ [], []  ]
        for _ in range(TOP):
            dist_result[0].append(1000)
            dist_result[1].append('')
        #print('Result = {}'.format(result))

        for i2, f in enumerate(færdighedvec):
            dist = spatial.distance.cosine(np.array(f), np.array(model[text]))
            if dist < best:
                result = færdighed[i2]
                best = dist
            if dist < max(dist_result[0]):
                index = dist_result[0].index(max(dist_result[0]))
                dist_result[0][index] = dist
                dist_result[1][index] = færdighed[i2]

            if mål == færdighed[i2]:
                tester.append(i2)


        #print('Result = {}'.format(result))
        #print('Mål = {}'.format(mål))
        if result == mål:
            predict_correct.append(1)
        else:
            predict_correct.append(0)

        if mål in dist_result[1]:
            predict_correct2.append(1)
        else:
            predict_correct2.append(0)

#print('Accuracy(TOP1) = ', np.mean(predict_correct)*100,'%')
#print('Accuracy(TOP{}) = '.format(TOP), np.mean(predict_correct2)*100,'%')

plotti = [42.5, 56.16, 68.49, 73.97, 83.56, 90.41, 95.89]
plt.plot(list(range(1,len(plotti)+1)),plotti)
plt.grid()
plt.xlabel(("TOP X"))
plt.ylabel(("Accuracy"))
plt.ylim([40,100])
plt.show()
