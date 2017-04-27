import fasttext
import numpy as np
import pandas as pd
import math
import sys

# Run with
# $ ipython
# [1] run -i fasttextclassify.py


def cossim(a, b):
    """
    Computes the cosine similarity of the vectors a and b.
    Input:      Numpy vectors of arbitrary but equal lengths
    Output:     Scalar in range [0,1]
                1   Identical
                .5  Orthogonal
                0   Identical but opposite
    """
    return 1 - math.acos(a.dot(b) / (np.linalg.norm(a, ord=2) * np.linalg.norm(b, ord=2))) / math.pi


def getsuggestion(model, fftvecs):
    # Take objective input
    objective = sys.argv[1:]
    objective = [
        'Eleven kan bruge historiske spor i lokalområdet til at fortælle om fortiden']

    # Compute similarities
    similarities = []
    vec = np.asarray(model[objective])
    for fftvec in fftvecs:
        similarities.append(cossim(vec, fftvec))

    # Sort descending
    similarities_sorted = sorted(similarities, reverse=True)
    fftsuggestions = [x for (y, x) in sorted(
        zip(similarities, ffts), reverse=True)]
    return (similarities_sorted, fftsuggestions)


if 'model' not in vars():
    path = "/Users/Jakob/Desktop/gyldendal/fastText/wiki.da/wiki.da.bin"
    model = fasttext.load_model(path)

# Number of suggestions
n = 5

# Create list with FFMs
path = 'FFM.json'
data = pd.read_json(path)
ffts = dict()
fftvecs = []
for i in data.keys():  # fag
    for j in data[i].keys():  # klassetrin
        if type(data[i][j]) is dict:
            ffts[(i, j) = data[i][j]


"""

#(similarities_sorted, fftsuggestions) = getsuggestion(model, fftvecs)
# Take objective input
objective = sys.argv[1:]
objective = [
    'Eleven kan bruge historiske spor i lokalområdet til at fortælle om fortiden']

# Compute similarities
similarities = []
vec = np.asarray(model[objective])
for fftvec in fftvecs:
    similarities.append(cossim(vec, fftvec))

# Sort descending
similarities_sorted = sorted(similarities, reverse=True)
fftsuggestions = [x for (y, x) in sorted(
    zip(similarities, ffts), reverse=True)]

for i in range(n):
    print(str(round(similarities_sorted[i], 4)) + "\t" + fftsuggestions[i])
"""
