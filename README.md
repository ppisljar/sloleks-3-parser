# Morphological lexicon Sloleks 2.0 parser

## What does this parser do?
This parser will extract all data from the the 1.5 GB XML file [found here](https://www.clarin.si/repository/xmlui/handle/11356/1230)
and put it in a SQLite database so that it can be used for further processing.

## Why did you convert the data from XML to SQL?
This parser played a key part in building my final project for [Harvard's CS50x course](https://cs50.harvard.edu/x/) as 
it allowed me to extract about 100.000 [lemmas][1] of the Slovenian language and use them an IndexedDB in a Chrome extension,
which was my final project.

## How did you extract the XML data?
Like this:
```bash
# download the data
wget https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1230/Sloleks2.0.LMF.zip
# activate a Python virtual environment
python3 -m venv env && source env/bin/activate
# install all dependencies
pip install -r requirements.txt
# run the parser
python convert.py -i Sloleks2.0.LMF.zip -x sloleks_clarin_2.0.xml -v
```

After about 45 min the data will get transferred to a 1 GB SQLite database called `sloleks.db`.

To extract the data for further use in my Chrome extension I exported it with this SQL query:
```sqlite
SELECT
       LOWER(fr.zapis_oblike) AS 'word',
       LOWER(l.zapis_oblike) AS 'lemma'
FROM form_representations fr
JOIN lemmas l ON fr.lexical_entry_id = l.lexical_entry_id
WHERE SUBSTR(l.zapis_oblike, 1, 1) NOT IN ('0', '1','2','3','4','5','6','7','8','9')
GROUP BY word
``` 

## Tell me more about Sloleks
Sloleks is the reference morphological lexicon for Slovenian language, developed to be used in NLP applications and 
language manuals. Encoded in LMF XML, the lexicon contains approx. 100,000 most frequent Slovenian lemmas, their 
inflected or derivative word forms and the corresponding grammatical description. Lemmatization rules, part-of-speech 
categorization and the set of feature-value pairs follow the JOS morphosyntactic specifications. In addition to 
grammatical information, each word form is also given the information on its absolute corpus frequency and its 
compliance with the reference language standard.


[1]: https://en.wikipedia.org/wiki/Lemma_(morphology)