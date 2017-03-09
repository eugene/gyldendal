#Python3
import pandas
import json
import sys
df = pandas.read_csv('Data/QuizResults.csv')
df2 = pandas.read_table('Data/UserDBextraction_unique_usersHASHED.txt')



#Get a list of unique users
uniqueusers = []
for f in df2['/*']:
	if len(f) > 52:
		uniqueusers.append(f.rstrip(','))

#Translate hash to a readable user number
hashtouser = []
for k in df['UserID']:
	hashtouser.append(uniqueusers.index(k))

df['UserID'] = hashtouser
 

TA = df['TaskAnswers']

answers = []

for element in TA:
	data = json.loads(element)
	data = data.get('1')
	data = data.get('answers')
	answers.append(data)

df['answers'] = answers

df = df[['UserID','Title','TaskScore/PointsGotten','TaskScore/PointsTotal','answers']]

df = df.rename(columns={'TaskScore/PointsGotten': 'Gotten', 'TaskScore/PointsTotal': 'Total', 'Title':'Quiz'})

df['Percent'] = df['Gotten']/df['Total']*100

df['Quiz'] = df['Quiz'].map(lambda x: x.lstrip('Quiz\+').rstrip('.'))

print(df.head())


try:
	if sys.argv[1] == "debug":
		import IPython
		IPython.embed()
except:
	pass