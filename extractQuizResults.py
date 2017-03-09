#Python3
import pandas
import json
import sys

df = pandas.read_csv('Data/QuizResults.csv')

TA = df['TaskAnswers']

answers = []

for element in TA:
	data = json.loads(element)
	data = data.get('1')
	data = data.get('answers')
	answers.append(data)

df['answers'] = answers

df = df[['UserID','Title','TaskScore/PointsGotten','TaskScore/PointsTotal','answers']]

df = df.rename(columns={'TaskScore/PointsGotten': 'Gotten', 'TaskScore/PointsTotal': 'Total'})

df['Percent'] = df['Gotten']/df['Total']*100

print(df.head())


try:
	if sys.argv[1] == "debug":
		import IPython
		IPython.embed()
except:
	pass