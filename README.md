# Morphological lexicon Sloleks 3.0 parser

## What does this parser do?
This parser will extract all data from the the 1.5 GB XML file [found here](https://www.clarin.si/repository/xmlui/handle/11356/1745)
and put it in a SQLite database so that it can be used for further processing.

apart from converting to sql it also does the following:
- removes diplicate prouciations, accentuations, forms and lemmas
- some lexical units had dupliate IDS (for diferent words), which were updated to be unique
- some word forms had multiple orthography forms, which were split out into separate word_forms to enable correct linking to accentuation and pronunciation
- [] add MSD to lexical unit

## TODO:
- [] add comment, relatedEntryList and labelList to lexical unit
- [] more fields to word forms
- [] add script to generate missing accentuations and pronunciations

## How did you extract the XML data?
Like this:
```bash
# download the data
./get_data.sh
# activate a Python virtual environment
python3 -m venv env && source env/bin/activate
# install all dependencies
pip install -r requirements.txt
# run the parser
python convert.py
```

After about 45 min the data will get transferred to a 1 GB SQLite database called `sloleks.db`.

## Citations
 title = {Morphological lexicon Sloleks 3.0},	
 author = {{\v C}ibej, Jaka and Gantar, Kaja and Dobrovoljc, Kaja and Krek, Simon and Holozan, Peter and Erjavec, Toma{\v z} and Romih, Miro and Arhar Holdt, {\v S}pela and Krsnik, Luka and Robnik-{\v S}ikonja, Marko},	 Čibej, Jaka; et al., 2022, 
 url = {http://hdl.handle.net/11356/1745},	  Morphological lexicon Sloleks 3.0, Slovenian language resource repository CLARIN.SI, ISSN 2820-4042, 
 note = {Slovenian language resource repository {CLARIN}.{SI}},	  http://hdl.handle.net/11356/1745.