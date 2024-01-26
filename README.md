# Morphological lexicon Sloleks 3.0 parser

## What does this parser do?
This parser will extract all data from the the 13 GB of XML [found here](https://www.clarin.si/repository/xmlui/handle/11356/1745)
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
# activate a Python virtual environment
python3 -m venv env && source env/bin/activate
# install all dependencies
pip install -r requirements.txt
# download the data
./get_data.sh
# run the parser
python convert.py
```

After about 1 hour the data will get transferred to a 2 GB SQLite database called `sloleks.db`.

dump was then generated with
```
sqlite3 sloleks.db .dump > sloleks.dump.sql
```


## schema

```
class LexicalEntry(Base):
    __tablename__ = "lexical_entries"
    id = Column(CHAR(35), primary_key=True)
    status = Column(String(16), nullable=True)
    sloleks_key = Column(String(64), index=True)
    lemma = Column(String(64), nullable=True)
    lexeme = Column(String(64), index=True)
    lexeme_type = Column(String(16), nullable=True)
    type = Column(String(16), nullable=True)
    category = Column(String(16), nullable=True)
    pronaunciation = Column(String(16), nullable=True)
    aspect = Column(String(16), nullable=True)
    frequency = Column(Integer, nullable=True)
    msd = Column(String(16), nullable=True)
    source = Column(String(64), index=True)

    def __repr__(self):
        return f"<LexicalEntry {self.id}>"


class WordForm(Base):
    __tablename__ = "word_forms"
    id = Column(Integer, primary_key=True)
    msd = Column(String(16), nullable=True)         #
    msd_system = Column(String(16), nullable=True)  #
    msd_language = Column(String(4), nullable=True)# 
    morphological_pattern_code = Column(String(16), nullable=True) 

    vform = Column(String(16), nullable=True)       # oblika
    number = Column(String(16), nullable=True)      # stevilo
    gender = Column(String(16), nullable=True)      # spol
    type = Column(String(16), nullable=True)          # tip
    person = Column(String(16), nullable=True)          # oseba
    negative = Column(String(16), nullable=True)        # nikalnost
    degree = Column(String(16), nullable=True)         # stopnja
    definiteness = Column(String(16), nullable=True)  # dolocnost
    case = Column(String(16), nullable=True)          # sklon
    aspect = Column(String(16), nullable=True)        # norma
    animate = Column(String(16), nullable=True)        # zivost
    clitic =Column(String(16), nullable=True)     # 
    owner_gender = Column(String(16), nullable=True)   # 
    owner_number = Column(String(16), nullable=True)   # 

    frequency = Column(Integer, nullable=True)      # pogostost

    form = Column(String(64), index=True)

    ACC_1 = Column(String(64), nullable=True)
    ACC_2 = Column(String(64), nullable=True)
    ACC_3 = Column(String(64), nullable=True)
    ACC_4 = Column(String(64), nullable=True)
    SAMPA_1 = Column(String(64), nullable=True)
    SAMPA_2 = Column(String(64), nullable=True)
    SAMPA_3 = Column(String(64), nullable=True)
    SAMPA_4 = Column(String(64), nullable=True)
    IPA_1 = Column(String(64), nullable=True)
    IPA_2 = Column(String(64), nullable=True)
    IPA_3 = Column(String(64), nullable=True)
    IPA_4 = Column(String(64), nullable=True)

    lexical_entry_id = Column(
        CHAR(35), ForeignKey("lexical_entries.id"), nullable=False, index=True
    )
    lexical_entry = relationship(
        "LexicalEntry",
        backref=backref("word_forms", cascade="all, delete-orphan", lazy="dynamic"),
    )
```

## pubished SQL database

you can find exported sqlite file here: https://huggingface.co/datasets/ppisljar/sloleks-3-sql/blob/main/sloleks.db
and the sql dump file which can be used to import the database to other SQLs (mysql, postgre, ...) is here: https://huggingface.co/datasets/ppisljar/sloleks-3-sql/blob/main/sloleks.dump.sql

## Citations
 title = {Morphological lexicon Sloleks 3.0},	
 author = {{\v C}ibej, Jaka and Gantar, Kaja and Dobrovoljc, Kaja and Krek, Simon and Holozan, Peter and Erjavec, Toma{\v z} and Romih, Miro and Arhar Holdt, {\v S}pela and Krsnik, Luka and Robnik-{\v S}ikonja, Marko},	 Čibej, Jaka; et al., 2022, 
 url = {http://hdl.handle.net/11356/1745},	  Morphological lexicon Sloleks 3.0, Slovenian language resource repository CLARIN.SI, ISSN 2820-4042, 
 note = {Slovenian language resource repository {CLARIN}.{SI}},	  http://hdl.handle.net/11356/1745.