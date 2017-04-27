import json
import nltk
import fasttext

path = 'wiki.da/wiki.da.bin'

if not 'model' in vars():
    model = fasttext.load_model(path)

print("all done")