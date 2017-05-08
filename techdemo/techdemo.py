# To run the thing do:
# 
# 1) Make sure you have flask and everything else installed (pip install blah)
# 2) replace with your model path and run: 
#
#    FLASK_APP=techdemo.py FLASK_DEBUG=1 MODEL_PATH="/Users/eugene/Git/fastText/models/wiki.da.bin" python -m flask run
# 

import fasttext
import json
import pandas
import numpy as np
import scipy
import string # for punctuation
import os # to access environment variables

from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine as cosine_distance
from collections import OrderedDict
import matplotlib.pyplot as plt

from flask import Flask, request, send_from_directory, render_template

if not 'model' in vars():
	path = os.environ['MODEL_PATH']
	model = fasttext.load_model(path)

def read_ffms():
	with open('../FFM.json') as data_file:    
		data = json.load(data_file)["Historie"]["3. - 4. klasse"]
		faerdiheder = data["færdighed"]
		viden = data["viden"]

		return {"faerdiheder": faerdiheder, "viden": viden}

#####################################
# dirty web development stuff below #
#####################################
app = Flask(__name__, static_url_path='')

@app.route('/suggest', methods=["POST"])
def suggest(text = None):
	ffms = read_ffms()
	t = request.form['text']
	if not t:
		return render_template('cards.html', text=None)

	text_score = model[t]
	distances = {}
	for (i, text) in enumerate(ffms["faerdiheder"]):
		ffm_score = model[text]
		distance = cosine_distance(text_score, ffm_score)
		distances[float(distance)] = i
	
	distances = OrderedDict(sorted(distances.items(), key=lambda item: item[0]))
	rendered = []
	for i in distances:
		index = distances[i]
		data = { 
			"first": (i == list(distances.keys())[0]),
			"score": "{0:.2f}".format(i), 
			"faerdighed": ffms["faerdiheder"][index], 
			"viden": ffms["viden"][index] 
		}
		rendered.append(render_template('card.html', data=data))

	return render_template('cards.html', text=(' '.join(rendered[0:5])))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
@app.route('/<portal_name>')
def main(portal_name = None):
	return render_template('main.html', portal_name=portal_name)
