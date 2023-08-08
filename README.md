# Morphological lexicon Sloleks 3.0 parser

## What does this parser do?
This parser will extract all data from the the 1.5 GB XML file [found here](https://www.clarin.si/repository/xmlui/handle/11356/1745)
and put it in a SQLite database so that it can be used for further processing.


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

After about 45 min the data will get transferred to a 2 GB SQLite database called `sloleks.db`.

 @misc{11356/1745,
 title = {Morphological lexicon Sloleks 3.0},
 author = {{\v C}ibej, Jaka and Gantar, Kaja and Dobrovoljc, Kaja and Krek, Simon and Holozan, Peter and Erjavec, Toma{\v z} and Romih, Miro and Arhar Holdt, {\v S}pela and Krsnik, Luka and Robnik-{\v S}ikonja, Marko},
 url = {http://hdl.handle.net/11356/1745},
 note = {Slovenian language resource repository {CLARIN}.{SI}},
 copyright = {Creative Commons - Attribution-{ShareAlike} 4.0 International ({CC} {BY}-{SA} 4.0)},
 issn = {2820-4042},
 year = {2022} }