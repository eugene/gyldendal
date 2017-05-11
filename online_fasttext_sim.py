from fasttext_sim import *

import math
import random

test_size = math.ceil(len(texts)*0.4)
test_ids = random.sample(range(0, len(texts)), test_size)

texts_train = {}
texts_test  = {}

for k, v in enumerate(texts.keys()):
	copy = {
		"vector": texts[v]["vector"],
		"text":   texts[v]["text"],
		"skill":  texts[v]["skill"]
	}
	if k in test_ids:
		copy["distance"] = texts[v]["distance"]
		texts_test[v] = copy
	else:
		texts_train[v] = copy

online_accuracy_base = []
for i in range(len(ffms)):
	a = 0
	for k, v in texts_test.items():
		distances = OrderedDict(sorted(v["distance"].items(), key=lambda item: item[0]))
		matches = [m["match"] for m in [v for v in distances.values()]]
		a += np.sum(matches[0:(i+1)])
	online_accuracy_base.append(a / len(texts_test))

[texts_test[d].pop("distance", None) for d in texts_test] # small cleanup

for k in texts_test:
	texts_test[k]["distances"] = []

	for kk in ffms:
		texts_test[k]["distances"].append([cosine_distance(texts_test[k]["vector"], ffms[kk]["vector"]), kk])	

	for kk in texts_train:
		texts_test[k]["distances"].append([cosine_distance(texts_test[k]["vector"], texts_train[kk]["vector"]), texts_train[kk]["skill"]])

	seen = {}
	result = []
	distances = OrderedDict(sorted(texts_test[k]["distances"], key=lambda item: item[0]))
	for i, pair in enumerate(distances.items()):
		if pair[1] not in seen:
			result.append(pair)
			seen[pair[1]] = True

	texts_test[k]["distances"] = []
	for r in result:
		if r[1] == texts_test[k]["skill"]:
			texts_test[k]["distances"].append([r[0], r[1], True])
		else:
			texts_test[k]["distances"].append([r[0], r[1], False])

online_accuracy_final = []
for i in range(len(ffms)):
	a = 0

	for k in texts_test:
		matches = [m[2] for m in [v for v in texts_test[k]["distances"]]]
		a += np.sum(matches[0:(i+1)])
		
	online_accuracy_final.append(a / len(texts_test))

def offline_accuracy_plot():
	plt.plot(range(len(ffms)), online_accuracy_base)
	plt.plot(range(len(ffms)), online_accuracy_final)
	plt.legend(['Base (offline) accuracy', 'Online accuracy'], loc='upper left')
	plt.grid()
	plt.xlabel(("In top X"))
	plt.ylabel(("Accuracy"))
	plt.show(block=False)
	input("Hit Enter To Close")
	plt.close()
