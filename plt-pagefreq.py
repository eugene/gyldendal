import pandas
import re
import json
import sys
import matplotlib.pyplot as plt
import numpy as np

df = pandas.read_csv('data/ReadingPattern.csv')
pages = []
for element in df['context.extensions.viewedPages']:
    pages.extend([int(re.search(r"\d+", x)[0]) for x in re.findall(r":\d+", element)])
    # print(re.search(r"/:/", element))

# pages
plt.hist(pages, len(np.unique(pages)), facecolor='blue', normed=1, alpha=0.75)
plt.xlabel('Page #')
plt.ylabel('Frequency')
plt.title(r'Most read pages')
plt.grid(True)
plt.show()
