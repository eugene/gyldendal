# About
The Danish publisher Gyldendal has a set of learning objectives that they would like linked to the official learning objectives of the Ministry of Education in order to ensure that the material lives up to certain requirements. Different models within natural language processing, including LSI and fastText, were applied to the task and their performance evaluated. FastText, being the best model, was implemented into a reference web application, usable by Gyldendal.

[:page_facing_up: Full paper](PAPER.pdf)

## File descriptions

### analysis.py
Gammel model

### cmsextractjson.py
Creates 36hist.json from 'data/historie/34/\*.json'

### extractFFM.py
Extract all FMM relevant for our purposes, 'all_ffms.json' to 'FFM.json'

### ffm.py
Extract specific fmms from 'all_ffsm.json'

### test_gandalf.py
Gandalfs testing ground

### techdemo/techdemo.py
Technology demo
