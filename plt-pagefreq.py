import pandas
import re
import json
import sys
import matplotlib.pyplot as plt

df = pandas.read_csv('data/ReadingPattern.csv')
pages = []
for element in df['context.extensions.viewedPages']:
    pages.extend([int(re.search(r"\d+", x)[0]) for x in re.findall(r":\d+", element)])
    # print(re.search(r"/:/", element))

# pages
plt.hist(pages, 500, normed=1, facecolor='green', alpha=0.75)
